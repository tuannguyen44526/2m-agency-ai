# HƯỚNG DẪN CÀI ĐẶT OPENCLAW
## 2M Marketing Agency AI — Full Stack Setup

---

## OPENCLAW LÀ GÌ?

OpenClaw là framework mã nguồn mở để chạy hệ thống multi-agent AI ngay trên máy tính của bạn (hoặc VPS). Nó làm vai trò "bộ não trung tâm" điều phối tất cả agent — đúng cách Dilaca Studio AI hoạt động.

GitHub: https://github.com/openclaw/openclaw  
Chi phí vận hành Dilaca: **$1.03/30 ngày** với 89 requests — siêu rẻ.

---

## KIẾN TRÚC TỔNG THỂ 2M

```
┌─────────────────────────────────────────────┐
│            ANH TUAN (bạn)                   │
│   Ra lệnh qua: Claude Desktop / Telegram    │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│          OPENCLAW ORCHESTRATOR              │
│         (chạy trên máy tính bạn)           │
│  - Nhận lệnh                               │
│  - Route đến đúng agent                    │
│  - Quản lý memory & context                │
└──────┬──────┬──────┬──────┬──────┬─────────┘
       ↓      ↓      ↓      ↓      ↓
   [Claude] [GPT] [Mini] [Gemini] [Groq]
    Sonnet   4o    Max    Flash   Llama
       ↓      ↓      ↓      ↓      ↓
  Anh   Chi  Con  Tham   So
  Tong  Brand Muoi  Tu   Hoc
  Cô    Bé    Đạo  Thư   Quản  Bé
  Chiến Viết  Diễn Ký    Lý    Đăng
```

---

## BƯỚC 1: PREREQUISITES

```bash
# Cài Node.js (v18+)
# Download từ: https://nodejs.org

# Cài Git
# Download từ: https://git-scm.com

# Verify
node --version    # phải thấy v18+
npm --version
git --version
```

---

## BƯỚC 2: CLONE VÀ CÀI OPENCLAW

```bash
# Clone repo
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Cài dependencies
npm install

# Copy config template
cp .env.example .env
```

---

## BƯỚC 3: CẤU HÌNH API KEYS (.env)

Mở file `.env` và điền:

```env
# === ANTHROPIC (Claude) ===
ANTHROPIC_API_KEY=sk-ant-...
# Dùng cho: Anh Tổng (CMO), Chị Brand, Thám Tử, Cô Chiến, Bé Viết, Thư Ký

# === OPENAI ===
OPENAI_API_KEY=sk-...
# Dùng cho: Đạo Diễn (gpt-4o), Số Học, Quản Lý, Bé Đăng (gpt-4o-mini)

# === MINIMAX (Tiếng Việt tự nhiên) ===
MINIMAX_GROUP_ID=...
MINIMAX_API_KEY=...
# Dùng cho: Con Muối

# === GOOGLE GEMINI (Research/Grounding) ===
GOOGLE_API_KEY=...
# Dùng cho: Thám Tử (fallback với web search)

# === GROQ (Siêu nhanh, realtime) ===
GROQ_API_KEY=...
# Dùng cho: Quản Lý (fallback realtime)

# === OPENROUTER (Gateway tất cả models - KHUYÊN DÙNG) ===
OPENROUTER_API_KEY=...
# Thay thế tất cả key trên bằng 1 key duy nhất
# Đăng ký tại: https://openrouter.ai

# === COMPANY CONFIG ===
COMPANY_NAME="2M Construction LLC"
COMPANY_LOCATION="Huntsville, Alabama"
OWNER_NAME="Tuan Nguyen"
HUMAN_APPROVAL_REQUIRED=true
```

> **💡 Tip:** Dùng **OpenRouter** thay vì nhiều API key riêng lẻ. 1 key, 1 billing, truy cập 100+ models. Dễ quản lý hơn nhiều.

---

## BƯỚC 4: CẤU HÌNH AGENTS

Tạo thư mục agents và copy SOUL.md files:

