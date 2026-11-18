# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `EverNous`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-EverNous-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S6

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Hoàng Cương | 2A202603568 | Kỹ sư cổng | x |
|   2 | Nguyễn Triều Dương | 2A202603524 | Sản phẩm và kinh doanh ||
|   3 | Vũ Trọng Quang | 2A202603535 | Kỹ sư cổng ||
|   4 | Nguyễn Đức Đạt | 2A202603544 | Vận hành và pháp lý ||

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenHoangCuong-2A202603568

### Phần việc phụ trách

**Kỹ sư cổng.** Phần code cổng: `lab10/guards.py`; chạy các mốc và đọc trace. Câu 2.1, 2.2, 2.6, 2.7, chốt cổng vòng 1, thẻ S6 phần sửa cổng (3.5), chạy ba mốc. Phiếu B mục B0 đến B2, B7.1, B7.2; Phiếu C mục C0, C7, C9.

### Đóng góp cụ thể

Vòng 1:
- Chạy mốc base, đọc khối "kinh doanh và vận hành" và "theo kho và hãng"; dò trace `T-002@55` và điền bảng soát lỗi (B1, B2).
- Viết các cổng phòng ngừa trong `write_gate`: tiền hoàn theo tracking và chính sách, lỗi hãng có căn cứ đúng kiện, tin gửi hãng chỉ trường được phép, từ chối nhưng đủ điều kiện (B7.1); nêu hai bước tránh chỉnh trên bộ dùng để chấm (B7.2).
- Chốt cổng vòng 1 bằng `lab10.checkpoint` (`437b79da`) và chạy mốc prepared cho v1.

Vòng 2 (thẻ S6):
- Chạy mốc prepared và đọc những gì cổng vòng 1 đã đỡ được (C0, C1).
- Sửa cổng: `pre_guard` chuyển người khi ticket không nói kiện và nhiều hãng cùng trễ; `write_gate` bỏ lệnh ghi khi hãng đã đủ 2 lỗi tự động trong ngày (C7).
- Chạy lại ba mốc và kiểm không regression trên bộ nền.

### Bằng chứng

Commit `21e48e2` (2.5), `e4349e8` (2.8), `4ff1191`, `b85312c` (lock gate 1), `CP4`. Lần chạy: base `R-base-before-20261118-155125-b45eeb`, prepared `R-base-prepared-20261118-164425-e04e78`; S6 base `R-S6-before-20261118-171120-683190`, prepared `R-S6-prepared-20261118-171120-683190`, after `R-S6-after-20261118-171120-683190`. Dòng trong phiếu: B1, B2, B7.1, B7.2, B8 (hash chốt), C0, C7.

### Exit ticket

Học được: cổng đọc nguồn sự thật (tracking, chính sách) bền hơn cổng đọc chữ khách, và một cổng đúng trên bộ nền vẫn có thể hở ở đơn nhiều hãng. Chưa chắc: cổng chuyển người có bắt được cách viết khác (khách nói "kiện thứ hai" mà không có `parcel_id`) trong bài kiểm tra ẩn hay không.

## VuTrongQuang-2A202603535

### Phần việc phụ trách

**Kỹ sư cổng.** Phần chỉ số theo dõi (`lab10/monitors.py`), ticket hiểm và phân tích lỗi: câu 2.8, thẻ S6 phần 3.1 đến 3.4 và 3.6. Phiếu B mục B7.3; Phiếu C mục C2, C4, C6, C8.

### Đóng góp cụ thể

Vòng 1:
- Dò trace và chọn tính chất cho behavioral test; viết và chạy hai ticket hiểm bằng `--adhoc` (B7.3). Với câu 2.8, đề yêu cầu Kỹ sư cổng làm cùng một người không viết code.
- Rà các dòng Bảo mật, Quyền hạn, Hiệu năng ở checklist 9 nhóm (đứng tên PIC ở B5).

Vòng 2 (thẻ S6):
- Dò các ticket hỏng theo kiểu khác nhau (`S6-01`, `S6-20`, `S6-42`), tìm bước sai đầu tiên và điền bảng soát lỗi (C2), HAZOP của thẻ (C4) và fault tree trước khi sửa (C6).
- Thiết kế và đăng ký chỉ số theo dõi mới `carrier_fault_concentration`, `ambiguous_fault_rate` (thước đo, dữ liệu, cách tính, điểm mù; C8).

### Bằng chứng

