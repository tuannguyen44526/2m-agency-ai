# 2M Marketing Agency AI

**Công ty:** 2M Construction LLC — Full-Service General Contractor, Huntsville, Alabama
**Chủ:** Tuan Nguyen · (938) 302-6795
**Màu nhận diện:** Navy `#1B2A4A` · Gold `#C9A84C` · White `#FFFFFF`

Hệ thống AI thay thế marketing agency ngoài: gõ 1 lệnh → các agent AI tự soạn toàn bộ content → **Tuan Nguyen duyệt trước khi đăng**. App có thể đăng trực tiếp lên Facebook/Instagram sau khi duyệt.

---

## Hệ thống chính: App Streamlit `2m_agency_ai.py`

App có 8 agent chạy tuần tự:

| Agent | Vai trò |
|-------|---------|
| 🚀 Cô Chiến | Campaign Manager — mục tiêu, KPI, timeline |
| 🧂 Con Muối | Content Brain — hook mạnh, tiếng Việt "mặn" |
| ✍️ Bé Viết | Content Manager — bài đăng FB/Nextdoor/GBP |
| 🎨 Chị Brand | Brand Director — giọng văn, nhận diện |
| 🎬 Đạo Diễn | Visual Director — mô tả ảnh, Canva prompt |
| 🔬 Cô Học | SEO Keyword Strategist |
| 📱 Bé Quản | Social Media Manager |
| 📤 Bé Đăng | Publisher — format, checklist trước khi đăng |

## Cách chạy

1. Lần đầu: double-click `1_SETUP.bat`
2. Mỗi lần dùng: double-click `2_RUN.bat` → browser mở `http://localhost:8501`
3. Chi tiết: xem `docs/QUICK_START.md` · Deploy cloud: `docs/DEPLOY_GUIDE.md`

## Cấu trúc thư mục

```
├── 2m_agency_ai.py        ← App chính (Streamlit)
├── requirements.txt
├── 1_SETUP.bat            ← Cài đặt lần đầu
├── 2_RUN.bat              ← Chạy app hằng ngày
│
├── WEEKLY_PLAN.md         ← Anh Tuan cập nhật mỗi tuần — app đọc làm lệnh nhanh
├── CUSTOMER_INSIGHTS.md   ← Hồ sơ khách hàng Huntsville — app nạp vào context
├── SEO_GUIDELINES.md      ← Từ khóa local SEO — app nạp vào context
│
├── CAMPAIGNS/             ← Output campaign (app tự ghi, không commit git)
├── PUBLISH_QUEUE/         ← Nội dung chờ đăng theo kênh (app tự ghi, không commit git)
│
├── scripts/               ← Script phụ trợ
│   ├── 3_SETUP_FACEBOOK.bat + setup_facebook.py  ← Kết nối FB/IG (token đọc từ .env)
│   ├── 4_CHECK_IG.bat + check_ig.py              ← Kiểm tra Instagram
│   └── RESTART_APP.bat
│
├── docs/                  ← QUICK_START.md, DEPLOY_GUIDE.md
├── _ARCHIVE/              ← Phiên bản cũ (xem _ARCHIVE/README.md)
└── .env                   ← API keys — KHÔNG BAO GIỜ commit
```

⚠️ **Lưu ý:** 3 file `WEEKLY_PLAN.md`, `CUSTOMER_INSIGHTS.md`, `SEO_GUIDELINES.md` phải nằm ở thư mục gốc — app đọc theo đường dẫn này.

## Nguyên tắc bất biến

1. **2M là full-service GC** — không bao giờ chỉ nói "deck/fence company"
2. **Duyệt trước khi đăng** — AI soạn, người duyệt
3. **Song ngữ Việt–Anh** khi phù hợp
4. **Không xử lý báo giá / bản vẽ kỹ thuật**
5. **Tone:** chuyên nghiệp & tin cậy, không quá salesy

## Bảo mật

- Mọi token/key chỉ nằm trong `.env` (local) hoặc Streamlit Cloud Secrets — **không hardcode vào code**
- Keys cần có: `ANTHROPIC_API_KEY`, `FB_PAGE_ACCESS_TOKEN`, `FB_PAGE_ID`, `IG_BUSINESS_ACCOUNT_ID`, `SITE_ADMIN_PASSWORD`, `IMGBB_API_KEY`, `FB_LONG_LIVED_TOKEN` (chỉ khi chạy setup FB)
