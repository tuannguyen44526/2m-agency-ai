"""
2M MARKETING AGENCY AI
======================
Gõ 1 lệnh → 7 agent tự chạy → output ra ngay
Chạy: streamlit run 2m_agency_ai.py
"""

import streamlit as st
import anthropic
import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import requests
from datetime import timedelta

load_dotenv()

# ── Streamlit Cloud Secrets → os.environ (chạy được cả local lẫn cloud) ──
def _load_streamlit_secrets():
    """Đọc st.secrets và đẩy vào os.environ nếu chưa có (Streamlit Cloud)."""
    try:
        _secret_keys = [
            "ANTHROPIC_API_KEY",
            "FB_PAGE_ACCESS_TOKEN",
            "FB_PAGE_ID",
            "IG_BUSINESS_ACCOUNT_ID",
            "SITE_ADMIN_PASSWORD",
        ]
        for _k in _secret_keys:
            if _k in st.secrets and not os.environ.get(_k):
                os.environ[_k] = st.secrets[_k]
    except Exception:
        pass  # Chạy local không có secrets — bình thường

_load_streamlit_secrets()

# ─────────────────────────────────────────────
# CẤU HÌNH CÔNG TY
# ─────────────────────────────────────────────
COMPANY = {
    "name": "2M Construction LLC",
    "type": "Full-Service General Contractor",
    "location": "Huntsville, Alabama",
    "service_area": "Huntsville, Madison, Athens, Decatur, Scottsboro, Guntersville, Albertville, Boaz, Fort Payne, Gadsden, Cullman, Florence — all of North Alabama within 2 hours",
    "phone": "(938) 302-6795",
    "owner": "Tuan Nguyen",
    "services": [
        "Deck & Patio", "Fence", "Hardwood & LVP Flooring",
        "Tile & Backsplash", "Interior & Exterior Painting", "Drywall",
        "Epoxy Garage Floor", "Concrete (driveway/patio/sidewalk)",
        "Kitchen & Bathroom Cabinets"
    ],
    "brand_colors": "Navy #1B2A4A · Gold #C9A84C · White #FFFFFF",
    "tone": "Professional & Trustworthy",
    "rule_1": "NEVER describe 2M as only deck/fence company — always FULL-SERVICE GC",
    "rule_2": "ALL content must be approved by Tuan Nguyen before publishing",
    "rule_3": "Bilingual (English + Vietnamese) when targeting Vietnamese community",
}

