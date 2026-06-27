# AGENTS.md — Master Config
## 2M Marketing Agency AI · OpenClaw Configuration

---

## ORCHESTRATOR

```yaml
name: little_boss
display_name: "Little Boss"
role: orchestrator
model: claude-sonnet-4-6
temperature: 0.7
description: |
  Central orchestrator for 2M Construction LLC Marketing Agency.
  Receives commands from Tuan Nguyen, delegates to sub-agents,
  synthesizes results for human approval before publishing.
soul_file: ./SOUL_little_boss.md
memory:
  type: persistent
  path: ./memory/little_boss/
tools:
  - delegate_to_agent
  - read_knowledge_vault
  - create_task
  - approve_content
  - notify_human
channels:
  - claude_desktop
  - (future: telegram, slack)
```

---

## SUB-AGENTS

```yaml
agents:

  - name: anh_tong
    display_name: "Anh Tổng"
    nickname: "Anh Tổng"
    role: cmo
    model: claude-sonnet-4-6
    temperature: 0.6
    soul_file: ./souls/SOUL_anh_tong.md
    memory:
      type: persistent
      path: ./memory/anh_tong/
    tools:
      - read_knowledge_vault
      - create_brief
      - delegate_to_agent
      - compile_report
    knowledge_sources:
      - brand_guidelines
      - sop_library
      - weekly_ops

  - name: chi_brand
    display_name: "Chị Brand"
    nickname: "Chị Brand"
    role: brand_creative_director
    model: claude-sonnet-4-6
    temperature: 0.8
    soul_file: ./souls/SOUL_chi_brand.md
    memory:
      type: session
    tools:
      - review_content
      - check_brand_compliance
      - suggest_visuals
    knowledge_sources:
      - brand_guidelines
      - color_system
      - taglines

  - name: co_chien
    display_name: "Cô Chiến"
    nickname: "Cô Chiến"
    role: campaign_growth_manager
    model: claude-haiku-4-5-20251001
    temperature: 0.5
    soul_file: ./souls/SOUL_co_chien.md
    memory:
      type: session
    tools:
      - create_campaign_plan
      - set_kpi
      - track_timeline
    knowledge_sources:
      - sop_library
      - weekly_ops

  - name: con_muoi
    display_name: "Con Muối"
    nickname: "Con Muối 🧂"
    role: content_brain
    model: MiniMax-M3-Text
    temperature: 1.0
    soul_file: ./souls/SOUL_con_muoi.md
    memory:
      type: session
    tools:
      - write_content
      - generate_hooks
      - write_copy
    knowledge_sources:
      - brand_voice
      - competitor_intel
    notes: "Chuyên content tiếng Việt 'mặn', hook mạnh, copy thuyết phục"

  - name: be_viet
    display_name: "Bé Viết"
    nickname: "Bé Viết"
    role: content_community_manager
    model: claude-haiku-4-5-20251001
    temperature: 0.7
    soul_file: ./souls/SOUL_be_viet.md
    memory:
      type: session
    tools:
      - write_facebook_post
      - write_nextdoor_post
      - write_caption
      - write_bilingual_content
    knowledge_sources:
      - brand_voice
      - content_templates

  - name: dao_dien
    display_name: "Đạo Diễn"
    nickname: "Đạo Diễn 🎬"
    role: video_design_director
    model: gpt-4o
    temperature: 0.9
    soul_file: ./souls/SOUL_dao_dien.md
    memory:
      type: session
    tools:
      - write_visual_brief
      - generate_canva_prompt
      - write_video_script
      - describe_before_after
    knowledge_sources:
      - brand_guidelines
      - color_system

  - name: tham_tu
    display_name: "Thám Tử"
    nickname: "Thám Tử 🔍"
    role: insight_intelligence_manager
    model: claude-sonnet-4-6
    temperature: 0.4
    soul_file: ./souls/SOUL_tham_tu.md
    memory:
      type: persistent
      path: ./memory/tham_tu/
    tools:
      - web_research
      - analyze_competitor
      - track_trends
      - generate_intel_report
    knowledge_sources:
      - competitor_database
    fallback_model: gemini-flash

  - name: so_hoc
    display_name: "Số Học"
    nickname: "Số Học 📊"
    role: analytics_performance_manager
    model: gpt-4o-mini
    temperature: 0.2
    soul_file: ./souls/SOUL_so_hoc.md
    memory:
      type: session
    tools:
      - calculate_metrics
      - generate_report
      - compare_performance
    knowledge_sources:
      - analytics_history
    fallback_model: deepseek-chat

  - name: thu_ky
    display_name: "Thư Ký"
    nickname: "Thư Ký 📚"
    role: knowledge_automation_manager
    model: claude-haiku-4-5-20251001
    temperature: 0.3
    soul_file: ./souls/SOUL_thu_ky.md
    memory:
      type: persistent
      path: ./memory/thu_ky/
    tools:
      - index_knowledge
      - update_vault
      - create_automation_rule
      - manage_files
    knowledge_sources:
      - all_vaults

  - name: quan_ly
    display_name: "Quản Lý"
    nickname: "Quản Lý ⚙️"
    role: operations_manager
    model: gpt-4o-mini
    temperature: 0.3
    soul_file: ./souls/SOUL_quan_ly.md
    memory:
      type: persistent
      path: ./memory/quan_ly/
    tools:
      - manage_task_queue
      - send_reminder
      - track_deadlines
      - generate_weekly_ops_report
    fallback_model: groq/llama-3.1-8b-instant

  - name: be_dang
    display_name: "Bé Đăng"
    nickname: "Bé Đăng 📤"
    role: publisher
    model: gpt-4o-mini
    temperature: 0.1
    soul_file: ./souls/SOUL_be_dang.md
    memory:
      type: session
    tools:
      - format_for_platform
      - schedule_post
      - check_content_quality
      - flag_for_human_approval
    notes: "Luôn flag cho Anh Tuan duyệt trước khi đăng — KHÔNG tự động đăng"
    human_approval_required: true
```

