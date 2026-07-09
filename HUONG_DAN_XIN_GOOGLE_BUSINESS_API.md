# HƯỚNG DẪN XIN QUYỀN GOOGLE BUSINESS PROFILE API
## Để Agency tự động đăng bài lên Google Business Profile (giống Facebook/Instagram hiện tại)

**Lưu ý quan trọng:** Đây là bước KHÔNG thể tự động hóa — Google bắt buộc con người nộp đơn và họ tự duyệt thủ công (vài ngày đến vài tuần). Anh Tuan cần tự thực hiện các bước dưới đây bằng tài khoản Google đang là chủ/quản lý (owner/manager) của GBP "2M Construction LLC".

---

## BƯỚC 0 — CHECKLIST ĐIỀU KIỆN (kiểm tra trước khi nộp đơn)

- [ ] GBP "2M Construction LLC" đã **xác minh (verified)** và hoạt động **từ 60 ngày trở lên**
- [ ] Có **website doanh nghiệp** đang hoạt động (2mconstructionllc.com hoặc domain đang dùng)
- [ ] **Email dùng để nộp đơn phải cùng domain với website** — đây là lý do bị từ chối phổ biến nhất.
  - VD: nếu website là `2mconstructionllc.com` thì nên dùng email dạng `tuan@2mconstructionllc.com`, KHÔNG dùng Gmail cá nhân nếu có thể.
  - Nếu chưa có email theo domain riêng, cân nhắc tạo trước khi nộp đơn (Google Workspace hoặc hosting email có sẵn).
- [ ] Email đó phải là **owner hoặc manager** trong Google Business Profile

Nếu thiếu bất kỳ mục nào ở trên, đơn gần như chắc chắn bị từ chối — nên hoàn thiện trước khi nộp.

---

## BƯỚC 1 — TẠO GOOGLE CLOUD PROJECT

1. Vào [console.cloud.google.com](https://console.cloud.google.com) → đăng nhập bằng tài khoản Google là owner/manager của GBP
2. Tạo project mới, đặt tên gợi ý: `2M-Construction-GBP-API`
3. Ghi lại **Project ID** (sẽ cần dùng ở Bước 3)

---

## BƯỚC 2 — NỘP ĐƠN XIN QUYỀN TRUY CẬP API

1. Vào: **https://support.google.com/business/workflow/16726127?hl=en**
2. Đăng nhập bằng đúng email owner/manager của GBP
3. Làm theo wizard trên trang — họ sẽ hỏi:
   - Project ID (Google Cloud project vừa tạo ở Bước 1)
   - Mô tả use case (mục đích sử dụng)
   - Website doanh nghiệp

### Mẫu mô tả use case (copy và chỉnh lại cho phù hợp):

> "2M Construction LLC is a full-service general contractor based in Huntsville, Alabama. We are building an internal marketing automation tool to manage and publish content to our own Google Business Profile listing — including creating posts, responding to reviews, and updating business information. This tool is used exclusively for our own business location and is not offered as a service to other businesses. Website: [điền website 2M]."

**Lưu ý khi điền:**
- Ghi rõ "our own business" — Google dễ từ chối các đơn nghe như làm dịch vụ SEO/agency cho nhiều khách hàng khác nếu chưa có track record.
- Không dùng từ ngữ mơ hồ như "marketing tool" chung chung — nói rõ sẽ làm gì (đăng bài, cập nhật giờ mở cửa, trả lời review).

---

## BƯỚC 3 — CHỜ DUYỆT

- Thời gian: vài ngày đến vài tuần, không có mốc cố định
- Cách kiểm tra đã được duyệt chưa: vào Google Cloud Console → APIs & Services → Quotas → tìm "Business Profile APIs"
  - Quota = **0 QPM** → chưa được duyệt
  - Quota = **300 QPM** → đã được duyệt, có thể dùng

---

## BƯỚC 4 — SAU KHI ĐƯỢC DUYỆT

1. Trong Google Cloud Console, bật (Enable) toàn bộ 8 API thuộc nhóm Business Profile:
   - My Business Account Management API
   - My Business Business Information API
   - My Business Lodging API (nếu có)
   - My Business Place Actions API
   - My Business Notifications API
   - My Business Verifications API
   - My Business Q&A API
   - Account Management API
2. Tạo OAuth 2.0 Client ID (Credentials → Create Credentials → OAuth client ID)
3. Báo lại tôi (kèm Client ID/Secret lưu an toàn) — tôi sẽ:
   - Viết script `scripts/5_SETUP_GBP.bat` + `setup_gbp.py` tương tự cách đã làm với Facebook
   - Thêm `GBP_ACCESS_TOKEN`, `GBP_LOCATION_ID` vào `.env`
   - Nối vào `2m_agency_ai.py` để bước "Bé Đăng" tự đăng thẳng lên Google Business Profile thay vì chỉ xuất file `.txt` để copy tay

---

## TÓM TẮT NHANH

| Bước | Ai làm | Thời gian |
|------|--------|-----------|
| 0. Kiểm tra điều kiện | Anh Tuan | 10 phút |
| 1. Tạo Cloud Project | Anh Tuan | 10 phút |
| 2. Nộp đơn | Anh Tuan | 15 phút |
| 3. Chờ Google duyệt | Google | vài ngày–vài tuần |
| 4. Bật API + báo lại Claude | Anh Tuan + Claude | 30 phút |