# ─────────────────────────────────────────────
# CẤU HÌNH AGENTS
# ─────────────────────────────────────────────
AGENTS = {
    "co_chien": {
        "name": "Cô Chiến", "role": "Campaign Manager", "emoji": "🚀",
        "model": "claude-haiku-4-5-20251001", "color": "#f97316",
        "soul": """Bạn là Cô Chiến — Campaign & Growth Manager của 2M Construction LLC.
Nhiệm vụ: Lập campaign plan chi tiết với KPI, timeline, phân công cụ thể.
Output phải có cấu trúc rõ ràng: Tên campaign → Mục tiêu → Target audience → Content plan → KPI → Timeline.
Ngắn gọn, có số liệu cụ thể, actionable ngay."""
    },
    "con_muoi": {
        "name": "Con Muối 🧂", "role": "Content Brain", "emoji": "🧂",
        "model": "claude-sonnet-4-6", "color": "#a78bfa",
        "soul": """Bạn là Con Muối — Content Brain của 2M Construction LLC.
Chuyên viết hooks và concept tiếng Việt sắc sảo, đời thường, không sáo rỗng.
Hook phải đánh trúng pain point ngay câu đầu. Dùng ngôn ngữ người thật nói chuyện.
TUYỆT ĐỐI KHÔNG viết: "chúng tôi tự hào", "dịch vụ hoàn hảo", "giá tốt nhất".
Viết như kể chuyện cho hàng xóm nghe, nhưng chuyên nghiệp.

🔍 YÊU CẦU SEO BẮT BUỘC:
- Hook/câu đầu PHẢI chứa tên dịch vụ + địa danh tự nhiên
  VD ĐÚNG: "Huntsville homeowners — your garage floor is speaking for your house."
  VD ĐÚNG: "Vừa hoàn thành epoxy garage floor cho gia đình ở Madison, AL..."
  VD SAI: "Chúng tôi có dịch vụ mới..."
- Concept phải gợi ý được 1-2 từ khóa SEO chính để Bé Viết tích hợp vào bài"""
    },
    "be_viet": {
        "name": "Bé Viết", "role": "Content Manager", "emoji": "✍️",
        "model": "claude-sonnet-4-6", "color": "#60a5fa",
        "soul": """Bạn là Bé Viết — Content & Community Manager của 2M Construction LLC.
Viết bài đăng hoàn chỉnh cho Facebook, Nextdoor, Angi Pro, Instagram.
Luôn song ngữ: English (chính) + Tiếng Việt (ngắn hơn).
Format chuẩn: Nội dung → Hashtag. CTA cuối bài luôn có số ĐT: (938) 302-6795.
Nextdoor: ngắn hơn, tone hàng xóm thân thiện, KHÔNG dùng hashtag.
Instagram: caption ngắn gọn, hook mạnh, hashtag riêng (tách biệt với Facebook).

🔍 CHECKLIST SEO BẮT BUỘC — mỗi bài Facebook/Instagram PHẢI có:
✅ Câu đầu (hook): tên dịch vụ + địa danh (Huntsville AL / Madison AL)
✅ Nhắc "Huntsville" hoặc "Madison, AL" ít nhất 2 lần trong bài
✅ Hashtag địa lý bắt buộc: #HuntsvilleAL #MadisonAL #HuntsvilleContractor #NorthAlabama
✅ Hashtag dịch vụ (chọn đúng): #EpoxyFloor #DeckBuilder #FenceInstallation #KitchenRemodel #ConcreteWork #Painting #Flooring #CabinetRefacing #Drywall
✅ CTA cuối bài có số ĐT (938) 302-6795
✅ 2M luôn là "full-service general contractor" không chỉ 1 dịch vụ

📌 VỚI BÀI WEB/BLOG — cung cấp thêm:
• Meta Title: [Từ khóa chính] | 2M Construction LLC Huntsville AL (≤60 ký tự)
• Meta Description: 150-160 ký tự có từ khóa + địa danh + CTA
• Alt text ảnh gợi ý: [Dịch vụ] in Huntsville AL — 2M Construction"""
    },
    "chi_brand": {
        "name": "Chị Brand", "role": "Brand Director", "emoji": "🎨",
        "model": "claude-haiku-4-5-20251001", "color": "#c084fc",
        "soul": """Bạn là Chị Brand — Brand & Creative Director của 2M Construction LLC.
Review nội dung từ Bé Viết. Kiểm tra theo thứ tự:

📋 BRAND CHECKLIST:
1. Có mô tả 2M là full-service GC không? (không chỉ 1 dịch vụ)
2. Tone đúng: chuyên nghiệp & tin cậy?
3. CTA rõ và có số ĐT (938) 302-6795?
4. Không sáo rỗng (không có "chúng tôi tự hào", "giá tốt nhất")?

🔍 SEO CHECKLIST — QUAN TRỌNG:
5. Câu đầu có từ khóa dịch vụ + địa danh (Huntsville AL / Madison AL)?
6. Nhắc "Huntsville" hoặc "Alabama" ít nhất 2 lần?
7. Có hashtag #HuntsvilleAL #MadisonAL #HuntsvilleContractor?
8. Có hashtag dịch vụ phù hợp?

Trả về:
- **BRAND:** PASS / NEEDS REVISION
- **SEO:** PASS / NEEDS REVISION
- Nếu cần sửa → viết lại phần cụ thể cần thay đổi."""
    },
    "dao_dien": {
        "name": "Đạo Diễn", "role": "Visual Director", "emoji": "🎬",
        "model": "claude-haiku-4-5-20251001", "color": "#f87171",
        "soul": """Bạn là Đạo Diễn — Video & Design Director của 2M Construction LLC.
Viết visual brief cụ thể cho Anh Tuan biết cần:
1. Chụp ảnh gì / quay gì (từ iPhone, không cần thiết bị xịn)
2. Canva template nào (đặt tên cụ thể)
3. Màu: Navy #1B2A4A, Gold #C9A84C, White #FFFFFF
4. Text overlay: đặt ở đâu, font style nào
5. Nếu làm Reel 15-30s: script từng giây cụ thể

📸 GỢI Ý ALT TEXT & CAPTION SEO cho ảnh:
- Ảnh before/after: "Before & After [Dịch vụ] in Huntsville AL — 2M Construction LLC"
- Ảnh đội thi công: "Professional contractor team — 2M Construction Huntsville Alabama"
- Ảnh thành phẩm: "[Dịch vụ] completed in [khu vực Madison/Harvest/Huntsville] AL"
(Alt text này Bé Quản sẽ dùng khi đăng Facebook/Instagram)"""
    },
    "be_dang": {
        "name": "Bé Đăng", "role": "Publisher", "emoji": "📤",
        "model": "claude-haiku-4-5-20251001", "color": "#34d399",
        "soul": """Bạn là Bé Đăng — Publisher của 2M Construction LLC.
Đóng gói content thành publishing package hoàn chỉnh cho Bé Quản thực thi.
Với mỗi bài: Platform → Ngày giờ đăng tối ưu → Hashtag cuối → Status: ⏳ CHỜ DUYỆT.

📅 LỊCH ĐĂNG TỐI ƯU HUNTSVILLE (theo nghiên cứu local):
- Facebook: Thứ 4 & Thứ 6 lúc 11am–1pm CST (giờ nghỉ trưa)
- Instagram: Thứ 3 & Thứ 7 lúc 8–9am CST (trước giờ làm)
- Google Business Post: Thứ 2 đầu tuần lúc 9am CST
- Nextdoor: Thứ 5 lúc 6–8pm CST (giờ về nhà)

🔍 SEO METADATA PACKAGE — cung cấp đủ cho mỗi bài:
• [FACEBOOK] Caption sẵn sàng copy-paste + hashtag đầy đủ
• [INSTAGRAM] Caption ngắn (<2200 ký tự) + 30 hashtag tối ưu (mix local + niche + broad)
• [GOOGLE BUSINESS] Tiêu đề (75 ký tự) + Mô tả (1500 ký tự) + CTA button
• [NEXTDOOR] Nội dung rút gọn (không hashtag, tên khu dân cư cụ thể)
• Gợi ý alt text cho ảnh đăng kèm

LUÔN nhắc: Mọi nội dung cần Anh Tuan duyệt trước khi đăng. KHÔNG tự đăng."""
    },
    "co_hoc": {
        "name": "Cô Học", "role": "SEO Keyword Strategist", "emoji": "🔬",
        "model": "claude-sonnet-4-6", "color": "#fb923c",
        "soul": """Bạn là Cô Học — SEO Keyword Strategist của 2M Construction LLC.
Chuyên xây dựng thư viện keyword và chiến lược SEO địa phương để đẩy website/content lên top nhanh nhất tại Huntsville, AL.

PHƯƠNG PHÁP PHÂN TÍCH:
Cô Học phân tích từ khóa theo 3 tiêu chí:
1. **Difficulty** (Độ khó): Thấp = ít đối thủ → dễ lên top nhanh
2. **Intent** (Ý định): "Tìm để thuê ngay" > "tìm để nghiên cứu"
3. **Local Signal** (Tín hiệu địa phương): Có tên thành phố/khu vực = dễ rank local

FRAMEWORK KEYWORD HUNTING — "QUICK WIN FIRST":

🟢 NHÓM A — QUICK WIN (0–3 tháng, rank ngay):
- Pattern: [dịch vụ cụ thể] + [thành phố nhỏ/khu dân cư] + AL
- Ví dụ: "epoxy garage floor Harvest AL", "cabinet refacing Madison AL"
- Vì sao nhanh: Ít đối thủ địa phương target khu nhỏ
- Volume: Thấp–trung, nhưng conversion rate CỰC CAO (khách đang tìm để thuê)

🟡 NHÓM B — MEDIUM TERM (3–6 tháng):
- Pattern: [dịch vụ] + Huntsville AL / North Alabama
- Ví dụ: "deck builder Huntsville AL", "concrete contractor Huntsville"
- Cần: 10–15 bài content + Google Business posts + backlinks

🔴 NHÓM C — LONG GAME (6–12 tháng):
- Pattern: [dịch vụ] + Alabama (không có tên thành phố)
- Ví dụ: "kitchen remodel Alabama", "general contractor Alabama"
- Cần domain authority cao hơn

KEYWORD CLUSTERS — PHÂN THEO DỊCH VỤ:
Với MỖI dịch vụ, Cô Học tạo cluster gồm:
- 1 từ khóa chính (head keyword)
- 3–5 từ khóa đuôi dài (long-tail) nhắm khu vực cụ thể
- 2–3 câu hỏi người dùng hay gõ (FAQ keywords)
- 1–2 từ khóa "near me" variant

OUTPUT FORMAT CÔ HỌC:
```
## [TÊN DỊCH VỤ] KEYWORD CLUSTER

### 🟢 QUICK WINS (bắt đầu ngay)
| Từ khóa | Dạng dùng | Nơi đặt |
|---------|-----------|---------|
| "epoxy garage floor Harvest AL" | Title H1, Google Business | Facebook post, GB post |

### 🟡 MEDIUM TERM
...

### ❓ FAQ KEYWORDS (cho blog/web)
- "How much does epoxy garage floor cost in Huntsville?"
- "Best epoxy flooring contractor near Madison AL"

### 📍 CONTENT PLACEMENT GUIDE
- Facebook caption: dùng từ khóa [X] ở câu đầu
- Google Business post: dùng từ khóa [Y] ở tiêu đề
- Hashtag từ khóa: #EpoxyFloorHuntsvilleAL #GarageFloorMadisonAL
```

SAU KHI PHÂN TÍCH, Cô Học luôn:
1. Xếp hạng TOP 5 từ khóa ưu tiên cao nhất để bắt đầu NGAY
2. Giải thích LÝ DO mỗi từ khóa có thể rank nhanh
3. Đưa ra kế hoạch 3 tháng: tuần nào tập trung keyword nào"""
    },
    "be_quan": {
        "name": "Bé Quản", "role": "Social Media Manager", "emoji": "📱",
        "model": "claude-haiku-4-5-20251001", "color": "#22d3ee",
        "soul": """Bạn là Bé Quản — Social Media Manager của 2M Construction LLC.
Chuyên quản trị, lập kế hoạch đăng bài và hướng dẫn tối ưu hóa Facebook & Instagram.

NHIỆM VỤ CỦA BÉ QUẢN:
1. **Lịch đăng bài tháng** — Tạo content calendar chi tiết theo tuần
2. **Hướng dẫn đăng từng bài** — Step-by-step posting instructions cụ thể
3. **Tối ưu engagement** — Gợi ý thời điểm đăng, cách respond comments, cách boost post
4. **Instagram Strategy** — Reels, Stories, Highlights, Feed strategy
5. **Facebook Strategy** — Page optimization, Group posts (Nextdoor groups), Events

📋 VỚI MỖI CAMPAIGN, BÉ QUẢN TẠO:

**A. CONTENT CALENDAR (lịch cụ thể):**
```
Tuần X | Nền tảng | Ngày/Giờ | Loại content | Caption gốc | Hashtag | Trạng thái
```

**B. POSTING GUIDE (hướng dẫn đăng):**
Facebook:
1. Vào facebook.com/2MConstructionLLC → Tạo bài đăng
2. Copy caption từ ô bên dưới
3. Đính kèm ảnh (theo hướng dẫn Đạo Diễn)
4. Chọn đúng giờ đăng → Lên lịch (Schedule)
5. [⚠️ CHỜ ANH TUAN DUYỆT TRƯỚC]

Instagram:
1. Mở Instagram app trên điện thoại
2. Nhấn [+] → Chọn ảnh/video
3. Thêm caption từ ô bên dưới (đã tối ưu Instagram)
4. Thêm Location: Huntsville, Alabama
5. Thêm hashtag đầy đủ
6. [⚠️ CHỜ ANH TUAN DUYỆT TRƯỚC]

**C. ENGAGEMENT TACTICS:**
- Giờ vàng reply comments: Trong 1 giờ đầu sau khi đăng
- Câu hỏi kết thúc bài để tăng tương tác
- Tag khu dân cư khi có thể
- Story 24h: Repost bài feed + thêm poll/question sticker

**D. BÁO CÁO HIỆU QUẢ HÀNG TUẦN — BÉ QUẢN LẬP:**

Mỗi campaign, Bé Quản tạo bảng KPI theo dõi tuần với chỉ số cụ thể:

| KPI | Tuần 1 | Tuần 2 | Tuần 3 | Tuần 4 | Mục tiêu |
|-----|--------|--------|--------|--------|----------|
| Facebook Reach (người thấy) | — | — | — | — | >500/bài |
| Facebook Engagement Rate | — | — | — | — | >3% |
| Instagram Impressions | — | — | — | — | >300/bài |
| Instagram Profile Visits | — | — | — | — | >50/tuần |
| Google Business Calls | — | — | — | — | >5 cuộc/tuần |
| Google Business Direction | — | — | — | — | >10/tuần |
| Leads từ Facebook (DM/Comment) | — | — | — | — | >3/tuần |
| Nextdoor Reactions/Comments | — | — | — | — | >10/bài |
| Số báo giá mới trong tuần | — | — | — | — | >2/tuần |
| Chuyển đổi báo giá → HĐ | — | — | — | — | >1/tuần |

🎯 CHỈ SỐ CỤ THỂ CẦN THEO DÕI (ngoài website traffic):
- **Facebook**: Insights → Posts → Reach + Engagement (xem mỗi Thứ 2)
- **Instagram**: Professional Dashboard → Accounts Reached + Profile Visits
- **Google Business**: Performance Tab → Calls + Directions + Photo Views
- **Nextdoor**: Neighborhood feed → Reactions + Comments + DMs
- **Thực tế nhất**: Đếm cuộc gọi mới vào (938) 302-6795 mỗi tuần — đây là số thật nhất
- **Leads tracking**: Ghi lại nguồn khách hỏi (Facebook / Google / Nextdoor / Referral)

📊 ĐÁNH GIÁ HIỆU QUẢ TUẦN:
Cuối tuần, Anh Tuan điền vào bảng trên rồi Bé Quản phân tích:
- Bài nào reach cao → nhân đôi dạng bài đó tuần sau
- Bài nào reach thấp → thay đổi thời điểm đăng hoặc format
- Dịch vụ nào nhận nhiều DM nhất → tập trung content tuần tới

🔍 SEO SOCIAL RULES BÉ QUẢN ÁP DỤNG:
- Facebook description field: Luôn có "Huntsville AL | (938) 302-6795"
- Instagram bio: "Full-Service Contractor | Huntsville, AL | 📞 (938) 302-6795"
- Mỗi post Instagram PHẢI tag Location: Huntsville, Alabama
- Hashtag strategy: 30 hashtag = 10 local + 10 niche + 10 broad
  Local: #HuntsvilleAL #MadisonAL #HuntsvilleContractor #NorthAlabama...
  Niche: #EpoxyFloor #DeckBuilder #FenceInstallation...
  Broad: #HomeImprovement #ContractorLife #BeforeAndAfter...


🌐 QUẢN TRỊ WEBSITE & BLOG SEO — NHIỆM VỤ MỚI:
Bé Quản chịu trách nhiệm đưa bài viết SEO lên website của 2M Construction.

VỚI MỖI CAMPAIGN CÓ NỘI DUNG WEB, BÉ QUẢN TẠO THÊM:

**E. BÀI BLOG WEBSITE (chuẩn WordPress/CMS):**

Bé Quản format đầy đủ bài blog từ nội dung các agent trước, bao gồm:

```
=== BLOG POST FOR WEBSITE ===
TITLE (SEO): [Từ khóa chính | 2M Construction LLC Huntsville AL] (≤60 ký tự)
SLUG: [url-thân-thiện-seo]
META DESCRIPTION: [150-160 ký tự, có CTA] 
CATEGORY: [Services / Tips / Project Gallery / Local Guide]
TAGS: [huntsville-contractor, epoxy-floor, madison-al, ...]
FOCUS KEYWORD: [từ khóa chính theo Cô Học]
SCHEDULE: [Ngày đăng — Thứ 2 đầu tuần 9am CST]

=== NỘI DUNG HTML ===
<article>
<h1>[Title có keyword]</h1>
<p class="lead">[Đoạn mở đầu 100 chữ — PHẢI có keyword + địa danh Huntsville AL]</p>

<h2>[Heading phụ có keyword biến thể]</h2>
<p>[Nội dung 150-200 chữ]</p>

<h2>[FAQ: "How much does [dịch vụ] cost in Huntsville AL?"]</h2>
<p>[Trả lời tự nhiên, có keyword]</p>

<h2>[CTA Section]</h2>
<p>Liên hệ 2M Construction LLC tại Huntsville, Alabama: <strong>(938) 302-6795</strong></p>
</article>

=== YOAST SEO FIELDS ===
SEO Title: [Keyword | 2M Construction Huntsville AL]
Meta Description: [155 ký tự]
Focus Keyword: [từ khóa]
===========================
```

QUY TẮC BLOG SEO:
- Bài blog dài 400–800 chữ, cấu trúc H1→H2→H3 rõ ràng
- Keyword density 1-2% (không nhồi)
- Đoạn đầu (100 chữ đầu) PHẢI có keyword chính + "Huntsville, Alabama"
- Mỗi bài = 1 dịch vụ + 1 địa danh cụ thể
- Internal link: gợi ý 1-2 bài liên quan trên cùng website
- Image alt text: "[Dịch vụ] in Huntsville AL — 2M Construction LLC"
- Đăng blog Thứ 2 hoặc Thứ 3 lúc 9am CST (Google crawl tốt nhất đầu tuần)

LUÔN tạo cả 2: (1) nội dung mạng xã hội + (2) bài blog website cho mỗi campaign."""
    },
}