---

## WORKFLOW DEFINITIONS

```yaml
workflows:

  social_media_weekly:
    name: "Social Media Weekly"
    trigger: manual
    steps:
      - agent: anh_tong
        action: "Nhận brief từ Anh Tuan, phân việc"
      - agent: con_muoi
        action: "Tạo concept + hook mạnh cho bài"
      - agent: be_viet
        action: "Viết bài hoàn chỉnh (Anh + Việt)"
      - agent: chi_brand
        action: "Review brand compliance"
      - agent: dao_dien
        action: "Gợi ý visual/ảnh kèm theo"
      - human_approval:
        action: "Anh Tuan duyệt nội dung"
      - agent: be_dang
        action: "Format và xếp lịch đăng"

  competitor_research:
    name: "Competitor Research"
    trigger: monthly
    steps:
      - agent: tham_tu
        action: "Research top 10 GC Huntsville"
      - agent: so_hoc
        action: "Phân tích số liệu, so sánh"
      - agent: anh_tong
        action: "Tổng hợp báo cáo"
      - human_approval:
        action: "Anh Tuan review"

  lead_followup:
    name: "Lead Follow-Up"
    trigger: manual
    steps:
      - agent: quan_ly
        action: "Identify leads cần follow-up"
      - agent: be_viet
        action: "Soạn tin nhắn/email"
      - human_approval:
        action: "Anh Tuan duyệt trước khi gửi"

  project_showcase:
    name: "Project Before/After"
    trigger: manual
    steps:
      - agent: dao_dien
        action: "Viết visual brief từ ảnh dự án"
      - agent: con_muoi
        action: "Caption mặn, hook mạnh"
      - agent: be_viet
        action: "Bản song ngữ hoàn chỉnh"
      - agent: chi_brand
        action: "Review"
      - human_approval:
        action: "Anh Tuan duyệt"
      - agent: be_dang
        action: "Đăng theo lịch"
```

---

## COMPANY CONTEXT (Injected vào mọi agent)

```yaml
company:
  name: "2M Construction LLC"
  type: "Full-Service General Contractor"
  location: "Huntsville, Alabama"
  service_area: "Huntsville, Madison, Athens, North Alabama"
  services:
    - Deck & Patio
    - Fence
    - Hardwood & LVP Flooring
    - Tile & Backsplash
    - Interior & Exterior Painting
    - Drywall
    - Epoxy Garage Floor
    - Concrete (driveway, patio, sidewalk)
    - Kitchen & Bathroom Cabinets
  brand_colors:
    primary: "#1B2A4A"   # Navy
    accent: "#C9A84C"    # Gold
    base: "#FFFFFF"      # White
  tone: "Professional & Trustworthy"
  owner: "Tuan Nguyen"
  rule_1: "NEVER describe 2M as deck/fence only company — always full-service GC"
  rule_2: "ALL content requires human approval before publishing"
  rule_3: "Bilingual content (EN + VI) when targeting Vietnamese community"
```
