# MA TRẬN MODEL AI — 2M Marketing Agency
## "Mỗi model có thế mạnh riêng — dùng đúng người đúng việc"

---

## NGUYÊN TẮC PHÂN MODEL

| Tiêu chí | Model phù hợp |
|----------|--------------|
| Điều phối phức tạp, reasoning sâu | Claude Sonnet |
| Viết sáng tạo, giọng văn tinh tế | Claude Sonnet |
| Content tiếng Việt tự nhiên, "mặn" | MiniMax-M3 hoặc GPT-4o |
| Task nhanh, template, checklist | Claude Haiku / GPT-4o-mini |
| Phân tích dữ liệu số liệu | GPT-4o-mini / DeepSeek |
| Research web, cạo dữ liệu | Gemini Flash (fast + grounding) |
| Mô tả visual / Canva prompts | GPT-4o / Gemini |
| Scheduling, automation logic | DeepSeek / GPT-4o-mini |
| Phản hồi realtime (chat nhanh) | Groq (Llama) — ultra fast |

---

## 11 AGENT × MODEL ASSIGNMENT

| # | Tên Thật | Biệt Danh | Model Chính | Model Dự Phòng | Lý Do |
|---|----------|-----------|-------------|----------------|-------|
| 1 | CMO AI | **Anh Tổng** | `claude-sonnet-4-6` | `gpt-4o` | Điều phối, reasoning phức tạp, quyết định chiến lược |
| 2 | Brand & Creative Director | **Chị Brand** | `claude-sonnet-4-6` | `gpt-4o` | Sáng tạo, giọng văn thương hiệu, nhất quán tone |
| 3 | Campaign & Growth Manager | **Cô Chiến** | `claude-haiku-4-5` | `gpt-4o-mini` | Lập kế hoạch, timeline, KPI — nhanh và có cấu trúc |
| 4 | Content Brain | **Con Muối** | `MiniMax-M3` | `claude-sonnet-4-6` | Tiếng Việt "mặn", sáng tạo, hook mạnh, copy bán hàng |
| 5 | Content & Community Manager | **Bé Viết** | `claude-haiku-4-5` | `gpt-4o-mini` | Bài đăng tiêu chuẩn, caption, template — khối lượng lớn |
| 6 | Video & Design Director | **Đạo Diễn** | `gpt-4o` | `gemini-flash` | Mô tả visual, storyboard, Canva/CapCut prompt |
| 7 | Insight & Intelligence Manager | **Thám Tử** | `claude-sonnet-4-6` | `gemini-flash` | Phân tích đối thủ sâu, market research (Gemini có web grounding) |
| 8 | Analytics & Performance Manager | **Số Học** | `gpt-4o-mini` | `deepseek-chat` | Xử lý số liệu, tính tỷ lệ, format báo cáo — rẻ + nhanh |
| 9 | Knowledge & Automation Manager | **Thư Ký** | `claude-haiku-4-5` | `deepseek-chat` | Quản lý file, index knowledge, automation logic |
| 10 | Operations Manager | **Quản Lý** | `gpt-4o-mini` | `groq/llama` | Task queue, scheduling, nhắc nhở — cần tốc độ |
| 11 | Publisher | **Bé Đăng** | `gpt-4o-mini` | `gemini-flash` | Format final content, check trước khi đăng, auto-schedule |

---

## ƯỚC TÍNH CHI PHÍ (theo mô hình Dilaca: ~89 requests/tháng)

| Model | Giá input/1M token | Giá output/1M token | Dùng cho agent | Ước tính/tháng |
|-------|-------------------|--------------------|--------------:|--------------|
| claude-sonnet-4-6 | $3.00 | $15.00 | CMO, Brand, Thám Tử | ~$0.50 |
| claude-haiku-4-5 | $0.25 | $1.25 | Campaign, Content, Thư Ký | ~$0.10 |
| gpt-4o-mini | $0.15 | $0.60 | Analytics, Ops, Publisher | ~$0.08 |
| MiniMax-M3 | ~$0.10 | ~$0.30 | Con Muối | ~$0.05 |
| gemini-flash | $0.075 | $0.30 | Research, fallback | ~$0.03 |
| deepseek-chat | $0.07 | $0.28 | Số Học, Thư Ký (fallback) | ~$0.03 |
| **TỔNG** | | | | **~$0.79 – $1.50/tháng** |

> **Lưu ý:** Chi phí thực tế phụ thuộc vào số lượng campaign và độ phức tạp brief. Với quy mô 2M Construction (1-2 campaign/tuần), ước tính dưới $5/tháng tổng cộng.

---

## KHI NÀO DÙNG MODEL NÀO

```
Anh Tuan giao việc cho CMO (Claude Sonnet)
         ↓
CMO phân tích và gọi đúng agent:

Cần sáng tạo cao?     → Claude Sonnet (Brand, Thám Tử)
Cần tiếng Việt mặn?  → MiniMax-M3 (Con Muối)
Cần nhanh/nhiều?      → Haiku/GPT-4o-mini (Bé Viết, Số Học, Ops)
Cần research web?     → Gemini Flash (Thám Tử dự phòng)
Cần visual prompt?    → GPT-4o (Đạo Diễn)
Cần siêu nhanh chat?  → Groq Llama (Quản Lý realtime)
```

---

## API KEYS CẦN THIẾT

```env
ANTHROPIC_API_KEY=sk-ant-...         # Claude (CMO, Brand, Thám Tử, Haiku agents)
OPENAI_API_KEY=sk-...                # GPT-4o, GPT-4o-mini
MINIMAX_API_KEY=...                  # Con Muối (tiếng Việt)
GOOGLE_API_KEY=...                   # Gemini Flash (research)
DEEPSEEK_API_KEY=...                 # Fallback rẻ
GROQ_API_KEY=...                     # Groq realtime (tùy chọn)
OPENROUTER_API_KEY=...               # Router tất cả models qua 1 endpoint (khuyên dùng)
```

> **Khuyến nghị:** Dùng **OpenRouter** làm API gateway duy nhất — 1 API key truy cập tất cả models, billing tập trung, dễ switch model khi cần.