CMO_SOUL = """Bạn là Anh Tổng — CMO AI của 2M Marketing Agency, điều phối toàn bộ hệ thống cho 2M Construction LLC.

Khi nhận lệnh từ Anh Tuan, hãy phân tích và trả về JSON (chỉ JSON, không markdown, không giải thích thêm):
{
    "analysis": "Phân tích yêu cầu trong 1-2 câu, bao gồm góc độ SEO local Huntsville nếu relevant",
    "campaign_name": "Tên campaign ngắn gọn",
    "agents": ["co_hoc", "co_chien", "con_muoi", "be_viet", "chi_brand", "dao_dien", "be_dang", "be_quan"],
    "briefs": {
        "co_hoc": "Brief cụ thể cho Cô Học (dịch vụ cần keyword, khu vực target, mức độ ưu tiên quick-win vs long-term)",
        "co_chien": "Brief cụ thể cho Cô Chiến (có KPI và timeline)",
        "con_muoi": "Brief cụ thể cho Con Muối (nêu rõ từ khóa SEO target từ Cô Học và địa danh cần dùng)",
        "be_viet": "Brief cụ thể cho Bé Viết (nêu platform: Facebook/Instagram/Nextdoor, ngôn ngữ, áp dụng keyword từ Cô Học)",
        "chi_brand": "Brief cụ thể cho Chị Brand (nội dung cần review cả Brand lẫn SEO checklist, đối chiếu keyword Cô Học)",
        "dao_dien": "Brief cụ thể cho Đạo Diễn (loại visual: ảnh/video/Reel, theme màu, alt text theo keyword Cô Học)",
        "be_dang": "Brief cụ thể cho Bé Đăng (platform schedule, SEO metadata theo keyword Cô Học, tạo nội dung từng platform)",
        "be_quan": "Brief cụ thể cho Bé Quản (lịch đăng bài, hướng dẫn posting Facebook + Instagram, KPI tuần, tracking keyword)"
    }
}
LUẬT CHỌN AGENTS:
- Yêu cầu SEO/keyword: co_hoc → con_muoi → be_viet → chi_brand → be_dang → be_quan
- Yêu cầu content: co_hoc → con_muoi → be_viet → chi_brand → dao_dien → be_dang → be_quan
- Yêu cầu campaign plan: co_hoc → co_chien → con_muoi → be_viet → chi_brand → dao_dien → be_dang → be_quan
- Luôn bắt đầu bằng co_hoc để có keyword foundation, luôn kết thúc bằng be_quan để có lịch và KPI."""

def get_customer_insights():
    """Load market research insights from file"""
    candidates = [
        Path("C:/Users/tomng/Downloads/Ai Agentcy for 2M Construction/CUSTOMER_INSIGHTS.md"),
        Path(__file__).parent / "CUSTOMER_INSIGHTS.md",
        Path("./CUSTOMER_INSIGHTS.md"),
    ]
    for p in candidates:
        if p.exists():
            return p.read_text(encoding="utf-8")
    return ""

def get_seo_guidelines():
    """Load SEO guidelines from file"""
    candidates = [
        Path("C:/Users/tomng/Downloads/Ai Agentcy for 2M Construction/SEO_GUIDELINES.md"),
        Path(__file__).parent / "SEO_GUIDELINES.md",
        Path("./SEO_GUIDELINES.md"),
    ]
    for p in candidates:
        if p.exists():
            return p.read_text(encoding="utf-8")
    return ""

def get_company_ctx():
    insights = get_customer_insights()
    seo = get_seo_guidelines()
    ctx = f"""
CÔNG TY: {COMPANY['name']} — {COMPANY['type']}
ĐỊA BÀN: {COMPANY['location']} | Phục vụ: {COMPANY['service_area']}
SỐ ĐT: {COMPANY['phone']} | CHỦ: {COMPANY['owner']}
DỊCH VỤ: {' · '.join(COMPANY['services'])}
THƯƠNG HIỆU: {COMPANY['brand_colors']}
TONE: {COMPANY['tone']}
QUY TẮC 1: {COMPANY['rule_1']}
QUY TẮC 2: {COMPANY['rule_2']}
QUY TẮC 3: {COMPANY['rule_3']}
"""
    if insights:
        ctx += f"""
===NGHIÊN CỨU THỊ TRƯỜNG & HỒ SƠ KHÁCH HÀNG===
{insights}
"""
    if seo:
        ctx += f"""
===SEO GUIDELINES — BẮT BUỘC ÁP DỤNG===
{seo}
"""
    return ctx


# =============================================================
# FACEBOOK & INSTAGRAM API
# =============================================================
FB_GRAPH = "https://graph.facebook.com/v19.0"

def get_social_creds():
    return {
        "fb_token":   os.environ.get("FB_PAGE_ACCESS_TOKEN", ""),
        "fb_page_id": os.environ.get("FB_PAGE_ID", ""),
        "ig_user_id": os.environ.get("IG_BUSINESS_ACCOUNT_ID", ""),
    }

def auto_detect_ig():
    """Tự động lấy IG Business Account ID nếu chưa có nhưng FB đã kết nối."""
    if os.environ.get("IG_BUSINESS_ACCOUNT_ID"):
        return  # đã có rồi
    token = os.environ.get("FB_PAGE_ACCESS_TOKEN", "")
    page_id = os.environ.get("FB_PAGE_ID", "")
    if not token or not page_id:
        return
    try:
        r = requests.get(
            f"{FB_GRAPH}/{page_id}",
            params={"access_token": token, "fields": "instagram_business_account"},
            timeout=5
        )
        ig_id = r.json().get("instagram_business_account", {}).get("id", "")
        if ig_id:
            import re as _re
            os.environ["IG_BUSINESS_ACCOUNT_ID"] = ig_id
            _env_path = Path(__file__).parent / ".env"
            try:
                _ec = _env_path.read_text(encoding="utf-8")
                _p = r"^IG_BUSINESS_ACCOUNT_ID=.*$"
                if _re.search(_p, _ec, _re.MULTILINE):
                    _ec = _re.sub(_p, f"IG_BUSINESS_ACCOUNT_ID={ig_id}", _ec, flags=_re.MULTILINE)
                else:
                    _ec += f"\nIG_BUSINESS_ACCOUNT_ID={ig_id}"
                _env_path.write_text(_ec, encoding="utf-8")
            except Exception:
                pass
    except Exception:
        pass

def clean_text(md_text: str) -> str:
    """Strip markdown for plain-text APIs."""
    import re
    t = re.sub(r"#{1,6} ", "", md_text)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = re.sub(r"`(.+?)`", r"\1", t)
    t = re.sub(r"^- ", "• ", t, flags=re.MULTILINE)
    return t.strip()

def fb_post_now(page_id: str, token: str, message: str, image_url: str = "") -> dict:
    """Post to Facebook Page immediately."""
    if image_url:
        url = f"{FB_GRAPH}/{page_id}/photos"
        data = {"url": image_url, "caption": message, "access_token": token}
    else:
        url = f"{FB_GRAPH}/{page_id}/feed"
        data = {"message": message, "access_token": token}
    r = requests.post(url, data=data, timeout=30)
    return r.json()

def fb_schedule(page_id: str, token: str, message: str,
                schedule_dt: datetime, image_url: str = "") -> dict:
    """Schedule a Facebook post (min 10 min, max 30 days ahead)."""
    import calendar
    ts = int(calendar.timegm(schedule_dt.utctimetuple()))
    if image_url:
        url = f"{FB_GRAPH}/{page_id}/photos"
        data = {"url": image_url, "caption": message,
                "scheduled_publish_time": ts, "published": "false",
                "access_token": token}
    else:
        url = f"{FB_GRAPH}/{page_id}/feed"
        data = {"message": message, "published": "false",
                "scheduled_publish_time": ts, "access_token": token}
    r = requests.post(url, data=data, timeout=30)
    return r.json()

def ig_post_now(ig_user_id: str, token: str, caption: str, image_url: str) -> dict:
    """Post to Instagram Business account (image required)."""
    if not image_url:
        return {"error": "Instagram requires an image URL"}
    # Step 1 – create container
    r1 = requests.post(
        f"{FB_GRAPH}/{ig_user_id}/media",
        data={"image_url": image_url, "caption": caption, "access_token": token},
        timeout=30
    )
    d1 = r1.json()
    if "id" not in d1:
        return d1
    # Step 2 – publish
    r2 = requests.post(
        f"{FB_GRAPH}/{ig_user_id}/media_publish",
        data={"creation_id": d1["id"], "access_token": token},
        timeout=30
    )
    return r2.json()

def ig_schedule(ig_user_id: str, token: str, caption: str,
                image_url: str, schedule_dt: datetime) -> dict:
    """Schedule Instagram post via container (image required)."""
    if not image_url:
        return {"error": "Instagram requires an image URL"}
    import calendar
    ts = int(calendar.timegm(schedule_dt.utctimetuple()))
    r1 = requests.post(
        f"{FB_GRAPH}/{ig_user_id}/media",
        data={"image_url": image_url, "caption": caption,
              "scheduled_publish_time": ts, "published": "false",
              "access_token": token},
        timeout=30
    )
    d1 = r1.json()
    if "id" not in d1:
        return d1
    return {"scheduled": True, "creation_id": d1["id"],
            "publish_at": schedule_dt.strftime("%d/%m/%Y %H:%M CST")}

def test_fb_token(page_id: str, token: str) -> bool:
    """Verify token is valid and has publish permission."""
    if not page_id or not token:
        return False
    r = requests.get(f"{FB_GRAPH}/{page_id}",
                     params={"fields": "name", "access_token": token}, timeout=10)
    return "name" in r.json()

# =============================================================
# 2MHUNTSVILLE.COM WEBSITE API  (Next.js + GitHub backend)
# =============================================================
import base64 as _b64

SITE_URL      = "https://www.2mhuntsville.com"
SITE_API_BLOG = f"{SITE_URL}/api/admin/blog"

def _site_token() -> str:
    """Build base64 auth token from SITE_ADMIN_PASSWORD env var."""
    pw = os.environ.get("SITE_ADMIN_PASSWORD", "")
    return _b64.b64encode(pw.encode()).decode() if pw else ""

def site_connected() -> bool:
    return bool(os.environ.get("SITE_ADMIN_PASSWORD", ""))

def site_post(title: str, content_md: str, excerpt: str = "",
              tags: list = None, slug: str = "", published: bool = False,
              meta_title: str = "", meta_description: str = "",
              cover_image_url: str = "") -> dict:
    """
    Create or update a blog post on 2mhuntsville.com via the admin API.
    Content must be Markdown.
    """
    token = _site_token()
    if not token:
        return {"error": "SITE_ADMIN_PASSWORD not set"}
    headers = {
        "x-admin-token": token,
        "Content-Type":  "application/json",
    }
    if not slug:
        slug = title.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    body = {
        "title":           title,
        "slug":            slug,
        "excerpt":         excerpt,
        "content":         content_md,
        "coverImageUrl":   cover_image_url,
        "tags":            tags or [],
        "metaTitle":       meta_title or title,
        "metaDescription": meta_description or excerpt,
        "published":       published,
    }
    try:
        r = requests.post(SITE_API_BLOG, json=body, headers=headers, timeout=20)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def site_list_posts() -> list:
    """Fetch all blog posts from 2mhuntsville.com admin API."""
    token = _site_token()
    if not token:
        return []
    try:
        r = requests.get(SITE_API_BLOG,
                         headers={"x-admin-token": token}, timeout=15)
        return r.json().get("posts", [])
    except Exception:
        return []

# ── Backward-compat shims (WordPress functions kept for reference) ──
def get_wp_creds():
    return {"url": "", "user": "", "password": ""}
def wp_connected() -> bool:
    return False

