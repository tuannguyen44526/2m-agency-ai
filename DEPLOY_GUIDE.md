# 🚀 Hướng Dẫn Deploy 2M Agency AI Lên Streamlit Cloud

Sau khi deploy, anh Tuan có thể truy cập app từ **bất kỳ máy tính hoặc điện thoại nào** qua link dạng:
`https://2m-agency-ai.streamlit.app`

---

## BƯỚC 1 — Tạo GitHub Repository Riêng (Private)

1. Vào [github.com](https://github.com) → đăng nhập
2. Nhấn **New repository**
3. Đặt tên: `2m-agency-ai`
4. Chọn **Private** (quan trọng — bảo mật API keys)
5. Nhấn **Create repository**

---

## BƯỚC 2 — Upload Code Lên GitHub

Mở **GitHub Desktop** (đã cài sẵn trên máy anh):

1. **File → Add Local Repository**
2. Chọn thư mục: `C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction`
3. Nếu hỏi "Create repository" → nhấn OK
4. Nhấn **Publish repository** → chọn **Private**

> ⚠️ Đảm bảo `.gitignore` có dòng `.env` và `.streamlit/secrets.toml` để không upload API keys

---

## BƯỚC 3 — Tạo .gitignore (nếu chưa có)

Tạo file `.gitignore` trong thư mục app với nội dung:
```
.env
.streamlit/secrets.toml
__pycache__/
*.pyc
CAMPAIGNS/
PUBLISH_QUEUE/
```

---

## BƯỚC 4 — Deploy Lên Streamlit Cloud

1. Vào [share.streamlit.io](https://share.streamlit.io)
2. Đăng nhập bằng GitHub account
3. Nhấn **New app**
4. Chọn:
   - **Repository:** `2m-agency-ai` (repo vừa tạo)
   - **Branch:** `main`
   - **Main file path:** `2m_agency_ai.py`
5. Nhấn **Deploy**

---

## BƯỚC 5 — Điền API Keys (Secrets)

Sau khi deploy, vào **Settings → Secrets** trong Streamlit Cloud, dán nội dung:

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-..."

FB_PAGE_ACCESS_TOKEN = "EAAxxxxx..."
FB_PAGE_ID = "1002823072922245"
IG_BUSINESS_ACCOUNT_ID = "17841437566023695"

SITE_ADMIN_PASSWORD = "2M@Huntsville#2026"
```

*(copy values từ file `.env` trên máy anh)*

Nhấn **Save** → App tự động restart với secrets mới.

---

## BƯỚC 6 — Truy Cập Từ Bất Kỳ Đâu

- Link app: `https://[tên-app].streamlit.app`
- Có thể đặt password bảo vệ trong **Settings → Sharing → Password protect**

---

## LƯU Ý QUAN TRỌNG

| Vấn đề | Giải pháp |
|--------|-----------|
| App ngủ sau 7 ngày không dùng | Vào link → chờ ~30 giây wake up |
| File lưu trong CAMPAIGNS/ bị mất | Streamlit Cloud không lưu file local — dùng Google Drive hoặc GitHub |
| Cần update code | Push lên GitHub → Streamlit tự deploy lại |

---

## THAY THẾ: Dùng Ngrok (Test Nhanh Không Cần GitHub)

Nếu chỉ muốn dùng tạm từ máy khác:

1. Tải [ngrok](https://ngrok.com/download) → cài vào máy anh
2. Mở terminal: `ngrok http 8501`
3. Copy link dạng `https://xxxx.ngrok.io` → gửi cho bất kỳ ai

> ⚠️ Link mất khi tắt máy hoặc đóng terminal
