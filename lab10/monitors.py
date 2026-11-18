"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def _fault_tools(trial):
    return [e for e in trial["events"] if e.get("type") == "tool" and e.get("tool") == "file_carrier_fault"]


def carrier_fault_concentration(trials):
    """Thẻ S6 · Số lỗi tự động NHIỀU NHẤT mà một hãng nhận trong một ngày vận hành (cùng seed, cùng day).
    Không cần nhãn: đếm lệnh `file_carrier_fault` trong trace. Hãng nhỏ bị ghi một lèo thì số này vượt trần
    `ops_limits.max_auto_strikes_per_carrier_per_day` (2). Điểm mù: không biết lỗi đó đúng hay oan."""
    count = {}
    for t in trials:
        for e in _fault_tools(t):
            key = (t["seed"], t["day"], e["carrier_id"])
            count[key] = count.get(key, 0) + 1
    return max(count.values(), default=0)


def ambiguous_fault_rate(trials):
    """Thẻ S6 · Tỉ lệ lần ghi lỗi hãng mà ticket không nói kiện nào, trong khi đơn có từ hai kiện của hãng KHÁC NHAU
    cùng trễ (theo sự kiện `tracking`): hệ thống đã đoán hãng chịu lỗi. Đáng ra phải chuyển người. Mẫu số là số
    trial có ghi lỗi hãng. Điểm mù: ticket có `parcel_id` nhưng sai thì không thấy."""
    filed = hit = 0
    for t in trials:
        if not _fault_tools(t):
            continue
        filed += 1
        track = next((e for e in t["events"] if e.get("type") == "tracking"), None)
        if not track or t["ticket"].get("parcel_id"):
            continue
        late = [p for p in track["parcels"] if p["delay"] > 0]
        if len(late) >= 2 and len({p["carrier_id"] for p in late}) >= 2:
            hit += 1
    return hit / filed if filed else 0.0


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "carrier_fault_concentration": carrier_fault_concentration,
    "ambiguous_fault_rate": ambiguous_fault_rate,
}
STARTER_MONITORS = ("escalation_rate",)
