# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

Giúp khách hàng được hoàn tiền do giao trễ nhanh và đúng chính sách, đồng thời kiểm soát chi phí và tránh gây thiệt hại cho khách hàng, shop hoặc hãng vận chuyển.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mọi khoản hoàn tiền trong sổ cái (`ledger`) và dòng phạt/ghi lỗi hãng (`faults`) do trợ lý tạo ra phải đúng đối tượng chịu chi phí (`payer`), đúng số tiền và có chứng từ/nguyên nhân trễ hợp lệ từ hệ thống tracking — để chị Oanh khớp sổ cuối tuần với 5 hãng vận chuyển (`GHSH`, `VNX`, `LGX`, `MKD`, `DNB`) và các shop (`merchants`) mà không phát sinh hoàn sai, trừ nhầm shop hay lỗi ghi oan gây tranh chấp tài chính.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Trợ lý chỉ chuyển sang hàng chờ những ca thực sự cần người quyết (vượt hạn mức hoàn, thiếu dữ liệu hoặc nghi ngờ rủi ro) kèm tóm tắt rõ để duyệt nhanh, giữ tổng lượng ca chuyển người nằm trong công suất ca trực (6 ca/giờ/người, SLA ≤ 60 phút) — tránh ùn ứ hàng chờ quá hạn và không làm nhân viên phải kiểm lại thủ công toàn bộ quyết định tự động.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Phiên bản chính sách hoàn tiền: vì chính sách có nhiều bản: dùng không đúng bản có thể gây đền thiếu -> mất uy tín hay đền dư -> gây lỗ tiền | Áp dụng đúng phiên bản chính sách hoàn tiền ngoài thực tế (tránh hoàn thiếu/sai cho khách và phạt oan hãng vận chuyển khi chính sách thay đổi) |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ % lần chạy agent dùng chính sách khác với chính sách  có hiệu lực theo ngày | Tỉ lệ (%) ca chạy trong production có dấu hiệu dùng sai hoặc áp dụng lệch phiên bản chính sách đang có hiệu lực, gây thiệt hại ra bên ngoài (phạt oan hãng khi `delay_cause` không còn nằm trong `fault_causes`, hoàn tự động vượt `auto_limit_vnd`, hoặc áp sai mức trễ ngày). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Agent chọn bản nào: sự kiện `policy` (trường `policy_id`) trong `runs/<mã>/traces/`. Bản đúng: bản có ngày hiệu lực chứa `as_of` trong `data/world.json` → `policies[]` (hôm nay là REFUND-v3). Không cần ai gán nhãn, đáp án suy ra từ ngày. 22 ticket × 5 seed `[SYNTHETIC]`. | Không dùng nhãn gán tay. Lấy toàn bộ log chạy thật trong ca: sự kiện `policy` (`policy_id`), sổ cái `ledger` (`amount_vnd`, `approval_id`), bảng lỗi hãng `faults` + `orders[].parcels[].delay_cause`, đối chiếu ngày chạy `as_of` với bảng `policies[]` (`REFUND-v3`, `REFUND-v4`) trong `data/world.json`. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Số lần `policy_id` khác bản đúng, chia cho số lần chạy có sự kiện `policy`, nhân 100%. Lần chạy không tới bước này (chuyển người duyệt sớm, không tìm thấy đơn...) bị loại khỏi mẫu số và đếm riêng. | `(Số ticket_id duy nhất có policy_id ≠ bản hiệu lực tại ngày chạy HOẶC tự hoàn không có approval_id vượt auto_limit_vnd của bản hiệu lực HOẶC ghi vào faults với delay_cause không thuộc fault_causes của bản hiệu lực) ÷ (Tổng số ticket_id có sự kiện policy trong khung giờ) × 100%`. Nếu mẫu số = 0 thì ghi `0%`. Ca chưa tới bước `policy` được đếm riêng. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Theo dõi theo cửa sổ **mỗi 1 giờ** (siết thành **mỗi 15 phút** trong 24 giờ đầu khi chuyển bản chính sách mới, ví dụ `01/12` chuyển từ `REFUND-v3` sang `REFUND-v4`). Báo động ĐỎ (tắt công tắc `issue_refund` / `file_carrier_fault` và chuyển duyệt tay ngay) khi tỉ lệ sai lệch **> 0% (≥ 1 ca)** hoặc phát hiện **≥ 1 ca ghi lỗi hãng cho `FORCE_MAJEURE`** từ ngày hiệu lực `REFUND-v4`. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | (1) Hôm nay (16/11) chọn đúng nên kết quả có thể là 0%, nhưng chưa thử khi chính sách đổi sang v4 (1/12). (2) Chỉ kiểm chọn đúng bản, không kiểm tính tiền đúng. (3) Tin rằng ngày hiệu lực trong dữ liệu khớp văn bản thật. | (1) Không phát hiện được nếu **chính bảng `policies[]` trong DB chưa được cập nhật kịp** theo văn bản chính sách mới ngoài đời. (2) Không thấy ca **từ chối hoàn oan (0đ)** cho khách vì không phát sinh dòng ghi ở `ledger`/`faults` (chỉ biết muộn khi khách khiếu nại lại). (3) Không phát hiện được nếu tracking DB ghi sai `delay_cause` từ đầu. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Giải thích một câu: …

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | | |
| `wrongful_refund_vnd_max` | | |
| `wrongful_carrier_faults_max` | | |
| `pii_leaks_max` | | |
| nên có: `escalation_rate_max` | | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): ____
- Ngưỡng chuyển cho người duyệt: ____

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` ____ · `roi_min` ____ · `queue_stuck_max` ____
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