```bash
mkdir -p agents/souls
mkdir -p agents/memory

# Copy tất cả SOUL.md từ thư mục 2M Construction vào đây
# agents/souls/SOUL_anh_tong.md
# agents/souls/SOUL_chi_brand.md
# ... (tất cả 11 agents)

# Copy AGENTS.md master config
cp "path/to/Ai Agentcy for 2M Construction/00_OPENCLAW_SETUP/AGENTS.md" ./config/agents.yaml
```

---

## BƯỚC 5: CHẠY HỆ THỐNG

```bash
# Start OpenClaw
npm run start

# Hoặc chạy background (Linux/Mac)
npm run start &

# Windows: dùng PM2
npm install -g pm2
pm2 start npm --name "2m-agency" -- run start
pm2 save
```

Khi chạy thành công, bạn sẽ thấy:
```
✅ 2M Marketing Agency AI — Online
✅ 11/11 Agents loaded
✅ Knowledge Vault: 8 sources indexed
✅ Awaiting commands from Tuan Nguyen...
```

---

## BƯỚC 6: GIAO TIẾP VỚI HỆ THỐNG

**Option A: Qua Claude Desktop (hiện tại)**
- Paste system prompt của Anh Tổng → Ra lệnh bằng tiếng Việt

**Option B: Qua Telegram Bot (sau khi setup OpenClaw)**
```env
TELEGRAM_BOT_TOKEN=...    # Tạo bot qua @BotFather
TELEGRAM_CHAT_ID=...      # Chat ID của bạn
```
Sau đó nhắn tin thẳng vào Telegram là xong — agent trả lời ngay.

**Option C: Qua Web UI (Dashboard đã xây)**
- Mở `2M_Agency_Dashboard.html` trong browser
- Dashboard visualize agent status và campaign

---

## BƯỚC 7: BROWSER AUTOMATION (tùy chọn, như Dilaca)

Dilaca dùng "dilaca-browser-control-service" để agent tự research web. Với 2M:

```bash
# Cài Playwright (browser automation)
npm install playwright
npx playwright install chromium

# Thêm vào .env:
BROWSER_AUTOMATION=true
BROWSER_HEADLESS=true
```

Cho phép Thám Tử tự động:
- Mở Google Maps → tìm đối thủ GC Huntsville
- Đọc review, ghi nhận thông tin
- Trả báo cáo về cho Anh Tổng

---

## CHI PHÍ ƯỚC TÍNH

```
Với ~100 requests/tháng (quy mô 2M Construction):

Model                  Requests  Chi phí/tháng
─────────────────────────────────────────────
claude-sonnet-4-6          30      ~$0.45
claude-haiku-4-5           25      ~$0.05
gpt-4o                      5      ~$0.15
gpt-4o-mini                25      ~$0.04
MiniMax-M3                 10      ~$0.03
Gemini Flash                5      ~$0.01
─────────────────────────────────────────────
TỔNG                      100      ~$0.73 – $1.50/tháng
```

**Kết luận: Dưới $2/tháng cho toàn bộ marketing agency AI.**

---

## ROADMAP TRIỂN KHAI

**Phase 1 (Tuần 1-2) — Manual với Claude Desktop:**
- ✅ Files và system prompts đã sẵn sàng
- ✅ Dashboard HTML đã có
- Dùng Claude Desktop, paste system prompt → ra lệnh

**Phase 2 (Tháng 1) — Semi-auto với OpenClaw:**
- [ ] Cài OpenClaw
- [ ] Kết nối API keys
- [ ] Test với 1 campaign nhỏ

**Phase 3 (Tháng 2-3) — Full automation:**
- [ ] Telegram bot kết nối
- [ ] Browser automation cho Thám Tử
- [ ] Bé Đăng auto-schedule (nhưng vẫn cần Tuan duyệt)
- [ ] Monthly analytics auto-report

---

## TÀI LIỆU THAM KHẢO

- OpenClaw GitHub: https://github.com/openclaw/openclaw
- Multi-agent guide: https://capodieci.medium.com/ai-agents-036-build-a-multi-agent-openclaw-system-without-config-hell-orchestrator-sub-agents-da68de349010
- OpenClaw orchestration: https://zenvanriel.com/ai-engineer-blog/openclaw-multi-agent-orchestration-guide/
- OpenRouter (API gateway): https://openrouter.ai
