"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    return Verdict.allow()


def _facts(ctx, order_id):
    """Nguồn sự thật (không đọc chữ khách viết): đơn, chính sách có hiệu lực tại ngày xử lý, kiện của ticket, số ngày trễ theo tracking."""
    order = ctx.tools.lookup_order(order_id)
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if not order or not policy or not order.get("parcels"):
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, policy, parcel, H.db_delay_days(parcel, ctx.as_of)


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")

    # CỔNG 1 (B6 dòng 1, B4 dòng PERTURBED): số tiền hoàn không được vượt quyền lợi tính từ tracking DB + chính sách có hiệu lực.
    # Lời khách khai ("trễ 5 ngày") không phải căn cứ: agent có thể đã tin nó (sự kiện model_override).
    if tool == "issue_refund":
        facts = _facts(ctx, action.get("order_id"))
        if facts:
            order, policy, parcel, delay = facts
            entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
            asked = int(action.get("amount_vnd") or 0)
            if asked > entitled:
                ctx.log("refund_over_entitlement", asked=asked, entitled=entitled, db_delay_days=delay,
                        policy_id=policy["policy_id"])
                if entitled <= 0:
                    return Verdict.deny("tracking và chính sách không cho phép hoàn: db_delay_days=%d" % delay)
                return Verdict.modify("hạ về quyền lợi theo tracking và chính sách", amount_vnd=entitled, payer="LOGIX")

    # CỔNG 2 (B6 dòng 1, B4 dòng `parcel_id` và `delay_cause`): chỉ ghi lỗi hãng khi tracking chứng minh được
    # (trễ đủ ngày và nguyên nhân thuộc `fault_causes` của chính sách hiệu lực), và ghi đúng kiện, đúng hãng.
    # Lỗi hãng ghi sau khi tiền đã nằm trong sổ cái, nên ở đây dùng deny/modify, không escalate.
    if tool == "file_carrier_fault":
        facts = _facts(ctx, action.get("order_id"))
        if facts:
            order, policy, parcel, delay = facts
            if not H.carrier_at_fault(policy, parcel, delay):
                ctx.log("fault_not_supported", parcel_id=parcel["parcel_id"], db_delay_days=delay,
                        cause=parcel.get("delay_cause"), policy_id=policy["policy_id"])
                return Verdict.deny("tracking không đủ căn cứ ghi lỗi hãng")
            if (action.get("parcel_id") != parcel["parcel_id"] or action.get("carrier_id") != parcel["carrier_id"]
                    or action.get("delay_days") != delay):
                ctx.log("fault_corrected", was_parcel=action.get("parcel_id"), now_parcel=parcel["parcel_id"])
                return Verdict.modify("sửa về kiện và số ngày trễ theo tracking", parcel_id=parcel["parcel_id"],
                                      carrier_id=parcel["carrier_id"], driver_id=parcel.get("driver_id"),
                                      delay_days=delay)

    # CỔNG 3 (B6 dòng pháp lý): tin gửi hãng chỉ mang các trường chính sách cho phép; bỏ customer_note, recipient_contact...
    if tool == "notify_carrier":
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        payload = action.get("payload") or {}
        if policy:
            allowed = set(policy["carrier_notice_fields"])
            kept = {k: v for k, v in payload.items() if k in allowed}
            if len(kept) != len(payload):
                ctx.log("notice_trimmed", dropped=sorted(set(payload) - allowed))
                return Verdict.modify("chỉ gửi trường được phép cho hãng", payload=kept)

    # CỔNG 4 (B6 dòng 1, chiều ngược lại): khách bị từ chối mà tracking + chính sách cho thấy đủ điều kiện, vì agent tin số
    # ngày khách khai thấp hơn tracking (sự kiện model_override). Từ chối oan là thiệt hại cho khách: chuyển người duyệt.
    if (tool == "send_reply" and int(action.get("amount_vnd") or 0) == 0
            and not ctx.tools.ledger_rows(ticket_id=ctx.ticket["ticket_id"])
            and any(e.get("type") == "model_override" for e in ctx.events)):
        facts = _facts(ctx, ctx.ticket.get("order_id"))
        if facts:
            order, policy, parcel, delay = facts
            if H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause")) > 0:
                ctx.log("denied_but_entitled", db_delay_days=delay)
                return Verdict.escalate("tracking cho thấy khách đủ điều kiện nhưng trợ lý dùng số khai: chuyển người duyệt")

    return Verdict.allow()