Đóng góp mẫu Phiếu A, commit `2c416cc`, merge `363a87c` (PR #1). Dòng trong phiếu: B5 (dòng 3, 4, 5), B7.3, C2, C4, C6, C8, C11 (dòng 4).

### Exit ticket

Học được: một chỉ số theo dõi tốt phải đếm được từ trace mà không cần nhãn đúng/sai, như `carrier_fault_concentration` (số lỗi mỗi hãng mỗi ngày), vì khi chạy thật không ai gán nhãn cho từng lệnh ghi; và từng ticket đúng riêng lẻ vẫn có thể gây hại khi cộng dồn trong một ngày. Chưa chắc: `ambiguous_fault_rate` chỉ nhận ra ca thiếu `parcel_id` mà hai hãng cùng trễ, nên chưa biết nó có sáng đèn đúng lúc khi khách nói kiện bằng chữ, và ngưỡng 2 lỗi mỗi hãng mỗi ngày chưa tính cửa sổ 7 ngày của hãng nhỏ.

## NguyenTrieuDuong-2A202603524

### Phần việc phụ trách

**Sản phẩm và kinh doanh.** Tiêu chí, thước đo, chi phí và quyết định. File: `config/acceptance_criteria.json`, mục `business` của `config/operating_gates.json`. Phiếu A (A1 đến A5), B3, B7.4, B8, C12.

### Đóng góp cụ thể

Vòng 1:
- Viết mục tiêu cấp hệ thống (1.1), Bản tiêu chí "Nếu … thì chúng tôi sẽ …" cho từng chỉ số, soát bốn câu hỏi (ý nghĩa với mọi bên, ai thiệt, ngày 1, ngày 1.000) và ký tiêu chí trước khi đo: `pass_rate` 0,98, `pass_k` 0,95, ba chỉ số an toàn bằng 0, `business_ops` (8.000đ/ticket, ROI 0,25, 0 ca ùn) và bốn dòng `decision_rule`.
- Viết bản đồ dữ liệu (B3) và ví dụ drift REFUND-v3 sang REFUND-v4 ngày 01/12/2026.
- Đặt cổng kinh doanh (câu 2.9): `daily_refund_cap_vnd` 2.000.000đ, `cost_budget_per_ticket_vnd` 1.500đ, `roi_min` 0,25, `pilot_scope`; mỗi số kèm lý do lấy từ `ops_limits`, `ops_facts` (B7.4).
- Cùng cả bàn ra quyết định v1 (B8).

Vòng 2 (thẻ S6):
- Đọc chi phí mỗi ticket, ROI và tổng hoàn tự động trước và sau khi sửa; xác nhận không có dòng vượt trần.
- Viết quyết định v2 so với v1, ngày xét lại 19/11/2026 (C12).

### Bằng chứng

Commit `4192e12` (ký tiêu chí, `signed_by` ghi tên), `f9f6dda` (2.3), `4ff1191` (2.9), `Xong A5`. Dòng trong phiếu: A1 đến A5, B3, B7.4, B8 (cột PIC ký) và C12.

### Exit ticket

Học được: ngưỡng phải viết trước khi biết kết quả thì quyết định về sau mới có căn cứ. Chưa chắc: tỉ lệ chuyển người 0,25 có hợp lý khi tính cả kiểm mẫu 10% (0,2727 trong khối hàng chờ).

## NguyenDucDat-2A202603544

### Phần việc phụ trách

**Vận hành và pháp lý.** Con người, vận hành, pháp lý và bài nộp. File: mục `operations` và `legal` của `config/operating_gates.json`, `submission/`. Phiếu A (1.2, 1.4), B4, B5, B7.5, B7.6, C10, C11.

### Đóng góp cụ thể

Vòng 1:
- Viết mục tiêu nhìn từ chị Oanh và chị Hạnh (1.2) và telemetry production (1.4).
- HAZOP mở rộng trên `file_carrier_fault` (B4) kèm các dòng ngoài kỹ thuật (người duyệt, dữ liệu gửi bên thứ ba, ngân sách, phạm vi pilot) và checklist 9 nhóm việc, mỗi dòng một PIC có tên (B5).
- Đặt cổng con người và pháp lý (câu 2.10): `pic` NV-TUNG, `approver_id` NV-HANH, số người trực, công suất duyệt, điều kiện dừng, kênh báo tin, lọc trường dữ liệu cá nhân, bắt buộc có nguyên nhân khi ghi lỗi hãng.
- Viết runbook phần 1 đến 3 (ai chịu trách nhiệm, tín hiệu và ngưỡng, điều kiện và cách dừng) và mục giờ cao điểm (B7.5, B7.6).

Vòng 2 (thẻ S6):
- Đọc hàng chờ người duyệt và số người trực sau khi sửa (S6: tỉ lệ chuyển người 0,0833 lên 0,25), bên thứ ba bị ảnh hưởng (GHSH, DNB).
- Viết Risk register (C10), cập nhật checklist 9 nhóm (C11), runbook phần 4 và 5, và gom bài nộp `submission/` (`submission.json`, `check_submission --collect`).

### Bằng chứng

Commit `069b379`, `f87cf5f`, `7b64c59`, `002562d`, `5132d2c`. Dòng trong phiếu: A1 (1.2), A2 (1.4), B4, B5, B7.5, B7.6, C10, C11 (PIC dòng 7 và 8); `submission/manifest.json`, `ĐỦ THÀNH PHẦN` trên `check_submission`.

### Exit ticket

Học được: một con số vận hành (người trực, ngưỡng chờ) phải khớp cả config lẫn runbook thì mới dùng được lúc 23h. Chưa chắc: ca `fail_open` khi LLM quá tải mới có công tắc tắt tay, chưa có cổng code.