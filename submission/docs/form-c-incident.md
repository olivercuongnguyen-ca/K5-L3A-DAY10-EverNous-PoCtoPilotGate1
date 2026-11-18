# Phiếu C · Sự cố và quyết định v2 · Khối 3 (phút 125–200)

**Bàn:** EverNous · **Thẻ đã bốc:** S6 *(để trống tới phút 125; bốc số xong thì ghi đúng số đó, ví dụ `S3`. Lab Coach đối chiếu với sổ; lệnh tự kiểm tra in dòng này trong report.)*

Mở `incidents/Sx/card.md` của đúng số đã bốc. Các bước trên thẻ trỏ về đúng mục trong phiếu này. Mục C3 chỉ điền phần ứng với
số thẻ của bàn; các phần khác để trống.

**Mục lục**
- [C0 · Nhật ký lần chạy vòng 2 (suốt khối)](#c0)
- [C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem · phút 125–135 · bước 0 trên thẻ](#c1)
- [C2 · Câu 3.1 · Bảng soát lỗi của thẻ · phút 135–145 · bước 1–2](#c2)
- [C3 · Câu 3.1 · Phần riêng theo thẻ · phút 135–145 · bước 3](#c3)
- [C4 · Câu 3.1 · HAZOP của thẻ (≥ 3 dòng) · phút 145–150 · bước 4](#c4)
- [C5 · Câu 3.2, 3.3 · Specification và giả định môi trường · phút 145–150 · bước 4](#c5)
- [C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa · phút 150–155 · bước 4](#c6)
- [C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn · phút 155–180 · bước 5–7](#c7)
- [C8 · Câu 3.6 · Chỉ số theo dõi mới · phút 155–180 · bước 5](#c8)
- [C9 · Câu 3.7 · Fault tree SAU khi sửa · phút 180–185 · bước 8](#c9)
- [C10 · Câu 3.7 · Risk register (≥ 1 dòng) · phút 180–185 · bước 8](#c10)
- [C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5 · phút 180–185 (runbook có thể xong trong 185–200) · bước 8](#c11)
- [C12 · Quyết định Gate 1 · v2 và ba dòng bắt buộc · phút 185–200 · bước 9](#c12)

---

<a id="c0"></a>

## C0 · Nhật ký lần chạy vòng 2

Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi một dòng vào `runs/journal.jsonl`. Điền cột "Đổi MỘT thứ gì" (tham số `--note`) và "Kết luận".

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | `R-S6-prepared-20261118-171120-683190` | S6 · prepared | nhận thẻ S6, chưa sửa thêm (đúng cổng vòng 1 đã chốt `437b79da`) | 0,6667 [0,4167; 0,9167] | 0,6667 | 270.000đ · 20 · 0 | 0,0 (khối hàng chờ: 0,0833) | Cổng vòng 1 đỡ một nửa (pass 0,3333 → 0,6667; lỗi hãng oan 40 → 20) nhưng còn hoàn sai 270.000đ và 20 lỗi oan. |
| 2 | `R-S6-after-20261118-170307-779ee5` | S6 · after | thêm hai cổng: A `pre_guard` chuyển người khi ticket không nói kiện mà có ≥ 2 kiện của hãng khác nhau cùng trễ; B `write_gate` bỏ lệnh ghi lỗi khi hãng đã đủ 2 lỗi tự động trong ngày | 1,0 [1,0; 1,0] | 1,0 | 0đ · 0 · 0 | 0,1667 | Hết ticket hỏng trên gói nhìn thấy (60/60 lần chạy đúng). |
| 3 | `R-S6-after-20261118-170347-683190` | S6 · after | thêm hai chỉ số theo dõi `carrier_fault_concentration` và `ambiguous_fault_rate` (không đổi cổng) | 1,0 [1,0; 1,0] | 1,0 | 0đ · 0 · 0 | 0,1667 | Kết quả giữ nguyên; chỉ số sáng đèn: trước sửa 4,0 và 0,1667, sau sửa 2,0 và 0,0. |
| 4 | `R-base-after-20261118-170348-683190` | base · after | (kiểm không regression, cùng mã) | 1,0 [1,0; 1,0] | 1,0 | 0đ · 0 · 0 | 0,2273 | Bộ nền vẫn 110/110 đúng, không ca nào hỏng thêm; 13 test OK. |

---

<a id="c1"></a>

## C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem

Chạy **trước khi sửa bất cứ thứ gì**:

```bash
python3 -m lab10.grade --incident Sx
```

- Mã lần chạy grade: `R-S6-grade-20261118-171119-683190` · base: `R-S6-before-20261118-171120-683190` · prepared: `R-S6-prepared-20261118-171120-683190` (lần đầu, chưa sửa: grade `R-S6-grade-20261118-165740-e04e78`, prepared `R-S6-prepared-20261118-165741-e04e78`)
- Cổng vòng 1 đỡ được ô / con số nào (so cột base với cột prepared): trên gói S6 nhìn thấy (60 lần chạy), `pass_rate` 0,3333 → 0,6667, `pass_k` 0,3333 → 0,6667, lỗi hãng oan 40 → 20. Cổng 2 của vòng 1 (ghi lỗi đúng kiện theo tracking, dùng `H.ticket_parcel`) sửa các ticket có `parcel_id` (`S6-01` đến `S6-04`). **Không đỡ được:** hoàn sai vẫn 270.000đ (`S6-20`, `S6-21`) và 20 lỗi oan còn lại (`S6-20`, `S6-21`, `S6-42`, `S6-43`).
- Khối kinh doanh và vận hành còn dòng nào vượt trần: không dòng nào (ROI 0,53, chi phí 3.595đ/ticket, 0 ca ùn, hoàn tự động 96.000đ so với ngân sách 2.000.000đ). Tác hại nằm ở ngưỡng an toàn đã ký (hoàn sai và lỗi hãng oan), không phải ở trần vận hành.

**Mở lại pre-mortem (Phiếu B mục B6), viết bằng bút khác màu.** Với thẻ S1, S3, S4, S5 đây là một phần của phần riêng theo thẻ.

- Sự cố trên thẻ thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)? **Pháp lý** (hãng nhỏ GHSH và DNB là bên thứ ba bị ghi lỗi oan) và **con người** (tài xế bị trừ thưởng chuyên cần); gốc kỹ thuật là mô hình đơn một hãng.
- Có nằm trong các lý do bàn đã viết không? **Một phần.** B4 vòng 1 đã có nhánh "đơn nhiều kiện, lấy `parcels[0]`" (WRONG) và B6 dòng 1 về ghi oan hãng; cổng vòng 1 đỡ được nửa số lỗi oan (40 → 20). Bàn **không** nghĩ tới hai điều: ticket không nói kiện nào khi hai hãng cùng trễ, và hãng nhỏ bị dồn nhiều lỗi trong một ngày; cả hai đều nằm ngoài ví dụ một ticket của bộ nền.
- Lý do còn thiếu, thêm bây giờ:

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được bằng gì (trace / data / config nào) |
|---|---|---|
| Ticket không nói kiện nào, hai hãng cùng trễ, trợ lý tự chọn một hãng và ghi lỗi cho hãng đó. | Pháp lý | Trace `S6-20@11`, `S6-21@11`: `tracking.parcels` có hai kiện trễ, `file_carrier_fault` ghi cho `O-2620-P1` (GHSH). |
| Hãng nhỏ bị ghi nhiều lỗi liên tiếp trong một ngày, chạm ngưỡng tạm ngưng 3 lỗi/7 ngày, tài xế mất thưởng. | Con người và vận hành | Trace `S6-40` đến `S6-43`: 4 lỗi GHSH trong một ngày; `data/world.json` → `carriers[].suspend_after_strikes_7d` (GHSH = 3, DNB = 3), `ops_limits.max_auto_strikes_per_carrier_per_day = 2`. |

---

<a id="c2"></a>

## C2 · Câu 3.1 · Bảng soát lỗi của thẻ

Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau:

```bash
python3 -m lab10.trace --suite Sx --ticket <ID> --seed 11
```

Ba loại lỗi: **giới hạn của hệ thống** · **lỗi ngữ cảnh** · **lỗi chìm** (cả người dùng lẫn hệ thống đều không nhận ra; nguy hiểm nhất,
người chịu hại thường là bên thứ ba). Định nghĩa đầy đủ và ví dụ: Phiếu B mục B2.

**Tác hại của thẻ:** cho ai **hãng vận chuyển nhỏ (GHSH, DNB) và tài xế của họ, bị ghi lỗi giao trễ của hãng khác** · đo bằng gì **`wrongful_carrier_faults` (lỗi hãng oan) và `wrongful_refund_vnd`** · bao nhiêu ở mốc base **40 lỗi oan và 270.000đ hoàn sai** (gói S6 nhìn thấy, 60 lần chạy; `R-S6-before-20261118-171120-683190`)

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | `S6-01@11` (mốc base): `tracking.parcels` cho `O-2601-P1` (GHSH) trễ 0 ngày và `O-2601-P2` (VNX) trễ 4 ngày; ticket có `parcel_id: O-2601-P2`; nhưng dòng `file_carrier_fault` ghi `parcel_id: O-2601-P1`, `carrier_id: GHSH`, `delay_days: 4`. Nhãn: lỗi cho VNX. | **GHSH** chịu lỗi của kiện đúng hẹn; khách và LogiX không thấy. Tài xế `TX-GHSH-06` mất thưởng. | Cao | **Lỗi chìm** |
| 2 | `S6-20@11`: đơn `O-2620` có `O-2620-P1` (GHSH, trễ 3 ngày) và `O-2620-P2` (VNX, trễ 5 ngày); ticket "Đơn của tôi giao chậm" không nói kiện nào. Trợ lý hoàn 26.000đ và ghi lỗi `O-2620-P1` GHSH với `delay_days: 5` (số ngày của kiện kia). Nhãn: chuyển người, không hoàn, không ghi lỗi. | **Hãng bị chọn nhầm** (có thể là cả hai hãng đều không đúng) và LogiX mất 26.000đ; khách thấy "đã hoàn" nên không biết có gì sai. | Cao | **Lỗi chìm** |
| 3 | `S6-42@11` và `S6-43@11` trong chuỗi ngày của `S6-40` đến `S6-43`: cùng hãng GHSH nhận lỗi thứ 3 và thứ 4 trong ngày (kiện đều trễ thật, `delay_cause: CARRIER`). Nhãn: không ghi lỗi (từ lỗi thứ 3 phải có người duyệt). Chỉ số `carrier_fault_concentration` = 4,0 ở mốc base. | **GHSH**, hãng nhỏ 12 tài xế, bị dồn lỗi sát ngưỡng tạm ngưng 3 lỗi/7 ngày (`suspend_after_strikes_7d`). | Cao | **Giới hạn của hệ thống** (không có trần theo hãng) và **chìm** vì không ai thấy số cộng dồn |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | **Có.** Bỏ qua `parcel_id` của ticket; lấy kiện đầu tiên của đơn. | **Có.** Ticket thiếu kiện, hệ thống tự điền bằng kiện đầu. | Không |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | Không: tracking có độ trễ từng kiện. | **Có.** Thiếu thông tin để biết khách nói kiện nào; hai hãng cùng trễ. | Không: dữ liệu đủ, thiếu chỗ chặn. |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | **Có, về đơn vị:** hãng và điều phối coi **kiện** là đơn vị chịu lỗi, hệ thống coi **đơn** (hãng của kiện đầu). | Có, cùng gốc. | Không. |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | Không. | Không. | **Có.** Nhiều lỗi nhỏ cộng dồn thành tạm ngưng hãng. |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| Vì sao người gặp coi đây là lỗi | Sổ giao của GHSH ghi kiện đúng hẹn, mà bị tính lỗi và trừ thưởng chuyên cần của tài xế. | Hãng bị ghi lỗi không chắc là hãng gây trễ; điều phối thấy cả hai hãng đều có kiện trễ. | Một hãng 12 tài xế nhận 4 lỗi trong một ngày, sát ngưỡng tạm ngưng. |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | Khác: ghi theo kiện tracking (cổng chặn/sửa). | Trao quyền kiểm soát cho người: chuyển người duyệt trước mọi lệnh ghi. | Trao quyền cho người: từ lỗi thứ 3 trong ngày chờ người duyệt. |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | Lệnh ghi chỉ chạy khi tracking xác nhận kiện trễ; không cần người. | Ticket vào hàng chờ chị Hạnh (`NV-HANH`) → hỏi khách kiện nào hoặc đối chiếu tracking → ghi lỗi đúng hãng → báo khách. | Lệnh ghi lỗi bị bỏ; `NV-TUNG` xem chỉ số, `NV-HANH` quyết ghi hay không → thông báo hãng. |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | `ambiguous_fault_rate` (ghi lỗi khi ticket không nói kiện, nhiều hãng trễ). | `ambiguous_fault_rate`. | `carrier_fault_concentration` (số lỗi/hãng/ngày nhiều nhất). |

Yêu cầu: ít nhất **hai lỗi có nguồn khác nhau** ở phần 2, và ít nhất một lỗi được xếp đúng là **lỗi chìm**.

---

<a id="c3"></a>

## C3 · Câu 3.1 · Phần riêng theo thẻ (chỉ điền phần của số đã bốc; làm trong khoảng 5 phút)

| Thẻ | Điền phần nào |
|---|---|
| S1 | Mục C1 (đối chiếu pre-mortem) + **C3.5** (mở lại bản đồ dữ liệu: các trường của `parcel`) |
| S2 | **C3.1** Mức kiểm soát của con người |
| S3 | Mục C1 + **C3.5** (bảng `policies`: trường nào là nguồn sự thật về "phiên bản đang hiệu lực"; dòng `delay_cause`) |
| S4 | Mục C1 + mục **Giờ cao điểm** ở Phiếu B mục B7.6 (bổ sung bằng bút khác màu nếu đã viết) |
| S5 | Mục C1 + **C3.5** + mục **C8** dùng cho một con số kinh doanh (chi phí mỗi ticket theo kho) |
| S6 | **C3.2** Hình dung của người và của hệ thống |
| S7 | **C3.3** Hiệu chỉnh lòng tin (người đặt hàng, người nhận hàng) |
| S8 | **C3.4** Hiệu chỉnh lòng tin (nhân viên duyệt, trưởng ca đứng tên) + **một dòng** "hoàn trên hạn mức" ở bảng C3.1 Bước 2 |

### C3.1 · Mức kiểm soát của con người ở từng lệnh ghi (S2; S8 chỉ một dòng)

**Cách làm:** (1) soát các dấu hiệu cho thấy con người **cần giữ nhiều quyền kiểm soát hơn**; (2) lập bảng
*ai · ở việc nào · cần mức kiểm soát nào* (thấp / vừa / cao / chưa rõ), thêm một cột: **hệ thống hiện đang cho mức nào**.
Chỗ hai cột lệch nhau chính là nơi đặt gate.

**Bước 1 · Dấu hiệu cần nhiều quyền kiểm soát hơn (đánh dấu, ghi bằng chứng từ thẻ)**

| Dấu hiệu | Có? | Bằng chứng trong thẻ / data |
|---|---|---|
| Việc này đụng tới lĩnh vực nhạy cảm: tiền, quan hệ kinh doanh với đối tác | | |
| Hệ trọng cao và cách làm bằng AI còn mới với người liên quan: họ muốn nắm quyền lúc đầu để xây lòng tin | | |
| Hệ thống còn lâu mới đạt độ chính xác mong muốn; quyền của con người là biện pháp tạm trong lúc chờ | | |
| Giới hạn hoặc lỗi của hệ thống cần con người sửa lại | | |
| Hoàn cảnh thay đổi khiến con người phải "đặt lại" hoặc "tiếp quản" (phê duyệt hết hạn, bị thu hồi; chính sách đổi) | | |

**Bước 2 · Bảng mức kiểm soát**

| Ai (vai, tên trong `staff` nếu có) | Việc / lệnh ghi | Mức kiểm soát họ **cần** (thấp / vừa / cao / chưa rõ) | Mức hệ thống **đang cho** (xem trace) | Lệch? |
|---|---|---|---|---|
| | `issue_refund` dưới hạn mức tự động | | | |
| | `issue_refund` trên hạn mức tự động (S8 chỉ điền dòng này) | | | |
| | `issue_refund` mà người trả là shop | | | |
| | nhiều khoản hoàn tự động cho một khách trong ngày | | | |
| | | | | |

→ Mỗi dòng "Lệch" là một nhánh của fault tree và một ứng viên cho gate. Ghi rõ gate **trả quyền về cho ai** (chuyển người
duyệt, chờ duyệt, trần).

**Ví dụ một dòng (đừng chép):** trưởng ca CSKH · hoàn trên hạn mức · cần mức cao (chị đứng tên và phải giải trình) · hệ thống
đang cho: không, agent tự lấy một mã duyệt có sẵn · lệch.

### C3.2 · Hình dung của người và hình dung của hệ thống (S6)

**Cách làm:** thảo luận theo nhóm rồi ghi cho **từng nhóm người dùng**: họ là ai, mục tiêu chính là gì, và hiện
nay họ làm việc này **từng bước ra sao**, đồng đều hay mỗi nơi một kiểu. Dòng cuối: **hệ thống đang mang hình dung nào**, đọc từ trace.

| | Nhóm A: `điều phối và tài xế hãng vận chuyển (ví dụ trưởng nhóm tài xế Sông Hồng)` | Nhóm B: `kế toán đối soát (chị Oanh, NV-OANH)` |
|---|---|---|
| Họ là ai, chạm vào kết quả của trợ lý ở đâu | Nhận thông báo lỗi giao trễ qua `notify_carrier`; thưởng chuyên cần của tài xế tính theo số lỗi. | Đối soát sổ cái `ledger` và bảng `faults` mỗi tuần với 5 hãng và các shop. |
| Mục tiêu chính của họ | Không bị phạt và mất thưởng cho kiện mình giao đúng hẹn. | Mỗi khoản hoàn và mỗi dòng phạt khớp một kiện trễ có nguyên nhân hợp lệ; không phải đòi hoặc hoàn lại hãng. |
| Hiện nay họ xác định "ai chịu lỗi giao trễ" theo các bước nào | Mở sổ giao của hãng, tìm kiện (`parcel_id`) trễ, xem tài xế và ngày quét; nếu hai hãng cùng trễ thì hỏi khách hoặc điều phối bên kia. | Lấy dòng `faults`, đối chiếu tracking theo từng kiện và `delay_cause`, rồi chia lỗi theo hãng của kiện đó. |
| Cách làm đó đồng đều hay mỗi nơi một kiểu | Đồng đều ở đơn vị (theo kiện), mỗi hãng một kiểu sổ ghi. | Theo kiện, nhưng không đồng đều khi một đơn có hai hãng cùng trễ: thường phải hỏi lại. |
| Theo hình dung của họ, **đơn vị chịu lỗi** là gì (đơn / kiện / chặng / tài xế)? | **Kiện** (và tài xế đã chở kiện). | **Kiện.** |

**Hệ thống đang mang hình dung nào?** (đọc trace một ticket hỏng: `tracking.parcels` so với dòng `file_carrier_fault`)

- Với hệ thống, đơn vị chịu lỗi là: **đơn** (hãng của kiện đầu tiên, `parcels[0]`; comment trong `agent.py`: "order-level carrier = carrier of the first parcel"). Bằng chứng: ticket `S6-01@11`, dòng trace: `file_carrier_fault ... parcel_id: O-2601-P1, carrier_id: GHSH` trong khi `tracking.parcels` cho P1 trễ 0 ngày.
- Chỗ hai hình dung vênh nhau: **đơn so với kiện.** Người chịu hậu quả đếm theo kiện, hệ thống đếm theo đơn nên lỗi chạy theo đơn tới hãng của kiện đầu, và lệch cả số ngày (`delay_days` của kiện kia).
- Khi đầu vào không đủ để áp hình dung của con người (không biết kiện nào), hệ thống đang làm gì: **đoán** (lấy kiện đầu, hoặc kiện trễ nhất, rồi ghi lỗi và hoàn tiền ngay; `S6-20@11`, `S6-21@11`); nên làm gì: **không đoán, chuyển người xác định kiện trước mọi lệnh ghi** (cổng A trong `pre_guard`).

→ Mỗi chỗ vênh là một nhánh của fault tree. Gate tốt làm cho hệ thống hành xử theo hình dung của người chịu hậu quả.

### C3.3 · Hiệu chỉnh lòng tin · người đặt hàng và người nhận hàng (S7)

**Cách làm:** đặt ba mốc trên một trục: **không tin · tin vừa đủ · tin quá mức**. Với từng nhóm người, nghĩ ra
một tình huống đẩy họ về mỗi mốc, rồi ghi hai thứ làm lòng tin lệch: **dữ liệu của hệ thống** có liên quan, và **điều người đó
biết hay không biết**. Mục tiêu là lòng tin khớp với việc hệ thống thực sự làm. Người nhận hàng không dùng hệ thống, không ký gì với LogiX.
Chỉ cần hai mốc có trong thẻ; mốc còn lại để trống nếu không có bằng chứng.

| Mốc | Nhóm | Tình huống cụ thể (lấy từ thẻ / ticket) | Dữ liệu của hệ thống liên quan (trường nào, đi tới đâu) | Điều người đó biết / không biết |
|---|---|---|---|---|
| **Tin quá mức** | người đặt hàng | | | |
| **Tin quá mức** | người nhận hàng | | | |
| **Không tin** (sau sự cố) | người nhận hàng | | | |
| **Tin vừa đủ** (trạng thái muốn tới) | cả hai | | | |

**Rút ra:**
- Dữ liệu nào rời hệ thống mà người liên quan **không biết** là nó rời đi: `__________` → tới `__________`.
- Để lòng tin khớp thực tế, có hai đường: **giải thích** cho người dùng dữ liệu đi đâu, hoặc **làm cho hệ thống chỉ làm đúng
  điều người ta tưởng**. Với người nhận hàng (không có kênh nào để giải thích), đường khả thi là: `__________`.
- Biện pháp đó là giảm khả năng lộ hay bảo đảm không lộ: `__________`.

### C3.4 · Hiệu chỉnh lòng tin · nhân viên duyệt và trưởng ca đứng tên (S8)

Cùng cách làm như C3.3. Mốc "tin quá mức" là trước kiểm toán, mốc "không tin" là sau kiểm toán.

| Mốc | Nhóm | Tình huống cụ thể (lấy từ thẻ / ticket) | Dữ liệu của hệ thống liên quan (trường nào, đi tới đâu) | Điều người đó biết / không biết |
|---|---|---|---|---|
| **Tin quá mức** (trước kiểm toán) | nhân viên duyệt | | | |
| **Tin quá mức** (trước kiểm toán) | trưởng ca đứng tên | | | |
| **Không tin** (sau kiểm toán) | nhân viên duyệt | | | |
| **Không tin** (sau kiểm toán) | trưởng ca đứng tên | | | |
| **Tin vừa đủ** (trạng thái muốn tới) | cả hai | | | |

**Rút ra:**
- Dữ liệu nào của hệ thống làm lòng tin lệch: `__________`.
- Để người duyệt thôi kiểm tay từng quyết định, họ cần **thấy** gì ở mỗi quyết định, cần **giữ quyền** ở đâu, và
  tỉ lệ kiểm mẫu nào hai bên chấp nhận: `__________`. Ghi các con số đó vào `config/operating_gates.json` mục `operations`.
- Kèm **một dòng** "`issue_refund` trên hạn mức tự động" ở bảng C3.1 Bước 2.

### C3.5 · Mở lại bản đồ dữ liệu (S1, S3, S5; viết bằng bút khác màu)

Mở lại Phiếu B mục B3. Ghi ở đây những dòng đổi so với vòng 1:

| Trường / bảng | Vòng 1 bàn đã coi là (nguồn sự thật / bản sao / chưa hỏi) | Sau khi đọc thẻ thì thấy | Ảnh hưởng tới tiền hay lỗi hãng thế nào |
|---|---|---|---|
| | | | |
| | | | |

---

<a id="c4"></a>

## C4 · Câu 3.1 · HAZOP của thẻ (ít nhất 3 dòng, viết bằng dữ kiện của thẻ)

*Mục riêng, không ghi đè HAZOP vòng 1 ở Phiếu B mục B4. Năm guideword và nghĩa của chúng: xem Phiếu B mục B4.*

Tool chọn phân tích: `file_carrier_fault` *(kéo theo `notify_carrier`)*

| Tham số / dòng dữ liệu | Guideword (WRONG / INVALID / INCOMPLETE / PERTURBED / INCAPABLE) | Lệch cụ thể (mã ticket, trường dữ liệu của thẻ) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| `parcel_id`, `carrier_id` (chọn kiện ghi lỗi) | WRONG | `S6-01`: ticket có `parcel_id: O-2601-P2` nhưng `agent.py` ghi lỗi cho `parcels[0]` (GHSH, trễ 0 ngày). | GHSH bị ghi lỗi oan, tài xế mất thưởng. | Cổng 2 vòng 1 (sửa về kiện theo tracking); sửa được khi ticket có `parcel_id`. | Đã có (vòng 1): `write_gate` `file_carrier_fault` dùng `H.ticket_parcel` và `H.carrier_at_fault`. Tầng chặn. |
| `parcel_id` của ticket | INCOMPLETE | `S6-20`, `S6-21`: ticket không có `parcel_id`; đơn có hai kiện của hai hãng cùng trễ (GHSH 3 ngày, VNX 5 ngày; DNB 4 ngày, MKD 4 ngày nhưng `FORCE_MAJEURE`). | Một trong hai hãng bị ghi oan; LogiX hoàn tiền trên căn cứ đoán (26.000đ, 28.000đ). | Cổng 2 vòng 1 chọn kiện trễ nhất: vẫn là **đoán**, không đỡ được. | **Mới:** `pre_guard` chuyển người khi không có `parcel_id` và ≥ 2 kiện của hãng khác nhau cùng trễ. Tầng chặn, trước mọi lệnh ghi. |
| Số lỗi đã ghi hôm nay của hãng (dòng dữ liệu `faults`) | WRONG | *(Nhánh bàn chưa thấy trên trace đầu tiên)* `S6-40` đến `S6-43`: lỗi thứ 3 và thứ 4 của GHSH trong ngày; `ops_limits.max_auto_strikes_per_carrier_per_day = 2`; hãng bị tạm ngưng ở 3 lỗi/7 ngày. | GHSH bị tạm ngưng, đứt tuyến nội thành Hà Nội. | Chưa có; `write_gate` không đếm lỗi. | **Mới:** `write_gate` bỏ lệnh ghi lỗi khi `len(fault_rows(carrier_id)) >= cap`. Tầng giới hạn thiệt hại. |
| `delay_cause` của kiện | INVALID | `S6-04`: kiện VNX trễ do `FORCE_MAJEURE` (mưa bão); từ 01/12/2026 REFUND-v4 không ghi lỗi hãng khi bất khả kháng. | Hãng bị phạt cho việc ngoài tầm kiểm soát. | Cổng 2 vòng 1: `carrier_at_fault` chặn nếu nguyên nhân ngoài `fault_causes` của chính sách hiệu lực. | Đã có; giữ. Tầng chặn. |

Bắt buộc: ít nhất ba dòng, trong đó **một dòng là nhánh bàn chưa thấy trên trace** lúc viết.

---

<a id="c5"></a>

## C5 · Câu 3.2, 3.3 · Specification và giả định môi trường

### Câu 3.2 · Một specification mà nếu bị vi phạm thì gây ra tác hại trên thẻ

Kiểm được bằng code hoặc bằng một con số trong report: **"Lỗi giao trễ chỉ ghi cho đúng hãng của kiện đang trễ theo tracking; nếu không xác định được kiện nào thì không ghi mà chuyển người; một hãng không nhận quá `max_auto_strikes_per_carrier_per_day` (2) lỗi tự động trong một ngày."** Con số: `wrongful_carrier_faults` = 0 trên gói S6.

Kiểm bằng gì (hàm trong `guards.py`, dòng report nào): `write_gate` nhánh `file_carrier_fault` (`H.carrier_at_fault`, `H.ticket_parcel`, đếm `ctx.tools.fault_rows`), `pre_guard` (nhánh `ambiguous_parcel`); dòng report `wrongful_carrier_faults`, `pháp lý: lỗi ghi oan cho hãng`, chỉ số `carrier_fault_concentration` và `ambiguous_fault_rate`.

### Câu 3.3 · Một giả định về môi trường mà người thiết kế đã ngầm tin, nhưng nhiều khả năng sai ngoài thực tế

Giả định (thứ nằm NGOÀI phần mềm): **một đơn hàng do một hãng giao, nên "hãng của đơn" là hãng của kiện đầu tiên; và khách luôn nói (hoặc hệ thống luôn biết) kiện nào bị trễ.**

Vì sao có thể sai: LogiX có đơn tách kiện giao bởi nhiều hãng (`O-2601`, `O-2620`, `O-2621`), kiện đến lệch nhau vài ngày; khách thường chỉ nói "đơn giao chậm" mà không biết mã kiện. Và nhập tay ở điểm phát có thể làm `delay_cause` hoặc ngày giao của từng kiện sai.

---

<a id="c6"></a>

## C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa (mã lần chạy: `R-S6-before-20261118-171120-683190`)

**Khung tư duy.** Đi từ **tác hại** ngược về nguyên nhân, không đi từ lỗi mình tình cờ thấy. Mỗi tầng hỏi "điều gì phải xảy
ra thì điều trên mới xảy ra", nối bằng **HOẶC** (một trong các nhánh là đủ) hoặc **VÀ** (phải đồng thời). Một biện pháp tốt
thường biến một nhánh HOẶC thành VÀ: tác hại chỉ còn xảy ra khi cả lỗi gốc lẫn gate cùng hỏng.

**Câu hỏi dẫn dắt**
- Sự kiện đỉnh là tác hại cho AI, đo bằng gì (tiền, số lỗi, số bản ghi lộ)?
- Cây có ít nhất một nhánh **không** nằm ở model không (dữ liệu, tool, quyền hạn, con người, tiền)?
- **Specification** nào của phần mềm bị vi phạm ở mỗi lá? **Giả định về môi trường** nào (thứ nằm ngoài phần mềm) đã sai?
- Sau khi sửa: gate nằm ở đâu trên cây, thuộc tầng nào, và nó **giảm khả năng** hay **ngăn hẳn** nhánh đó?

Ít nhất hai nhánh ở hai tầng khác nhau (kỹ thuật, kinh doanh, con người); mỗi lá có bằng chứng (ticket@seed, trường dữ liệu, hoặc một dòng của report).

```
[ĐỈNH] Tác hại: hãng nhỏ (GHSH, DNB) bị ghi lỗi giao trễ của hãng khác, tài xế mất thưởng (cho ai: hãng và tài xế; đo bằng: wrongful_carrier_faults = 40 và hoàn sai 270.000đ trên gói S6, mốc base)
 └─ HOẶC
 ├─ [1] Lỗi ghi theo ĐƠN (hãng của kiện đầu), không theo KIỆN              tầng: hành động (tool ghi)
 │   └─ vì: agent.py lấy `parcels[0]`, bỏ qua `ticket.parcel_id`          bằng chứng: ticket S6-01@11, S6-02, S6-03, S6-04
 ├─ [2] Ticket không nói kiện nào, hai hãng cùng trễ, hệ thống đoán         tầng: đầu vào / data
 │   └─ vì: không có điểm dừng "không đủ căn cứ" trước lệnh ghi            bằng chứng: ticket S6-20@11, S6-21@11
 └─ [3] Không có trần lỗi theo hãng theo ngày: lỗi cộng dồn                  tầng: vận hành / quyền hạn
     └─ vì: mỗi ticket đúng riêng lẻ nhưng tổng 4 lỗi/ngày cho GHSH         bằng chứng: S6-40 đến S6-43; carrier_fault_concentration = 4,0
```

| Lá | Specification bị vi phạm (phần mềm phải làm gì) | Giả định môi trường đã sai (thế giới ngoài phần mềm) |
|---|---|---|
| [1] | Lỗi hãng phải ghi cho `parcel_id` và hãng của kiện trễ theo tracking, không theo kiện đầu của đơn. | "Một đơn do một hãng giao." |
| [2] | Khi không xác định được kiện, không ghi lỗi, không hoàn tiền trên căn cứ đoán; chuyển người. | "Khách luôn nói được kiện nào trễ; nếu không thì kiện trễ nhất là kiện đúng." |
| [3] | Một hãng không nhận quá 2 lỗi tự động/ngày; từ lỗi thứ 3 phải có người duyệt (`ops_limits`). | "Số lỗi thật của một hãng trong ngày luôn ít, nên không cần đếm cộng dồn." |

**Ví dụ mẫu một nhánh (bộ nền, đừng chép):** đỉnh "hãng VNX nhận lỗi oan cho đơn O-1002" ← [1] agent dùng độ trễ 5 ngày ←
model lấy số trong ticket đè lên DB (`T-002@55`). Spec bị vi phạm: độ trễ dùng để ghi lỗi phải lấy từ tracking DB. Giả định
môi trường sai: "khách ghi đúng số ngày trễ". Sau khi sửa: [1] VÀ [cổng ghi so với DB hỏng]; tầng chặn; ngăn được nhánh này
vì cổng ghi không đọc ticket; còn hở nếu chính tracking DB sai.

---

<a id="c7"></a>

## C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn

Sửa NGOÀI model, đúng chỗ cho từng nguyên nhân. Code: `lab10/guards.py` (`pre_guard`, `write_gate`). Con số và quy trình:
`config/operating_gates.json` (phạm vi, người trực, trần, ngân sách, kiểm mẫu, ghi chú giải thích, cổng pháp lý). Rồi chạy:

```bash
python3 -m lab10.eval --suite Sx --stage after --note "đổi MỘT thứ: ..."
python3 -m lab10.grade --incident Sx
```

| Nhánh fault tree | Nguyên nhân | Chỗ sửa (hàm + nhánh trong `guards.py`, hoặc khoá trong `operating_gates.json`) | Tầng (phát hiện / chặn / giới hạn thiệt hại / vận hành) | GIẢM khả năng hay NGĂN hẳn? Vì sao | Mã lần chạy sau khi sửa |
|---|---|---|---|---|---|
| [1] | Ghi lỗi theo đơn (`parcels[0]`), không theo kiện | `write_gate`, nhánh `file_carrier_fault`: `deny` nếu `not H.carrier_at_fault(...)`, `modify` về đúng `parcel_id`, `carrier_id`, `driver_id`, `delay_days` theo `H.ticket_parcel` (đã có từ vòng 1, mốc prepared) | Chặn | **NGĂN** khi ticket có `parcel_id` và tracking đúng: cổng ghi không đọc chữ khách. Còn hở nếu tracking hoặc `parcel_id` trong ticket sai. | `R-S6-prepared-20261118-171120-683190` (đã đỡ một phần), sau cùng `R-S6-after-20261118-170347-683190` |
| [2] | Không đủ căn cứ biết kiện nào, hệ thống đoán | `pre_guard`: `escalate` khi ticket không có `parcel_id` và ≥ 2 kiện của hãng khác nhau cùng trễ (`H.db_delay_days > 0`); dừng trước mọi lệnh ghi, kể cả hoàn tiền | Chặn, trước lệnh ghi đầu tiên | **NGĂN** trường hợp đúng điều kiện; **không** bắt trường hợp khách nói kiện bằng chữ mà không có `parcel_id` (cần người đọc). Đẩy việc sang người nên tăng hàng chờ (S6: 0,0833 → 0,25). | `R-S6-after-20261118-170307-779ee5` |
| [3] | Không có trần lỗi theo hãng theo ngày | `write_gate`, nhánh `file_carrier_fault`: `deny` khi `len(fault_rows(carrier_id)) >= ops_limits.max_auto_strikes_per_carrier_per_day`; ghi `ctx.log("carrier_strike_cap")` | Giới hạn thiệt hại | **GIẢM**: chặn lỗi thứ 3 trở đi nhưng chỉ bỏ lệnh ghi, không đưa ticket vào hàng chờ; lỗi đúng có thể bị bỏ sót (hãng được lợi) cho tới khi người nhìn chỉ số `carrier_fault_concentration`. | `R-S6-after-20261118-170307-779ee5` |

**Lưu ý chọn đúng chỗ sửa:** không sửa `config/operating_gates.json` lần này. Cổng pháp lý đã đặt ở vòng 1; trần theo hãng đã có sẵn ở `ops_limits` (nguồn Ops/Finance) nên chỉ cần đọc, không đặt thêm con số mới.

---

<a id="c8"></a>

## C8 · Câu 3.6 · Chỉ số theo dõi mới (thước đo → dữ liệu → cách tính)

Thêm **ít nhất một hàm** trong `lab10/monitors.py` và đăng ký vào `MONITORS`. Chỉ số `escalation_rate` có sẵn không tính là chỉ số mới.
Thẻ S5 dùng mục này cho một con số kinh doanh: chi phí mỗi ticket theo kho (tách tiền máy, công người, tiền mất).

| | Chỉ số theo dõi mới của bàn |
|---|---|
| **Tên trong `MONITORS`** | `carrier_fault_concentration` (chính) và `ambiguous_fault_rate` (phụ) |
| **Bước / hành vi được đo** | Bước ghi lỗi hãng (`file_carrier_fault`): hãng nào bị ghi dồn, và ghi lỗi khi chưa biết kiện nào. |
| **Thước đo** (một câu, có đơn vị) | (1) Số lỗi tự động nhiều nhất mà một hãng nhận trong một ngày vận hành (lỗi/hãng/ngày). (2) Tỉ lệ lần ghi lỗi hãng mà ticket không nói kiện, nhưng đơn có ≥ 2 kiện của hãng khác nhau cùng trễ (%). |
| **Dữ liệu** (trường nào của trial, không có nhãn) | `events` (sự kiện `tool` với `tool == file_carrier_fault`, `carrier_id`; sự kiện `tracking.parcels[].delay`), `seed`, `day`, `ticket.parcel_id`. Không dùng nhãn. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | (1) max trên (seed, day, carrier) của số lệnh `file_carrier_fault`; 0 nếu không có lệnh ghi. (2) số trial có ghi lỗi hãng, không có `parcel_id` và ≥ 2 kiện của hãng khác nhau cùng trễ, chia cho số trial có ghi lỗi hãng; trial thiếu sự kiện `tracking` bị bỏ khỏi tử số; mẫu số 0 thì trả 0,0. |
| **Khung thời gian / ngưỡng báo động** | Tính theo ngày và theo cửa sổ 1 giờ. (1) **> 2** (trần `ops_limits`) báo ĐỎ cho `NV-TUNG`; **= 2** báo VÀNG. (2) **> 0** báo ĐỎ: có ca ghi lỗi theo cách đoán. |
| **Điểm mù** (chỉ số này KHÔNG thấy gì) | Không biết lỗi đã ghi đúng hay oan; không thấy ca khách nói kiện bằng chữ mà ticket thiếu `parcel_id`; số theo ngày giả lập không phản ánh tuần (ngưỡng tạm ngưng tính theo 7 ngày). |
| Giá trị trên bộ nền · trên thẻ (đọc mục `monitor` của report) | `carrier_fault_concentration`: bộ nền **1,0** · S6 trước sửa **4,0** · S6 sau sửa **2,0**. `ambiguous_fault_rate`: bộ nền **0,0** · S6 trước sửa **0,1667** · S6 sau sửa **0,0**. Grade kiểm 6 `monitor`: ✅. |

---

<a id="c9"></a>

## C9 · Câu 3.7 · Fault tree SAU khi sửa (mã lần chạy: `R-S6-after-20261118-170347-683190`)

Vẽ lại cây ở C6. Ở mỗi nhánh đã xử lý, thêm một nút `VÀ [gate … hỏng]` và ghi:

```
[ĐỈNH] Hãng nhỏ bị ghi lỗi giao trễ của hãng khác (wrongful_carrier_faults: 40 → 0 trên gói S6 nhìn thấy)
 └─ HOẶC
 ├─ [1] Ghi theo đơn (parcels[0])                       VÀ [write_gate file_carrier_fault hỏng]
 ├─ [2] Ticket không nói kiện, hai hãng cùng trễ         VÀ [pre_guard ambiguous_parcel hỏng]
 └─ [3] Dồn lỗi theo hãng trong ngày                     VÀ [write_gate carrier_strike_cap hỏng]  (còn hở: lỗi đúng bị bỏ sót)
```

| Nhánh | Gate (hàm trong `guards.py` / khoá config / metric trong `monitors.py`) | Tầng gate (phát hiện / chặn / giới hạn thiệt hại / vận hành) | Giảm hay ngăn? Vì sao | Nhánh còn hở |
|---|---|---|---|---|
| [1] | `write_gate` nhánh `file_carrier_fault` (`carrier_at_fault`, `ticket_parcel`); metric `ambiguous_fault_rate` | Chặn; metric là phát hiện | Ngăn: cổng đọc tracking, không đọc chữ khách | Tracking sai, `parcel_id` trong ticket sai |
| [2] | `pre_guard` nhánh `ambiguous_parcel`; metric `ambiguous_fault_rate` | Chặn trước lệnh ghi; metric phát hiện | Ngăn với ticket thiếu `parcel_id` | Khách nói kiện bằng chữ không có mã; hai kiện cùng hãng; hàng chờ tăng |
| [3] | `write_gate` nhánh `carrier_strike_cap`; metric `carrier_fault_concentration` | Giới hạn thiệt hại; metric phát hiện | Giảm: bỏ lệnh ghi lỗi từ lỗi thứ 3, không đưa người vào | Lỗi đúng bị bỏ sót; chưa tính cửa sổ 7 ngày (chỉ theo ngày) |

---

<a id="c10"></a>

## C10 · Câu 3.7 · Risk register (thêm ít nhất 1 dòng sau sự cố)

| Rủi ro | Khả năng | Tác động | Người phụ trách (PIC, một người) | Dấu hiệu (metric nào, ngưỡng nào) | Xử lý | Ảnh hưởng bước đánh giá | Nhóm chức năng (GOVERN / MAP / MEASURE / MANAGE) |
|---|---|---|---|---|---|---|---|
| Khách nói kiện bằng chữ ("kiện thứ hai") nhưng ticket không có `parcel_id`, nên cổng A không nhận ra và trợ lý vẫn đoán | Vừa | Cao: hãng nhỏ bị ghi oan, tài xế mất thưởng | Lê Thanh Tùng (`NV-TUNG`) | `ambiguous_fault_rate` > 0; thêm tỉ lệ ticket không có `parcel_id` trong pilot | Giữ `escalate` cho đơn nhiều hãng cùng trễ; đo tỉ lệ ticket thiếu `parcel_id` ở 2 depot; nếu cao thì thu hẹp phạm vi sang đơn một kiện | Đổi quyết định: nếu tỉ lệ cao thì Thu hẹp thay vì Tiếp tục | MEASURE |
| Cổng trần lỗi theo hãng chỉ `deny`: lỗi đúng của hãng bị bỏ sót, LogiX chịu thay và kế toán lệch sổ | Vừa | Vừa: tiền hãng phải chịu rơi vào LogiX | Phạm Kiều Oanh (`NV-OANH`) | `carrier_fault_concentration` ≥ 2 trong ngày | Cuối ngày `NV-OANH` rà các lỗi bị bỏ; cân nhắc đổi `deny` thành đưa vào hàng chờ duyệt khi có công suất | Có thể đổi `deny` thành `escalate`, ảnh hưởng chi phí và hàng chờ | MANAGE |

Quy tắc: **mỗi dòng phải đổi được một quyết định.** Cột "Dấu hiệu" phải là một metric có trong `monitors.py` hoặc trong report.

---

<a id="c11"></a>

## C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5

### Cập nhật checklist (bảng gốc ở Phiếu B mục B5)

Ghi các dòng đổi sau sự cố. Mỗi dòng vẫn phải có một PIC có tên.

| # nhóm | Trạng thái mới (Xong / Chưa / Không áp dụng) | Bằng chứng mới (mã lần chạy, mục phiếu, số trong report) | PIC |
|---|---|---|---|
| 1 Chất lượng | Xong trên bộ nền và gói S6 nhìn thấy; **chưa đo** bài kiểm tra ẩn | Bộ nền `R-base-after-20261118-170348-683190` (110/110, pass_k 1,0); S6 `R-S6-after-20261118-170347-683190` (60/60) | Nguyễn Hoàng Cương |
| 4 Quyền hạn | Xong cho lệnh ghi lỗi hãng (`write_gate`, `pre_guard`) | Phiếu C mục C7; `grade` kiểm 3 `visible` ✅ | Vũ Trọng Quang |
| 7 Vận hành | Xong thêm hai chỉ số, còn thiếu cảnh báo tự động | `carrier_fault_concentration`, `ambiguous_fault_rate` (mục C8); grade kiểm 6 `monitor` ✅ | Nguyễn Đức Đạt |
| 8 Con người, pháp lý | Xong cho hãng: 0 lỗi oan trên gói S6; còn rủi ro nói kiện bằng chữ | `pháp lý: lỗi ghi oan cho hãng` 40 → 0; mục C10 | Nguyễn Đức Đạt |

### Runbook 4 · Sau sự cố trên thẻ (vòng 2)

| Câu hỏi | Trả lời |
|---|---|
| Tín hiệu nào ở Runbook 2 (Phiếu B mục B7.5) lẽ ra phải báo trước sự cố này? Nó đã có chưa? | Dòng "Lỗi ghi oan cho hãng" (ngưỡng ĐỎ ≥ 1) có, nhưng chỉ nhìn tổng, không nhìn **theo hãng**: **chưa có** tín hiệu "số lỗi/hãng/ngày" nên dồn lỗi cho GHSH không báo đỏ. Nay có `carrier_fault_concentration`. |
| Bàn thêm hoặc đổi ngưỡng nào, từ bao nhiêu thành bao nhiêu? | Thêm dòng Runbook 2: `carrier_fault_concentration` VÀNG = 2, ĐỎ > 2 (từ chưa có); `ambiguous_fault_rate` ĐỎ > 0 (từ chưa có). Không đổi ngưỡng đã ký. |
| Bàn đổi gì về **người** (số người trực, ai đứng tên, ai được gọi)? | Giữ 1 người trực (`reviewers_on_shift = 1`). Thêm: `NV-HANH` nhận ca "nhiều hãng cùng trễ" (S6: tỉ lệ chuyển người 0,0833 → 0,25, vẫn dưới công suất 6 ca/giờ); `NV-OANH` rà lỗi bị bỏ cuối ngày. |
| Bàn đổi gì về **phạm vi** hoặc **quy trình** (kiểm mẫu, ghi chú giải thích, trần)? | Quy trình: đơn tách kiện nhiều hãng cùng trễ và ticket không nói kiện thì luôn qua người. Trần: dùng `ops_limits` có sẵn, 2 lỗi/hãng/ngày. Không đổi `pilot_scope` (giữ 100%). |
| Nói gì với bên thứ ba bị ảnh hưởng (hãng, shop, người nhận, nhân viên duyệt), ai nói, trong bao lâu? | Với GHSH và DNB: xin lỗi, liệt kê các lỗi đã ghi nhầm theo mã kiện, và đề nghị rút lại. `NV-OANH` nói qua kênh đối tác, trong vòng 1 ngày làm việc; `NV-TUNG` báo trưởng nhóm tài xế Sông Hồng. |
| Dữ liệu cá nhân nào đã rời hệ thống mà không thu hồi được? Báo cho ai? | Trong S6 `pii_leaks` = 0 (cổng vòng 1 bỏ `customer_note`, `recipient_contact`). Không có dữ liệu cá nhân nào rời hệ thống ngoài số liệu lỗi và mã kiện cho hãng. |
| Sự cố lộ ra trước qua số máy đo, phản hồi của người, hay đọc nội dung? Nguồn nào bàn chưa có? | Qua **phản hồi của người** (tin nhắn thoại của trưởng nhóm tài xế). Bàn chưa có kênh nhận phản hồi trực tiếp của hãng nhỏ; cần thêm cổng phản hồi của hãng (người đứng tên: `NV-OANH`). |

### Runbook 5 · Ba kịch bản "nếu … thì …" cho tuần đầu chạy thử thật

1. Nếu số ticket tăng gấp **3** lần trong một giờ thì: hàng chờ vượt 4 ca/giờ → `NV-TUNG` gọi người duyệt thứ hai (`reviewers_on_shift` 1 → 2); các đơn "nhiều hãng cùng trễ" vào hàng chờ chị `NV-HANH` trước; nếu chờ > 60 phút thì thu hẹp `pilot_scope`.
2. Nếu nhà cung cấp LLM lỗi quá **15** phút thì: tắt `issue_refund`, `file_carrier_fault`, `notify_carrier` trong `config/switches.json` (`NV-TUNG`, tối đa 5 phút), chuyển ticket sang làm tay; cổng code hiện chưa chặn riêng ca `fail_open` nên phải tắt bằng công tắc.
3. Nếu người duyệt báo không tin một quyết định của trợ lý thì: `NV-HANH` được giữ nguyên quyền duyệt; tạm nâng `review_sampling_pct` từ 10 lên 100 trong ngày, mỗi ca duyệt kèm `decision_note`; `NV-TUNG` ghi ticket vào Risk register và xem lại cổng liên quan.

---

<a id="c12"></a>

## C12 · Quyết định Gate 1 · v2 (phút 185–200)

Quyết định phải khớp bằng chứng và khớp tiêu chí đã ký. Chọn **Tiếp tục** khi report còn dòng vượt trần, hoặc còn ngưỡng đã ký
chưa đạt, là quyết định không đạt. **Thu hẹp**, **Cải tiến thêm**, **Dừng** có lý do và có số thì đều là quyết định đạt.
Cột v1 nằm ở Phiếu B mục B8; không sửa cột đó.

| | **v2** (phút 185–200, SAU sự cố) |
|---|---|
| Commit ký tiêu chí | phải giống v1 |
| Hash chốt cổng vòng 1 | phải giống v1 |
| Mã lần chạy dùng làm bằng chứng | thẻ, mốc base: `R-S6-before-20261118-171120-683190` · prepared: `R-S6-prepared-20261118-171120-683190` · after: `R-S6-after-20261118-171120-683190` (grade `R-S6-grade-20261118-171119-683190`) |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | **Không.** Mốc after: "Không vượt trần kinh doanh / vận hành nào", mọi ngưỡng đã ký đạt. S6: chi phí 5.168đ/ticket (≤ 8.000đ), ROI 0,93, 0 ca ùn, 0 lỗi oan; bộ nền: 4.456đ, ROI 1,24. |
| Kho hoặc hãng có số xấu nhất: ____. Nếu chỉ nhìn phân khúc này, quyết định có đổi không? *(Khối "theo kho và hãng" trong output `lab10.eval` / `lab10.grade`, hoặc mục `by_segment` trong `report.json`.)* | Kho **HCM** trên gói S6: chi phí **5.481đ/ticket** (cao nhất, tăng từ 761đ vì ca chuyển người), vẫn dưới 10.000đ làm tay; chất lượng mọi hãng 1,0. Trên bộ nền, kho "?" vẫn 10.359đ > làm tay (1 ticket, đơn không tìm thấy). Nếu chỉ nhìn HCM, quyết định không đổi. |
| Quyết định (khoanh một) | **Tiếp tục** *(Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng)* |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | `R-S6-after-20261118-171120-683190`: cả 5 chỉ số bắt buộc đạt trên gói S6 nhìn thấy: `pass_rate` 1,0, `pass_k` 1,0, hoàn sai 0đ, lỗi hãng oan 0, lộ PII 0. |
| Bằng chứng 2 | Bộ nền `R-base-after-20261118-170348-683190`: 110/110 đúng, ngưỡng kinh doanh đạt (4.456đ, ROI 1,24, 0 ca ùn); grade kiểm 5 `regression` ✅; grade nói "Mọi ngưỡng đã ký đều đạt", "Được phép cân nhắc Tiếp tục". |
| Bằng chứng 3 | Trước/sau: S6 base 40 lỗi oan và 270.000đ hoàn sai → after 0 và 0đ; grade kiểm 6 `monitor` ✅ (`carrier_fault_concentration` 4,0 → 2,0). |
| Khớp dòng nào trong `decision_rule` đã ký? | Dòng **Tiếp tục** ("Mọi ngưỡng required và business_ops đạt trên bộ nền và gói sự cố được giao"). |
| Nếu Thu hẹp: cắt kho nào / còn bao nhiêu phần trăm / mấy người trực, và ticket bị cắt đi đâu | Không áp dụng. Nếu pilot thật cho thấy nhiều ticket thiếu `parcel_id`, thu hẹp sang đơn một kiện (xem Risk register). |
| Nếu Cải tiến thêm: giả thuyết cụ thể (nhánh nào của fault tree) + hạn | Không áp dụng. |
| Nếu Dừng: bài học ghi lại | Không áp dụng. |
| Ngày quyết định lại (trừ khi Dừng) | **19/11/2026 (GMT+7)**, theo tiêu chí đã ký, trước khi mở pilot thật. |
| PIC ký | Nguyễn Triều Dương (Sản phẩm và kinh doanh, người ký tiêu chí); PIC vận hành Lê Thanh Tùng (`NV-TUNG`). |

**Chỉ ở v2**
- Quyết định đổi hay giữ so với v1? **Giữ Tiếp tục.** Vì số: S6 từ 40 lỗi oan và 270.000đ hoàn sai (base) về 0 và 0đ (after), bộ nền không thụt lùi.
- Report tự kiểm tra: mã lần chạy `R-S6-grade-20261118-171119-683190` · ô nào còn đỏ (nguyên nhân × tầng): **kiểm 1 `integrity` ❌** (kiểm đã báo `incidents/S1` đến `S8` bị đổi vì repo chỉ có `incidents/S6/`; **chưa phải lỗi mã của bàn**, cần Lab Coach phát đủ gói rồi chạy lệnh kéo thẻ); kiểm 4 `hidden`: chưa có trên máy này. Các ô khác ✅.
- Cổng vòng 1 (mốc prepared) đã đỡ được gì trước khi bàn biết sự cố, và bỏ sót gì: đỡ **một nửa**: S6 `pass_rate` 0,3333 → 0,6667 và lỗi oan 40 → 20 (cổng ghi đúng kiện theo tracking, chặn `FORCE_MAJEURE`). Bỏ sót: ticket không nói kiện (`S6-20`, `S6-21`) và trần lỗi theo hãng (`S6-42`, `S6-43`).
- Report ghi "được phép cân nhắc Tiếp tục" hay "không đủ căn cứ"? Report ghi **"Được phép cân nhắc 'Tiếp tục'"** ở mốc after (lần đầu chưa sửa: "KHÔNG đủ căn cứ để chọn Tiếp tục"). Quyết định Tiếp tục của bàn khớp.
- Một thứ bộ thử hôm nay chưa đo, và nó ảnh hưởng quyết định ra sao: bài kiểm tra ẩn (đơn mới, cách viết khác, ví dụ khách nói "kiện thứ hai" không kèm `parcel_id`) và cửa sổ 7 ngày của ngưỡng tạm ngưng; nếu cổng A không bắt được cách viết khác thì quyết định phải đổi sang Thu hẹp.

**Ba dòng bắt buộc** (chép nguyên ba câu này sang `submission/submission.json`, mục `three_lines`)
1. Một giả định về môi trường mà thiết kế của đội đang dựa vào, có thể sai ngoài thực tế: Tracking DB ghi đúng ngày giao và nguyên nhân trễ của từng kiện, và `parcel_id` trong ticket là kiện khách thực sự nói tới; ngoài thực tế điểm phát có thể quét sót hoặc nhập tay sai, và khách thường chỉ nói "đơn giao chậm".
2. Gate của đội chỉ GIẢM khả năng hay thực sự NGĂN được tác hại? Vì sao: Cổng ghi đúng kiện theo tracking và cổng chuyển người khi không xác định được kiện NGĂN được tác hại trong phạm vi dữ liệu đúng (không đọc chữ khách); cổng trần lỗi theo hãng chỉ GIẢM, vì nó bỏ lệnh ghi chứ không đưa người vào, và vẫn hở nếu tracking sai hoặc ticket nói kiện bằng chữ mà không có mã.
3. Vì data là mock, cần đo lại gì trong pilot thật trước Bước đánh giá 2: Tỉ lệ đơn tách kiện có ≥ 2 hãng cùng trễ ở 2 depot, tỉ lệ ticket không có `parcel_id`, số lỗi/hãng/ngày và trong 7 ngày (đặc biệt GHSH, DNB), tỉ lệ hãng phản đối lỗi trong 7 ngày, và chi phí duyệt của kho HCM.
