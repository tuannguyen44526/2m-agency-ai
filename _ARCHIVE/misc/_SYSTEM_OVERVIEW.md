# 2M Marketing Agency AI — Tổng Quan Hệ Thống

**Công ty:** 2M Construction LLC  
**Loại hình:** Full-Service General Contractor (Residential & Commercial)  
**Địa bàn:** Huntsville, Alabama  
**Dịch vụ:** Deck, fence, sàn, gạch, sơn, drywall, epoxy, concrete, tủ bếp  
**Màu nhận diện:** Navy (#1B2A4A) · Gold (#C9A84C) · White (#FFFFFF)

---

## Mục Đích Hệ Thống

Thay thế hoàn toàn marketing agency ngoài. Toàn bộ nội dung do AI soạn sẵn, **Tuan Nguyen duyệt trước khi đăng**. Không tự động đăng.

---

## Cấu Trúc 6 Vai Trò

```
01_CMO/                    ← Bạn giao việc vào ĐÂY
02_Content_Marketing/      ← Bài đăng FB, Nextdoor, Angi Pro
03_Brand_Creative/         ← Nhận diện thương hiệu, giọng văn
04_Insight_Competitor/     ← Theo dõi đối thủ & xu hướng thị trường
05_Lead_Outreach/          ← Cold outreach, follow-up lead
06_Analytics_Performance/  ← Đo hiệu quả, tổng hợp số liệu
```

---

## Quy Trình Vận Hành

```
Tuan Nguyen
    ↓ (giao nhiệm vụ)
CMO AI (01_CMO)
    ↓ (phân việc)
┌───────────────┬──────────────┬──────────────┬──────────────┐
Content      Brand        Insight      Lead         Analytics
Manager      Director     Intel        Outreach     Manager
    ↓              ↓            ↓            ↓            ↓
        (nộp bản thảo / báo cáo lên CMO)
CMO AI tổng hợp → Trình Tuan Nguyen duyệt → Đăng/Gửi
```

---

## Nguyên Tắc Bất Biến

1. **2M là full-service GC** — không bao giờ chỉ nói "deck/fence company"
2. **Duyệt trước khi đăng** — AI soạn, người duyệt
3. **Song ngữ Việt-Anh** khi phù hợp (FB, cộng đồng Việt)
4. **Không xử lý báo giá / bản vẽ kỹ thuật** — đó là hệ thống riêng
5. **Tone:** Chuyên nghiệp & tin cậy, không quá salesy

---

## Cách Dùng Nhanh

Mỗi thư mục vai trò chứa:
- `ROLE.md` — Mô tả nhiệm vụ + system prompt để dùng với AI
- `EXAMPLES.md` — Ví dụ output mẫu
- (Một số vai có thêm template hoặc tracker)

Khi cần giao việc: mở `01_CMO/ROLE.md`, copy system prompt vào Claude, rồi ra lệnh.