def wp_post(title: str, html_content: str, excerpt: str = "",
            tags: list = None, categories: list = None,
            slug: str = "", status: str = "draft",
            yoast_title: str = "", yoast_desc: str = "",
            focus_kw: str = "", schedule_dt=None) -> dict:
    """
    Publish or schedule a post to WordPress via REST API.
    Uses Application Password auth (WP 5.6+).
    status: 'publish' | 'draft' | 'future'
    """
    import base64, re
    c = get_wp_creds()
    if not c["url"]:
        return {"error": "WP_SITE_URL not set"}

    token = base64.b64encode(f"{c['user']}:{c['password']}".encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }

    # Auto-generate slug from title if not given
    if not slug:
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]

    payload = {
        "title":   title,
        "content": html_content,
        "excerpt": excerpt,
        "slug":    slug,
        "status":  status,
    }
    if tags:
        payload["tags_input"] = tags          # plain names
    if categories:
        payload["categories_names"] = categories
    if schedule_dt and status == "future":
        payload["date"] = schedule_dt.strftime("%Y-%m-%dT%H:%M:%S")

    # Yoast SEO meta (requires Yoast plugin)
    if yoast_title or yoast_desc or focus_kw:
        payload["meta"] = {
            "_yoast_wpseo_title":    yoast_title or title,
            "_yoast_wpseo_metadesc": yoast_desc,
            "_yoast_wpseo_focuskw":  focus_kw,
        }

    endpoint = f"{c['url']}/wp-json/wp/v2/posts"
    try:
        r = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        data = r.json()
        if r.status_code in (200, 201):
            return {"id": data.get("id"), "link": data.get("link"), "status": data.get("status")}
        return {"error": data.get("message", f"HTTP {r.status_code}"), "raw": data}
    except Exception as e:
        return {"error": str(e)}

def extract_blog_sections(be_quan_output: str) -> dict:
    """
    Parse Bé Quản output to extract blog post fields.
    Returns dict with keys: title, slug, meta_desc, html, yoast_title, focus_kw, tags, schedule_str
    """
    import re
    txt = be_quan_output

    def _between(start_marker, end_marker, fallback=""):
        m = re.search(re.escape(start_marker) + r"(.*?)" + re.escape(end_marker),
                      txt, re.DOTALL)
        return m.group(1).strip() if m else fallback

    def _line_val(key):
        m = re.search(rf"(?i){re.escape(key)}\s*[:：]\s*(.+)", txt)
        return m.group(1).strip() if m else ""

    html_block = _between("=== NỘI DUNG HTML ===", "=== YOAST SEO FIELDS ===")
    if not html_block:
        html_block = _between("=== BLOG POST FOR WEBSITE ===", "=== YOAST SEO FIELDS ===")
    if not html_block:
        # Fallback: use full output as plain HTML paragraphs
        nl = "\n"
        paras = [f"<p>{l.strip()}</p>" for l in txt.splitlines() if len(l.strip()) > 30]
        html_block = nl.join(paras[:20])

    title      = _line_val("TITLE (SEO)") or _line_val("TITLE") or "2M Construction — Huntsville AL"
    slug       = _line_val("SLUG") or ""
    meta_desc  = _line_val("META DESCRIPTION") or _line_val("META")
    focus_kw   = _line_val("FOCUS KEYWORD") or _line_val("KEYWORD")
    sched_str  = _line_val("SCHEDULE")
    tags_raw   = _line_val("TAGS")
    tags       = [t.strip().strip('"') for t in tags_raw.split(",") if t.strip()] if tags_raw else []
    yoast_title = _line_val("SEO Title") or title

    return {
        "title":       title,
        "slug":        slug,
        "meta_desc":   meta_desc,
        "html":        html_block,
        "yoast_title": yoast_title,
        "focus_kw":    focus_kw,
        "tags":        tags,
        "schedule_str": sched_str,
    }



# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="2M Marketing Agency AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* === DARK THEME === */
.stApp { background:#0d1526 !important; color:#c8d4e8; font-family:'Segoe UI',system-ui,sans-serif; }
section[data-testid="stSidebar"] { background:#141f35 !important; border-right:1px solid rgba(201,168,76,.2); }
.stTextInput input, .stTextArea textarea {
    background:#1a2844 !important; color:#c8d4e8 !important;
    border:1px solid rgba(201,168,76,.3) !important; border-radius:8px !important;
}
.stButton button { border-radius:8px !important; font-weight:700 !important; }
.stButton button[kind="primary"] {
    background:linear-gradient(135deg,#C9A84C,#e0c06a) !important;
    color:#111c33 !important; border:none !important;
}
/* Hide footer */
#MainMenu, footer, header { visibility:hidden; }
/* Agent boxes */
div[data-testid="stExpander"] {
    background:#141f35 !important; border:1px solid rgba(201,168,76,.2) !important;
    border-radius:10px !important; margin-bottom:8px;
}
/* Progress */
.stProgress > div > div { background:linear-gradient(90deg,#1B2A4A,#C9A84C) !important; }
/* Sidebar text */
.sidebar-metric { display:flex; justify-content:space-between; padding:5px 0;
    border-bottom:1px solid rgba(136,146,164,.1); font-size:13px; }
.metric-val { color:#C9A84C; font-weight:700; }
/* Status badges */
.badge-online { background:rgba(46,204,113,.15); color:#2ecc71; padding:2px 10px;
    border-radius:12px; font-size:11px; border:1px solid rgba(46,204,113,.3); }
.badge-wait { background:rgba(201,168,76,.15); color:#C9A84C; padding:2px 10px;
    border-radius:12px; font-size:11px; border:1px solid rgba(201,168,76,.3); }
.title-gold { color:#C9A84C; font-size:22px; font-weight:800; margin:0; }
.sub-gray { color:#8892a4; font-size:13px; margin:2px 0 16px; }
hr { border-color:rgba(201,168,76,.15) !important; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───────────────────────────────────
with st.sidebar:
    st.markdown('<p class="title-gold">🏗️ 2M Agency AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-gray">2M Construction LLC · Huntsville, AL</p>', unsafe_allow_html=True)

    _env_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if "api_key" not in st.session_state or not st.session_state["api_key"]:
        st.session_state["api_key"] = _env_key
    api_key = st.text_input(
        "🔑 Anthropic API Key",
        type="password",
        value=st.session_state["api_key"],
        help="Lấy tại: console.anthropic.com/keys",
        key="api_key_input"
    )
    # Update session state
    st.session_state["api_key"] = api_key or _env_key
    api_key = st.session_state["api_key"]
    if api_key:
        st.markdown('<span class="badge-online">✓ API Key sẵn sàng</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-wait">⚠ Chưa có API Key</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"**🤖 {len(AGENTS)} Agents Online**")
    for aid, a in AGENTS.items():
        st.markdown(f'{a["emoji"]} **{a["name"]}** — {a["role"]}')

    st.markdown("---")
    st.markdown("**📋 Company**")
    st.markdown(f'📞 {COMPANY["phone"]}')
    st.markdown(f'📍 {COMPANY["location"]}')

    st.markdown("---")
    # FB / IG connection status — auto-detect IG if needed
    auto_detect_ig()
    _creds = get_social_creds()
    _fb_ok = bool(_creds["fb_token"] and _creds["fb_page_id"])
    _ig_ok = bool(_creds["fb_token"] and _creds["ig_user_id"])
    st.markdown("**📡 Kết nối mạng xã hội**")
    if _fb_ok:
        st.markdown('<span class="badge-online">📘 Facebook ✓ Đã kết nối</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-wait">📘 Facebook ✗ Chưa kết nối</span>', unsafe_allow_html=True)
    if _ig_ok:
        st.markdown('<span class="badge-online">📸 Instagram ✓ Đã kết nối</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-wait">📸 Instagram ✗ Chưa kết nối</span>', unsafe_allow_html=True)

    _exp_label_fb = "✓ Cài đặt FB/IG" if _fb_ok else "⚙️ Kết nối Facebook & Instagram"
    with st.expander(_exp_label_fb, expanded=(not _fb_ok)):
        _fb_token_in = st.text_input("🔑 Page Access Token",
            value=_creds["fb_token"] or "", type="password",
            key="fb_token_input", placeholder="EAAxxxxx...")
        _fb_page_in = st.text_input("📘 Facebook Page ID",
            value=_creds["fb_page_id"] or "",
            key="fb_page_input", placeholder="123456789012345")
        _ig_id_in = st.text_input("📸 IG Business Account ID",
            value=_creds["ig_user_id"] or "",
            key="ig_id_input", placeholder="987654321012345")

        _sc1, _sc2 = st.columns(2)
        with _sc1:
            if st.button("💾 Lưu", use_container_width=True, key="fb_save_btn"):
                import re as _re
                _env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
                try:
                    with open(_env_path, "r", encoding="utf-8") as _f:
                        _ec = _f.read()
                    def _set_ev(c, k, v):
                        p = rf"^{k}=.*$"
                        return _re.sub(p, f"{k}={v}", c, flags=_re.MULTILINE) if _re.search(p, c, _re.MULTILINE) else c + f"\n{k}={v}"
                    _ec = _set_ev(_ec, "FB_PAGE_ACCESS_TOKEN", _fb_token_in.strip())
                    _ec = _set_ev(_ec, "FB_PAGE_ID", _fb_page_in.strip())
                    _ec = _set_ev(_ec, "IG_BUSINESS_ACCOUNT_ID", _ig_id_in.strip())
                    with open(_env_path, "w", encoding="utf-8") as _f:
                        _f.write(_ec)
                    os.environ["FB_PAGE_ACCESS_TOKEN"] = _fb_token_in.strip()
                    os.environ["FB_PAGE_ID"] = _fb_page_in.strip()
                    os.environ["IG_BUSINESS_ACCOUNT_ID"] = _ig_id_in.strip()
                    st.success("✓ Đã lưu!")
                    st.rerun()
                except Exception as _e:
                    st.error(f"Lỗi: {_e}")
        with _sc2:
            if st.button("🔍 Test", use_container_width=True, key="fb_test_btn"):
                _tk = (_fb_token_in or _creds["fb_token"]).strip()
                _pid = (_fb_page_in or _creds["fb_page_id"]).strip()
                if _tk and _pid:
                    try:
                        _r = requests.get(f"{FB_GRAPH}/{_pid}",
                            params={"access_token": _tk, "fields": "name,fan_count"}, timeout=10)
                        if _r.status_code == 200:
                            _d = _r.json()
                            st.success(f"✓ {_d.get('name')} ({_d.get('fan_count',0):,} fans)")
                        else:
                            st.error(_r.json().get("error", {}).get("message", f"HTTP {_r.status_code}"))
                    except Exception as _e:
                        st.error(str(_e))
                else:
                    st.warning("Nhập token và Page ID trước")

        with st.expander("📖 Cách lấy token (5 phút)"):
            st.markdown("""
**Bước 1:** Vào [Graph API Explorer](https://developers.facebook.com/tools/explorer/)  
**Bước 2:** Chọn Meta App → **Generate Access Token**  
**Bước 3:** Tick các quyền:
- `pages_show_list` ✓  
- `pages_read_engagement` ✓  
- `pages_manage_posts` ✓  
- `instagram_basic` ✓  
- `instagram_content_publish` ✓  

**Bước 4:** Copy token → dán vào ô "Page Access Token" trên  
**Bước 5:** **Page ID**: Vào Facebook Page → About → Page ID  
**Bước 6:** **IG ID**: Instagram Settings → About → Account type & ID
            """)

        with st.expander("⚡ Tự động lấy token dài hạn"):
            st.markdown("Nhập App credentials → App tự lấy token 60 ngày + Page ID + IG ID:")
            _app_id_in = st.text_input("App ID", key="fb_app_id", placeholder="123456789")
            _app_sec_in = st.text_input("App Secret", key="fb_app_secret", type="password", placeholder="abc123...")
            _short_tok_in = st.text_input("User Token (từ Graph Explorer)", key="fb_short_tok", type="password", placeholder="EAAxxxxx")
            if st.button("🔄 Lấy token dài hạn", key="fb_exchange_btn", use_container_width=True):
                if _app_id_in and _app_sec_in and _short_tok_in:
                    try:
                        _r1 = requests.get(f"{FB_GRAPH}/oauth/access_token", params={
                            "grant_type": "fb_exchange_token",
                            "client_id": _app_id_in.strip(),
                            "client_secret": _app_sec_in.strip(),
                            "fb_exchange_token": _short_tok_in.strip()
                        }, timeout=15)
                        if _r1.status_code != 200:
                            st.error(f"Lỗi exchange: {_r1.json().get('error', {}).get('message', 'Lỗi token')}")
                        else:
                            _ll_token = _r1.json()["access_token"]
                            _r2 = requests.get(f"{FB_GRAPH}/me/accounts",
                                params={"access_token": _ll_token, "fields": "name,id,access_token"}, timeout=15)
                            if _r2.status_code == 200:
                                _pages = _r2.json().get("data", [])
                                if _pages:
                                    _pg = _pages[0]
                                    _page_token = _pg["access_token"]
                                    _page_id = _pg["id"]
                                    _page_name = _pg["name"]
                                    _r3 = requests.get(f"{FB_GRAPH}/{_page_id}",
                                        params={"access_token": _page_token,
                                                "fields": "instagram_business_account"}, timeout=15)
                                    _ig_id_auto = ""
                                    if _r3.status_code == 200:
                                        _ig_id_auto = _r3.json().get("instagram_business_account", {}).get("id", "")
                                    import re as _re2
                                    _env_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
                                    with open(_env_path2, "r", encoding="utf-8") as _f2:
                                        _ec2 = _f2.read()
                                    def _sev2(c, k, v):
                                        p = rf"^{k}=.*$"
                                        return _re2.sub(p, f"{k}={v}", c, flags=_re2.MULTILINE) if _re2.search(p, c, _re2.MULTILINE) else c + f"\n{k}={v}"
                                    _ec2 = _sev2(_ec2, "FB_PAGE_ACCESS_TOKEN", _page_token)
                                    _ec2 = _sev2(_ec2, "FB_PAGE_ID", _page_id)
                                    if _ig_id_auto:
                                        _ec2 = _sev2(_ec2, "IG_BUSINESS_ACCOUNT_ID", _ig_id_auto)
                                    with open(_env_path2, "w", encoding="utf-8") as _f2:
                                        _f2.write(_ec2)
                                    os.environ["FB_PAGE_ACCESS_TOKEN"] = _page_token
                                    os.environ["FB_PAGE_ID"] = _page_id
                                    if _ig_id_auto:
                                        os.environ["IG_BUSINESS_ACCOUNT_ID"] = _ig_id_auto
                                    _msg = f"✓ **{_page_name}** (Page ID: {_page_id})"
                                    if _ig_id_auto:
                                        _msg += f"\n✓ IG Account ID: {_ig_id_auto}"
                                    st.success(_msg)
                                    st.rerun()
                                else:
                                    st.error("Không tìm thấy Page nào trong tài khoản")
                            else:
                                st.error(f"Lỗi lấy pages: {_r2.json()}")
                    except Exception as _e:
                        st.error(str(_e))
                else:
                    st.warning("Nhập đủ App ID, App Secret và User Token")
    st.markdown("---")
    # WP / Website connection status
    _wp_ok = site_connected()
    st.markdown("**🌐 Kết nối Website**")
    if _wp_ok:
        st.markdown('<span class="badge-online">🌐 2mhuntsville.com ✓ Đã kết nối</span>', unsafe_allow_html=True)
        st.caption("🔗 www.2mhuntsville.com")
    else:
        st.markdown('<span class="badge-wait">🌐 Website ✗ Chưa kết nối</span>', unsafe_allow_html=True)

    with st.expander("⚙️ Cài đặt Website" + (" ✓" if _wp_ok else "")):
        _site_pw_in = st.text_input("🔑 Admin Password", value=os.environ.get("SITE_ADMIN_PASSWORD",""),
                                    key="site_pw_input", placeholder="2M@Huntsville#2026",
                                    type="password")
        _wc1, _wc2 = st.columns(2)
        with _wc1:
            if st.button("💾 Lưu", use_container_width=True, key="wp_save_btn"):
                import re as _re2
                _env_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
                try:
                    with open(_env_path2, "r", encoding="utf-8") as _f2:
                        _ec2 = _f2.read()
                    def _set_ev2(c, k, v):
                        p = rf"^{k}=.*$"
                        return _re2.sub(p, f"{k}={v}", c, flags=_re2.MULTILINE) if _re2.search(p, c, _re2.MULTILINE) else c + f"\n{k}={v}"
                    _ec2 = _set_ev2(_ec2, "SITE_ADMIN_PASSWORD", _site_pw_in.strip())
                    with open(_env_path2, "w", encoding="utf-8") as _f2:
                        _f2.write(_ec2)
                    os.environ["SITE_ADMIN_PASSWORD"] = _site_pw_in.strip()
                    st.success("✓ Đã lưu!")
                    st.rerun()
                except Exception as _e2:
                    st.error(f"Lỗi: {_e2}")
        with _wc2:
            if st.button("🔍 Test", use_container_width=True, key="wp_test_btn"):
                _pw = (_site_pw_in or os.environ.get("SITE_ADMIN_PASSWORD","")).strip()
                if _pw:
                    try:
                        import base64 as _b64t
                        _tok = _b64t.b64encode(_pw.encode()).decode()
                        _wr = requests.get(SITE_API_BLOG,
                            headers={"x-admin-token": _tok}, timeout=10)
                        if _wr.status_code == 200:
                            st.success(f"✓ Kết nối 2mhuntsville.com thành công!")
                        else:
                            st.error(f"Lỗi {_wr.status_code}: Sai password")
                    except Exception as _e3:
                        st.error(str(_e3))
                else:
                    st.warning("Nhập admin password")
        st.caption("🔗 Website: www.2mhuntsville.com/admin")
    st.markdown("---")
    auto_save = st.checkbox("💾 Tự động lưu file", value=True)
    show_detail = st.checkbox("📖 Xem từng agent", value=True)

# ─── MAIN ──────────────────────────────────────
col_title, col_time = st.columns([3, 1])
with col_title:
    hr = datetime.now().hour
    greet = "Good morning" if hr < 12 else "Good afternoon" if hr < 18 else "Good evening"
    st.markdown(f'<p class="title-gold">{greet}, Anh Tuan 👋</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-gray">2M Marketing Agency AI — Gõ 1 lệnh, hệ thống tự chạy tất cả</p>', unsafe_allow_html=True)
with col_time:
    st.markdown(f'<div style="text-align:right;color:#8892a4;font-size:12px;padding-top:8px">{datetime.now().strftime("%d/%m/%Y %H:%M")}</div>', unsafe_allow_html=True)

st.markdown("---")

# ─── COMMAND BAR ───────────────────────────────

def get_weekly_commands() -> list:
    """
    Tạo lệnh nhanh động theo tuần hiện tại.
    Đọc từ WEEKLY_PLAN.md nếu có, nếu không tự sinh theo lịch xoay vòng.
    """
    from datetime import date
    week_num = date.today().isocalendar()[1]
    month    = date.today().month
    day_name = ["Thứ 2","Thứ 3","Thứ 4","Thứ 5","Thứ 6","Thứ 7","CN"][date.today().weekday()]

    # Đọc WEEKLY_PLAN.md nếu tồn tại
    plan_candidates = [
        Path("C:/Users/tomng/Downloads/Ai Agentcy for 2M Construction/WEEKLY_PLAN.md"),
        Path(__file__).parent / "WEEKLY_PLAN.md",
    ]
    plan_text = ""
    for p in plan_candidates:
        if p.exists():
            plan_text = p.read_text(encoding="utf-8")
            break

    # Nếu có plan → đưa vào prompt để sinh lệnh
    if plan_text:
        # Trả về gợi ý dựa trên plan (parsed thủ công đơn giản)
        lines = [l.strip() for l in plan_text.splitlines() if l.strip() and not l.startswith("#")]
        cmds = [l.lstrip("-•* ") for l in lines if len(l) > 20][:6]
        if cmds:
            return cmds

    # Fallback: xoay vòng theo tuần + mùa
    season_services = {
        (3,4,5):   ["epoxy garage floor","deck & patio","fence","concrete driveway","exterior painting"],
        (6,7,8):   ["epoxy garage floor","deck & patio","concrete","flooring","cabinet refacing"],
        (9,10,11): ["kitchen cabinet","interior painting","flooring","drywall","bathroom tile"],
        (12,1,2):  ["interior painting","flooring","kitchen remodel","drywall repair","cabinet refacing"],
    }
    services = ["epoxy garage floor","deck & patio","fence","flooring","kitchen cabinet","concrete"]
    for months, svcs in season_services.items():
        if month in months:
            services = svcs
            break

    svc1 = services[(week_num) % len(services)]
    svc2 = services[(week_num + 1) % len(services)]
    svc3 = services[(week_num + 2) % len(services)]

    week_label = f"Tuần {week_num}"
    return [
        f"[{week_label}] Tạo content Facebook + Instagram về dịch vụ {svc1} tại Huntsville AL — SEO tốt, có lịch đăng",
        f"[{week_label}] Viết bài Nextdoor giới thiệu dịch vụ {svc1} cho khu Madison & Harvest",
        f"[{week_label}] Soạn 2 bài: before/after {svc1} và tips chọn nhà thầu uy tín Huntsville",
        f"[{week_label}] Tạo content {svc2} với keyword quick-win cho Huntsville AL + lịch đăng cả tuần",
        f"[{week_label}] Viết bài Google Business Post về {svc2} — tối ưu SEO local map pack",
        f"[{week_label}] Lập báo cáo hiệu quả marketing tuần {week_num-1} và kế hoạch tuần {week_num} cho dịch vụ {svc3}",
    ]

st.markdown("### ⌘ Ra Lệnh Cho Agency")

# Callback: khi chọn lệnh nhanh → tự điền vào ô lệnh
def _on_quick_select():
    val = st.session_state.get("quick_select_box", "")
    if val and val != "— Chọn lệnh tuần này —":
        # Dùng _pending_fill (non-widget key) — Streamlit không cho phép
        # set widget key từ callback widget khác
        st.session_state["_pending_fill"] = val
        st.session_state["trigger_run"] = True

weekly_cmds = get_weekly_commands()

from datetime import date as _date
_wk = _date.today().isocalendar()[1]
st.selectbox(
    f"⚡ Lệnh nhanh tuần {_wk} (chọn → tự điền + chạy ngay):",
    ["— Chọn lệnh tuần này —"] + weekly_cmds,
    key="quick_select_box",
    on_change=_on_quick_select,
)

# Áp dụng pending fill TRƯỚC khi text_area render (Streamlit cho phép set widget key trước render)
if "_pending_fill" in st.session_state:
    st.session_state["main_cmd_ta"] = st.session_state.pop("_pending_fill")

command = st.text_area(
    "✏️ Hoặc nhập lệnh tùy chỉnh:",
    placeholder="VD: Tạo content Facebook tuần này về dịch vụ epoxy garage mùa hè...",
    height=80,
    key="main_cmd_ta",
)
# Đọc giá trị hiện tại
command = st.session_state.get("main_cmd_ta", "")

# Detect auto-run trigger from quick select
_trigger = st.session_state.pop("trigger_run", False)

run_col, clear_col = st.columns([1, 4])
with run_col:
    run_btn = st.button("🚀 Chạy Agency", type="primary", use_container_width=True)
with clear_col:
    if st.button("🗑️ Xóa lệnh", use_container_width=False):
        st.session_state["main_cmd_ta"] = ""
        st.rerun()

# Auto-run if triggered from quick select
if _trigger and st.session_state.get("main_cmd_ta", ""):
    run_btn = True

# ─────────────────────────────────────────────
# ORCHESTRATION ENGINE
# ─────────────────────────────────────────────
def parse_cmo_json(text: str) -> dict:
    """Extract JSON from CMO response — robust parser"""
    import re
    text = text.strip()
    # Strip markdown code fences
    for marker in ["```json", "```"]:
        if marker in text:
            text = text.split(marker)[1].split("```")[0].strip()
            break
    # Find first { and last }
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        text = text[start:end]
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Try fixing common issues: replace smart quotes, strip trailing commas
    text_fixed = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    text_fixed = re.sub(r',\s*}', '}', text_fixed)
    text_fixed = re.sub(r',\s*]', ']', text_fixed)
    try:
        return json.loads(text_fixed)
    except json.JSONDecodeError:
        pass
    # Fallback: extract key fields with regex
    def rx(key):
        m = re.search(rf'"{key}"\s*:\s*"([^"]*)"', text)
        return m.group(1) if m else ""
    agents_m = re.search(r'"agents"\s*:\s*\[([^\]]+)\]', text)
    agents = re.findall(r'"(\w+)"', agents_m.group(1)) if agents_m else ["co_chien","con_muoi","be_viet","chi_brand","dao_dien","be_dang"]
    briefs = {}
    briefs_m = re.search(r'"briefs"\s*:\s*\{([^}]+)\}', text, re.DOTALL)
    if briefs_m:
        for am in re.finditer(r'"(\w+)"\s*:\s*"([^"]*)"', briefs_m.group(1)):
            briefs[am.group(1)] = am.group(2)
    for a in agents:
        if a not in briefs:
            briefs[a] = rx("analysis") or "Tạo content marketing cho 2M Construction"
    return {
        "analysis": rx("analysis") or "Phân tích lệnh từ Anh Tuan",
        "campaign_name": rx("campaign_name") or "2M Campaign",
        "agents": agents,
        "briefs": briefs
    }

def call_agent(client: anthropic.Anthropic, agent_id: str, brief: str, context: str) -> str:
    agent = AGENTS[agent_id]
    system = agent["soul"] + "\n\n===COMPANY INFO===\n" + get_company_ctx()
    user_msg = f"NHIỆM VỤ: {brief}"
    if context.strip():
        user_msg += f"\n\n===BỐI CẢNH TỪ CÁC AGENT TRƯỚC===\n{context}"
    resp = client.messages.create(
        model=agent["model"],
        max_tokens=2500,
        system=system,
        messages=[{"role": "user", "content": user_msg}]
    )
    return resp.content[0].text

def call_cmo(client: anthropic.Anthropic, command: str) -> dict:
    system = CMO_SOUL + "\n\n===COMPANY INFO===\n" + get_company_ctx()
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        system=system,
        messages=[{"role": "user", "content": f'Lệnh từ Anh Tuan: "{command}"'}]
    )
    return parse_cmo_json(resp.content[0].text)

BASE_DIR = Path("C:/Users/tomng/Downloads/Ai Agentcy for 2M Construction")

def get_base_dir() -> Path:
    """Trả về thư mục gốc của dự án"""
    candidates = [BASE_DIR, Path(__file__).parent, Path(".")]
    for p in candidates:
        if p.exists():
            return p
    return Path(".")

def save_output(campaign_name: str, full_md: str) -> str | None:
    try:
        base = get_base_dir() / "CAMPAIGNS"
        base.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d_%H%M")
        safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in campaign_name)[:35].strip()
        folder = base / f"{ts}_{safe}"
        folder.mkdir(exist_ok=True)
        out = folder / "CAMPAIGN_OUTPUT.md"
        out.write_text(full_md, encoding="utf-8")
        return str(folder)
    except Exception:
        return None

def approve_and_distribute(campaign_name: str, outputs: dict, agents_ran: list) -> dict:
    """
    Khi Anh Tuan bấm PHÊ DUYỆT:
    - Tách content theo platform
    - Lưu vào thư mục PUBLISH_QUEUE/[platform]/
    - Cập nhật QUEUE.md
    Trả về dict {platform: filepath}
    """
    results = {}
    try:
        ts = datetime.now().strftime("%Y-%m-%d_%H%M")
        safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in campaign_name)[:30].strip()
        queue_base = get_base_dir() / "PUBLISH_QUEUE"
        queue_base.mkdir(exist_ok=True)

        # Nội dung từng platform lấy từ Bé Đăng (be_dang) + Bé Quản (be_quan)
        be_dang_output = outputs.get("be_dang", "")
        be_quan_output = outputs.get("be_quan", "")
        be_viet_output = outputs.get("be_viet", "")
        co_hoc_output  = outputs.get("co_hoc", "")

        # === FACEBOOK ===
        fb_dir = queue_base / "FACEBOOK"
        fb_dir.mkdir(exist_ok=True)
        fb_content = (
            "# FACEBOOK -- " + campaign_name + "\n" +
            "Ngay phe duyet: " + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n" +
            "Trang thai: CHO DANG\n\n" +
            "CACH DANG:\n" +
            "1. Vao facebook.com -> Trang 2M Construction LLC\n" +
            "2. Nhan 'Tao bai viet' -> Copy noi dung ben duoi\n" +
            "3. Dinh kem anh (xem huong dan Dao Dien)\n" +
            "4. Chon 'Len lich' -> Thu 4 hoac Thu 6, 11am-1pm CST\n" +
            "5. Nhan 'Len lich bai viet'\n\n" +
            "NOI DUNG:\n" + be_viet_output + "\n\n" +
            "LICH & KPI:\n" + be_quan_output + "\n"
        )
        fb_file = fb_dir / f"{ts}_{safe}_FACEBOOK.txt"
        fb_file.write_text(fb_content, encoding="utf-8")
        results["Facebook"] = str(fb_file)

        # === INSTAGRAM ===
        ig_dir = queue_base / "INSTAGRAM"
        ig_dir.mkdir(exist_ok=True)
        ig_content = (
            "# INSTAGRAM -- " + campaign_name + "\n" +
            "Ngay phe duyet: " + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n" +
            "Trang thai: CHO DANG\n\n" +
            "CACH DANG TREN DIEN THOAI:\n" +
            "1. Mo Instagram app -> nhan [+] goc duoi giua\n" +
            "2. Chon anh/video tu thu vien\n" +
            "3. Nhan 'Tiep theo' -> dan caption vao o mo ta\n" +
            "4. Them vi tri: Huntsville, Alabama\n" +
            "5. Dan 30 hashtag vao cuoi caption\n" +
            "6. Nhan 'Chia se'\n" +
            "THOI DIEM TOT NHAT: Thu 3 & Thu 7 luc 8-9am CST\n\n" +
            "NOI DUNG:\n" + be_viet_output + "\n\n" +
            "PUBLISHING PACKAGE:\n" + be_dang_output + "\n"
        )
        ig_file = ig_dir / f"{ts}_{safe}_INSTAGRAM.txt"
        ig_file.write_text(ig_content, encoding="utf-8")
        results["Instagram"] = str(ig_file)

        # === GOOGLE BUSINESS ===
        gb_dir = queue_base / "GOOGLE_BUSINESS"
        gb_dir.mkdir(exist_ok=True)
        gb_content = (
            "# GOOGLE BUSINESS -- " + campaign_name + "\n" +
            "Ngay phe duyet: " + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n" +
            "Trang thai: CHO DANG\n\n" +
            "CACH DANG:\n" +
            "1. Vao business.google.com -> Chon 2M Construction LLC\n" +
            "2. Nhan 'Them bai dang' -> Chon loai: Cap nhat hoac Uu dai\n" +
            "3. Copy noi dung ben duoi vao o mo ta\n" +
            "4. Them anh dep nhat cua du an\n" +
            "5. Nhan nut CTA: 'Goi ngay' -> (938) 302-6795\n" +
            "THOI DIEM TOT NHAT: Thu 2 dau tuan luc 9am CST\n\n" +
            "NOI DUNG:\n" + be_dang_output + "\n"
        )
        gb_file = gb_dir / f"{ts}_{safe}_GOOGLE_BUSINESS.txt"
        gb_file.write_text(gb_content, encoding="utf-8")
        results["Google Business"] = str(gb_file)

        # === NEXTDOOR ===
        nd_dir = queue_base / "NEXTDOOR"
        nd_dir.mkdir(exist_ok=True)
        nd_content = (
            "# NEXTDOOR -- " + campaign_name + "\n" +
            "Ngay phe duyet: " + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n" +
            "Trang thai: CHO DANG\n\n" +
            "CACH DANG:\n" +
            "1. Vao nextdoor.com -> Nhan 'Dang bai' trong neighborhood feed\n" +
            "2. Chon dung khu dan cu (Harvest / Jones Valley / Hampton Cove)\n" +
            "3. Copy noi dung ben duoi (KHONG dung hashtag tren Nextdoor)\n" +
            "4. Dang ngay -- tone hang xom, than thien\n" +
            "THOI DIEM TOT NHAT: Thu 5 luc 6-8pm CST\n\n" +
            "NOI DUNG:\n" + be_viet_output + "\n"
        )
        nd_file = nd_dir / f"{ts}_{safe}_NEXTDOOR.txt"
        nd_file.write_text(nd_content, encoding="utf-8")
        results["Nextdoor"] = str(nd_file)

        # === SEO KEYWORD LIBRARY ===
        if co_hoc_output:
            kw_dir = queue_base / "SEO_KEYWORDS"
            kw_dir.mkdir(exist_ok=True)
            kw_content = ("# KEYWORD LIBRARY -- " + campaign_name + "\n" +
                          "Ngay tao: " + datetime.now().strftime('%d/%m/%Y %H:%M') + "\n\n" +
                          co_hoc_output + "\n")
            kw_file = kw_dir / f"{ts}_{safe}_KEYWORDS.txt"
            kw_file.write_text(kw_content, encoding="utf-8")
            results["SEO Keywords"] = str(kw_file)

        # === MASTER QUEUE LOG ===
        queue_log = queue_base / "QUEUE.md"
        log_entry = ("\n| " + datetime.now().strftime('%d/%m/%Y %H:%M') +
                     " | " + campaign_name + " | PHE DUYET | FB+IG+GB+ND | CHO DANG |")
        with open(queue_log, "a", encoding="utf-8") as f:
            if not queue_log.exists() or queue_log.stat().st_size == 0:
                f.write("# PUBLISH QUEUE -- 2M Construction\n\n")
                f.write("| Ngay | Campaign | Trang thai | Platforms | Dang |\n")
                f.write("|------|----------|-----------|-----------|------|\n")
            f.write(log_entry)

    except Exception as e:
        results["error"] = str(e)

    return results


# =============================================================
# RUN WHEN BUTTON CLICKED
# =============================================================
if run_btn:
    if not command.strip():
        st.warning("Nhap lenh truoc!")
        st.stop()
    if not api_key.strip():
        st.error("Can nhap Anthropic API Key trong sidebar!")
        st.stop()

    client = anthropic.Anthropic(api_key=api_key.strip())
    st.markdown("---")

    # Step 1: CMO
    st.markdown("### Agency dang van hanh...")
    cmo_ph = st.empty()
    cmo_ph.info("**Anh Tong** dang phan tich lenh...")

    try:
        plan = call_cmo(client, command)
    except Exception as e:
        cmo_ph.error(f"Loi CMO: {e}")
        st.stop()

    analysis      = plan.get("analysis", "Da phan tich xong.")
    campaign_name = plan.get("campaign_name", f"Campaign {datetime.now().strftime('%Y-%m-%d')}")
    agents_to_run = [a for a in plan.get("agents", list(AGENTS.keys())) if a in AGENTS]
    briefs        = plan.get("briefs", {})

    cmo_ph.success(f"**Anh Tong:** {analysis}")
    st.markdown(f"**Campaign:** `{campaign_name}` | **Agents:** {len(agents_to_run)}")

    # Step 2: Run agents
    progress_bar = st.progress(0.0, text="Dang chay agents...")
    outputs: dict[str, str] = {}
    placeholders: dict[str, object] = {}
    for aid in agents_to_run:
        placeholders[aid] = st.empty()

    full_md = ("# " + campaign_name + "\n" +
               "Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M') + "\n" +
               "Command: " + command + "\n\n---\n\n" +
               "## ANH TONG (CMO)\n" + analysis + "\n\n")

    for idx, aid in enumerate(agents_to_run):
        agent = AGENTS[aid]
        ph    = placeholders[aid]
        ph.warning(f"{agent['emoji']} **{agent['name']}** dang lam viec...")

        context_parts = [
            f"=== {AGENTS[p]['name']} ({AGENTS[p]['role']}) ===\n{o}"
            for p, o in outputs.items()
        ]
        context = "\n\n".join(context_parts)
        brief   = briefs.get(aid, f"Lam theo yeu cau: {command}")

        try:
            result      = call_agent(client, aid, brief, context)
            outputs[aid] = result
            full_md     += f"---\n\n## {agent['emoji']} {agent['name'].upper()} ({agent['role']})\n\n{result}\n\n"
            ph.success(f"**{agent['name']}** -- Xong!")
        except Exception as e:
            ph.error(f"**{agent['name']}** loi: {e}")
            outputs[aid] = f"[Loi: {e}]"

        progress_bar.progress(
            (idx + 1) / len(agents_to_run),
            text=f"Dang chay {agent['name']}... ({idx+1}/{len(agents_to_run)})"
        )

    progress_bar.progress(1.0, text="Hoan tat!")

    full_md += "\n---\n*Generated by 2M Marketing Agency AI*\n"

    saved_folder = None
    if auto_save:
        saved_folder = save_output(campaign_name, full_md)

    st.session_state["last_outputs"]    = outputs
    st.session_state["last_campaign"]   = campaign_name
    st.session_state["pending_approval"] = True
    st.session_state["last_full_md"]    = full_md
    st.session_state["last_agents_ran"] = agents_to_run
    st.session_state["last_saved_folder"] = saved_folder

# ══════════════════════════════════════════════════════════════
# KẾT QUẢ & PHÊ DUYỆT — nằm NGOÀI if run_btn: để không bị reset
# ══════════════════════════════════════════════════════════════
if st.session_state.get("pending_approval"):
    outputs       = st.session_state.get("last_outputs", {})
    campaign_name = st.session_state.get("last_campaign", "")
    full_md       = st.session_state.get("last_full_md", "")
    agents_to_run = st.session_state.get("last_agents_ran", [])
    saved_folder  = st.session_state.get("last_saved_folder")

    _rc1, _rc2 = st.columns([5, 1])
    with _rc2:
        if st.button("🗑️ Xóa kết quả", key="clear_results_btn"):
            for _k in ["pending_approval", "last_outputs", "last_campaign",
                       "last_full_md", "last_agents_ran", "last_saved_folder"]:
                st.session_state.pop(_k, None)
            st.rerun()

    st.markdown("---")
    st.markdown("### KET QUA -- Anh Tuan Xem & Duyet")
    if saved_folder:
        st.success(f"Da luu tai: `{saved_folder}/CAMPAIGN_OUTPUT.md`")

    if show_detail:
        for aid in agents_to_run:
            if aid in outputs and aid in AGENTS:
                ag       = AGENTS[aid]
                expanded = aid in ("be_viet", "co_hoc", "be_quan")
                with st.expander(f"{ag['emoji']} {ag['name']} -- {ag['role']}", expanded=expanded):
                    st.markdown(outputs[aid])

    st.markdown("---")
    st.markdown("### ✅ PHÊ DUYỆT & TỰ ĐỘNG ĐĂNG BÀI")

    creds = get_social_creds()
    fb_connected = bool(creds["fb_token"] and creds["fb_page_id"])
    ig_connected = bool(creds["fb_token"] and creds["ig_user_id"])

    # --- Posting mode ---
    post_col, sched_col = st.columns([1, 2])
    with post_col:
        post_mode = st.radio(
            "Chế độ đăng:",
            ["Đăng ngay", "Lên lịch", "Lưu file (thủ công)"],
            index=0 if fb_connected else 2
        )
    with sched_col:
        sched_date = None
        sched_time_str = None
        if post_mode == "Lên lịch":
            sched_date = st.date_input("Ngày đăng:", value=datetime.now().date() + timedelta(days=1))
            sched_time_str = st.text_input("Giờ đăng (HH:MM, giờ CST):", value="11:00")

    # --- Image URL for Instagram ---
    img_url = ""
    if ig_connected or post_mode != "Lưu file (thủ công)":
        img_url = st.text_input(
            "🖼️ URL ảnh để đăng Instagram (để trống nếu chưa có):",
            placeholder="https://... (ảnh phải public, min 320px)",
            help="Instagram bắt buộc cần ảnh. Facebook có thể đăng text-only."
        )

    # --- Platform selection ---
    plat_col1, plat_col2, plat_col3, plat_col4, plat_col5 = st.columns(5)
    with plat_col1:
        do_fb = st.checkbox("📘 Facebook", value=fb_connected)
    with plat_col2:
        do_ig = st.checkbox("📸 Instagram", value=ig_connected and bool(img_url))
    with plat_col3:
        do_wp = st.checkbox("🌐 Website", value=wp_connected())
    with plat_col4:
        do_save = st.checkbox("💾 Lưu file", value=True)
    with plat_col5:
        do_dl = st.checkbox("⬇️ Download", value=False)

    if not fb_connected and (do_fb or do_ig):
        st.warning("⚠️ Chưa kết nối Facebook API. Xem hướng dẫn kết nối trong sidebar.")
    if do_wp and not wp_connected():
        st.warning("⚠️ Chưa kết nối WordPress. Thêm WP_SITE_URL / WP_USERNAME / WP_APP_PASSWORD vào .env")

    # --- Buttons ---
    btn_col, dl_col = st.columns([2, 2])
    with btn_col:
        approve_btn = st.button("✅ PHÊ DUYỆT & THỰC THI", type="primary", use_container_width=True)
    with dl_col:
        st.download_button(
            "⬇️ Tải toàn bộ (.md)",
            data=full_md.encode("utf-8"),
            file_name=f"{campaign_name.replace(' ','_')[:30]}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    if approve_btn:
        results_log = []

        # --- Prepare schedule datetime ---
        schedule_dt = None
        if post_mode == "Lên lịch" and sched_date and sched_time_str:
            try:
                h, m = map(int, sched_time_str.split(":"))
                schedule_dt = datetime(sched_date.year, sched_date.month, sched_date.day, h, m)
            except Exception:
                st.error("Giờ không đúng định dạng HH:MM")
                st.stop()

        # --- Build clean text for each platform ---
        fb_caption  = clean_text(outputs.get("be_viet", outputs.get("be_dang", "")))
        ig_caption  = clean_text(outputs.get("be_viet", outputs.get("be_dang", "")))

        # === FACEBOOK ===
        if do_fb and fb_connected:
            with st.spinner("📘 Đang đăng lên Facebook..."):
                try:
                    if post_mode == "Lên lịch" and schedule_dt:
                        res = fb_schedule(creds["fb_page_id"], creds["fb_token"],
                                          fb_caption, schedule_dt, img_url)
                        if "id" in res:
                            st.success(f"📘 Facebook đã lên lịch: {schedule_dt.strftime('%d/%m/%Y %H:%M')} CST (ID: {res['id']})")
                            results_log.append(f"FB scheduled {schedule_dt.strftime('%d/%m %H:%M')}")
                        else:
                            st.error(f"📘 Facebook lỗi: {res.get('error', {}).get('message', res)}")
                    else:
                        res = fb_post_now(creds["fb_page_id"], creds["fb_token"], fb_caption, img_url)
                        if "id" in res:
                            post_url = f"https://www.facebook.com/{res['id']}"
                            st.success(f"📘 Facebook đã đăng! [Xem bài]({post_url})")
                            results_log.append("FB posted")
                        else:
                            st.error(f"📘 Facebook lỗi: {res.get('error', {}).get('message', res)}")
                except Exception as e:
                    st.error(f"📘 Facebook exception: {e}")
        elif do_fb and not fb_connected:
            st.warning("📘 Facebook chưa kết nối — bỏ qua.")

        # === INSTAGRAM ===
        if do_ig and ig_connected:
            if not img_url:
                st.warning("📸 Instagram cần URL ảnh — bỏ qua. Thêm URL ảnh và phê duyệt lại.")
            else:
                with st.spinner("📸 Đang đăng lên Instagram..."):
                    try:
                        if post_mode == "Lên lịch" and schedule_dt:
                            res = ig_schedule(creds["ig_user_id"], creds["fb_token"],
                                              ig_caption, img_url, schedule_dt)
                            if res.get("scheduled"):
                                st.success(f"📸 Instagram đã lên lịch: {res['publish_at']}")
                                results_log.append("IG scheduled")
                            else:
                                st.error(f"📸 Instagram lỗi: {res.get('error', {}).get('message', res)}")
                        else:
                            res = ig_post_now(creds["ig_user_id"], creds["fb_token"],
                                              ig_caption, img_url)
                            if "id" in res:
                                st.success(f"📸 Instagram đã đăng! (ID: {res['id']})")
                                results_log.append("IG posted")
                            else:
                                st.error(f"📸 Instagram lỗi: {res.get('error', {}).get('message', res)}")
                    except Exception as e:
                        st.error(f"📸 Instagram exception: {e}")
        elif do_ig and not ig_connected:
            st.warning("📸 Instagram chưa kết nối — bỏ qua.")

        # === WORDPRESS / WEBSITE ===
        if do_wp and wp_connected():
            be_quan_out = outputs.get("be_quan", "")
            if not be_quan_out:
                st.warning("🌐 Không có output từ Bé Quản để đăng website.")
            else:
                with st.spinner("🌐 Đang chuẩn bị bài blog và đăng lên website..."):
                    try:
                        blog = extract_blog_sections(be_quan_out)
                        # Determine status
                        if post_mode == "Lên lịch" and schedule_dt:
                            wp_status = "future"
                        elif post_mode == "Lưu file (thủ công)":
                            wp_status = "draft"  # safe draft for manual review
                        else:
                            wp_status = "publish"
                        res = wp_post(
                            title=blog["title"],
                            html_content=blog["html"],
                            excerpt=blog["meta_desc"],
                            tags=blog["tags"],
                            categories=["Construction Tips", "Local Guide"],
                            slug=blog["slug"],
                            status=wp_status,
                            yoast_title=blog["yoast_title"],
                            yoast_desc=blog["meta_desc"],
                            focus_kw=blog["focus_kw"],
                            schedule_dt=schedule_dt if wp_status == "future" else None,
                        )
                        if "error" in res:
                            st.error(f"🌐 Website lỗi: {res['error']}")
                        else:
                            if wp_status == "future":
                                st.success(f"🌐 Bài blog đã lên lịch: {schedule_dt.strftime('%d/%m/%Y %H:%M')} — [Xem draft]({res.get('link','')})")
                            elif wp_status == "draft":
                                st.success(f"🌐 Bài blog đã lưu draft trên WordPress — [Xem draft]({res.get('link','')})")
                            else:
                                st.success(f"🌐 Bài blog đã xuất bản! — [Đọc ngay]({res.get('link','')})")
                            results_log.append(f"WP {wp_status}")
                    except Exception as e:
                        st.error(f"🌐 Website exception: {e}")
        elif do_wp and not wp_connected():
            st.warning("🌐 WordPress chưa kết nối — bỏ qua.")

        # === SAVE FILES ===
        if do_save:
            with st.spinner("💾 Đang lưu file vào PUBLISH_QUEUE..."):
                dist = approve_and_distribute(campaign_name, outputs, agents_to_run)
            for platform, filepath in dist.items():
                if platform == "error":
                    st.error(f"Lỗi lưu file: {filepath}")
                else:
                    fname  = Path(filepath).name
                    folder = platform.replace(" ", "_").upper()
                    st.success(f"💾 {platform} → `PUBLISH_QUEUE/{folder}/{fname}`")
            results_log.append("Files saved")

        # === SUMMARY ===
        if results_log:
            st.info(
                "**Hoàn tất!** Đã thực hiện: " + " | ".join(results_log) + "\n\n"
                "**Nhớ:** Thêm ảnh trực tiếp trên Facebook/Instagram nếu chưa có URL ảnh.\n"
                "**KPI:** Ghi lại engagement sau 24h để so sánh tuần sau."
            )

# ══════════════════════════════════════════════════════════════
# 📝  BÉ QUẢN — BLOG MANAGER  (Quản trị Website & SEO Blog)
# ══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("## 📝 Blog Manager — Bé Quản")
st.markdown(
    '<p class="sub-gray">Viết & đăng bài SEO tự động lên website 2M Construction</p>',
    unsafe_allow_html=True,
)

_bm_wp_ok = site_connected()
if not _bm_wp_ok:
    st.info(
        "🌐 **Chưa kết nối website.**\n\n"
        "Điền admin password tại sidebar → **⚙️ Cài đặt Website** để Bé Quản bắt đầu đăng bài."
    )
else:
    _bm_tab1, _bm_tab2 = st.tabs(["✍️ Viết bài mới", "📋 Danh sách bài đã đăng"])

    # ── TAB 1: VIẾT BÀI MỚI ──────────────────────────────────
    with _bm_tab1:
        _bm_c1, _bm_c2 = st.columns([2, 1])
        with _bm_c1:
            _bm_topic = st.text_input(
                "🎯 Chủ đề bài blog",
                placeholder="VD: Epoxy garage floor Huntsville AL — bao nhiêu tiền? (2025)",
                key="bm_topic",
            )
            _bm_keywords = st.text_input(
                "🔑 Keywords SEO (cách nhau bởi dấu phẩy)",
                placeholder="epoxy garage huntsville, garage floor coating alabama, epoxy floor cost",
                key="bm_keywords",
            )
            _bm_notes = st.text_area(
                "📝 Ghi chú thêm (tùy chọn)",
                placeholder="VD: Nhấn mạnh giá cạnh tranh, có trước/sau, đề cập Madison AL và Harvest AL",
                height=80,
                key="bm_notes",
            )
        with _bm_c2:
            _bm_mode = st.selectbox(
                "📤 Chế độ đăng",
                ["📋 Draft (xem trước)", "🚀 Publish ngay", "📅 Lên lịch"],
                key="bm_mode",
            )
            _bm_sched_dt = None
            if "Lên lịch" in _bm_mode:
                _bm_sched_dt = st.date_input("📅 Ngày đăng", key="bm_sched_date")
                _bm_sched_hr = st.number_input("⏰ Giờ (CST)", 0, 23, 9, key="bm_sched_hr")
                if _bm_sched_dt:
                    from datetime import datetime as _bm_dt, timezone as _bm_tz
                    _bm_sched_dt = _bm_dt(
                        _bm_sched_dt.year, _bm_sched_dt.month, _bm_sched_dt.day,
                        _bm_sched_hr, 0, 0
                    )

            _bm_category = st.selectbox(
                "📁 Danh mục",
                ["Services", "Tips & Guides", "Project Gallery", "Local Guide", "Cost Guide"],
                key="bm_cat",
            )

        _bm_run = st.button("✍️ Bé Quản viết bài SEO", type="primary",
                            disabled=not _bm_topic, key="bm_run_btn")

        if _bm_run and _bm_topic:
            _bm_api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
            if not _bm_api_key:
                st.error("Cần ANTHROPIC_API_KEY trong .env")
            else:
                with st.spinner("🖊️ Bé Quản đang viết bài SEO..."):
                    try:
                        import anthropic as _bm_anthropic
                        _bm_client = _bm_anthropic.Anthropic(api_key=_bm_api_key)

                        _bm_soul = AGENTS["be_quan"]["soul"]
                        _bm_brief = f"""Viết bài blog SEO đầy đủ cho website 2M Construction LLC.

CHỦ ĐỀ: {_bm_topic}
KEYWORDS: {_bm_keywords or 'tự chọn từ chủ đề'}
GHI CHÚ: {_bm_notes or 'không có'}
DANH MỤC: {_bm_category}

YÊU CẦU FORMAT (PHẢI theo đúng):
=== BLOG POST FOR WEBSITE ===
TITLE (SEO): [title ≤60 ký tự, có keyword chính]
SLUG: [url-thân-thiện-seo]
META DESCRIPTION: [150-160 ký tự, có CTA]
CATEGORY: {_bm_category}
TAGS: [tag1, tag2, tag3, tag4, tag5]
FOCUS KEYWORD: [keyword chính]
YOAST TITLE: [title | 2M Construction LLC Huntsville AL]

=== NỘI DUNG HTML ===
<article>
<h1>[Title có keyword]</h1>
<p class="lead">[Đoạn mở đầu 100 chữ — có keyword + Huntsville AL]</p>

<h2>[Heading 1 có keyword biến thể]</h2>
<p>[Nội dung 150-200 chữ]</p>

<h2>[FAQ: "How much does X cost in Huntsville AL?"]</h2>
<p>[Trả lời tự nhiên, có keyword]</p>

<h2>Why Choose 2M Construction LLC?</h2>
<p>[Nêu 3-4 lý do cụ thể, có địa danh]</p>

<h2>Contact Us Today</h2>
<p>Call <a href="tel:9383026795">(938) 302-6795</a> for a free estimate in Huntsville, Madison, and North Alabama.</p>
</article>

Bài blog dài 500-800 chữ. SEO local chuẩn. Tiếng Anh."""

                        _bm_resp = _bm_client.messages.create(
                            model=AGENTS["be_quan"]["model"],
                            max_tokens=3000,
                            system=_bm_soul + "\n\n===COMPANY INFO===\n" + get_company_ctx(),
                            messages=[{"role": "user", "content": _bm_brief}],
                        )
                        _bm_output = _bm_resp.content[0].text
                        st.session_state["bm_last_output"] = _bm_output

                    except Exception as _bm_e:
                        st.error(f"Lỗi: {_bm_e}")
                        st.session_state["bm_last_output"] = ""

        # Hiển thị kết quả + nút đăng
        if st.session_state.get("bm_last_output"):
            _bm_out = st.session_state["bm_last_output"]
            st.markdown("---")
            st.markdown("### 📄 Preview bài Bé Quản viết")

            with st.expander("Xem nội dung đầy đủ", expanded=True):
                st.text_area("Output", _bm_out, height=400, key="bm_output_ta")

            # Parse & show summary
            _bm_blog = extract_blog_sections(_bm_out)
            if _bm_blog.get("title"):
                _pi1, _pi2, _pi3 = st.columns(3)
                _pi1.metric("Title", _bm_blog["title"][:40] + "..." if len(_bm_blog["title"]) > 40 else _bm_blog["title"])
                _pi2.metric("Focus KW", _bm_blog.get("focus_kw", "—"))
                _pi3.metric("Tags", str(len(_bm_blog.get("tags", []))) + " tags")

            st.markdown("#### 📤 Đăng lên 2mhuntsville.com")
            _bm_post_col1, _bm_post_col2 = st.columns(2)
            with _bm_post_col1:
                _bm_published = "Publish" in _bm_mode

                if st.button(
                    f"🚀 {'Xuất bản ngay' if _bm_published else 'Lưu Draft'} lên website",
                    type="primary", key="bm_post_btn"
                ):
                    with st.spinner("🌐 Đang đăng bài lên 2mhuntsville.com..."):
                        try:
                            _bm_res = site_post(
                                title=_bm_blog.get("title", _bm_topic),
                                content_md=_bm_blog.get("html", _bm_out),
                                excerpt=_bm_blog.get("meta_desc", ""),
                                tags=_bm_blog.get("tags", []),
                                slug=_bm_blog.get("slug", ""),
                                published=_bm_published,
                                meta_title=_bm_blog.get("yoast_title", ""),
                                meta_description=_bm_blog.get("meta_desc", ""),
                            )
                            if "error" in _bm_res:
                                st.error(f"Lỗi: {_bm_res['error']}")
                            else:
                                _bm_post = _bm_res.get("post", {})
                                _bm_slug = _bm_post.get("slug", "")
                                _bm_link = f"https://www.2mhuntsville.com/blog/{_bm_slug}" if _bm_slug else "https://www.2mhuntsville.com/blog"
                                if _bm_published:
                                    st.success(f"✅ Bài đã xuất bản! [Đọc ngay]({_bm_link})")
                                else:
                                    st.success(f"✅ Đã lưu draft! Vào [2mhuntsville.com/admin]({SITE_URL}/admin) để duyệt.")
                                st.session_state["bm_last_output"] = ""
                        except Exception as _bm_pe:
                            st.error(f"Lỗi đăng bài: {_bm_pe}")

            with _bm_post_col2:
                if st.button("🗑️ Viết lại", key="bm_rewrite_btn"):
                    st.session_state["bm_last_output"] = ""
                    st.rerun()

    # ── TAB 2: DANH SÁCH BÀI ĐÃ ĐĂNG ────────────────────────
    with _bm_tab2:
        if st.button("🔄 Tải danh sách bài", key="bm_list_btn"):
            with st.spinner("Đang tải..."):
                _bm_posts = site_list_posts()
            if _bm_posts:
                for _p in _bm_posts:
                    _p_pub = _p.get("published", False)
                    _p_icon = "🟢" if _p_pub else "📋"
                    _p_date = (_p.get("publishedAt") or _p.get("updatedAt", ""))[:10]
                    _p_title = _p.get("title", "—")
                    _p_slug = _p.get("slug", "")
                    _p_link = f"https://www.2mhuntsville.com/blog/{_p_slug}" if _p_slug else "#"
                    _p_tags = ", ".join(_p.get("tags", [])[:3])
                    st.markdown(
                        f"{_p_icon} **[{_p_title}]({_p_link})** · {_p_date}"
                        + (f" · `{_p_tags}`" if _p_tags else "")
                    )
            else:
                st.info("Chưa có bài viết nào. Tạo bài đầu tiên ở tab ✍️ bên cạnh!")
