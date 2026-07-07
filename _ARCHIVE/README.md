# _ARCHIVE — Tài liệu phiên bản cũ

Hệ thống hiện tại là **app Streamlit `2m_agency_ai.py`** ở thư mục gốc. Mọi thứ trong đây là các phiên bản/kế hoạch trước, giữ lại để tham khảo.

| Thư mục | Nội dung |
|---------|----------|
| `v1_roles_manual/` | Thế hệ 1: 6 thư mục vai trò (01_CMO → 06_Analytics) với ROLE.md để copy-paste thủ công vào Claude. Đã được thay bằng app. |
| `v3_openclaw_plan/` | Kế hoạch OpenClaw 11 agent (AGENTS.md, MULTI_MODEL_MATRIX.md, SOUL files). Chưa triển khai — nếu sau này làm multi-agent thật thì lấy từ đây. |
| `git_scripts/` | Script push GitHub dùng 1 lần. ⚠️ PUSH_WITH_TOKEN.bat từng chứa GitHub PAT plaintext — đã xóa token khỏi file, nhưng token vẫn nằm trong lịch sử git → PHẢI revoke trên github.com/settings/tokens |
| `misc/` | File cũ: _SYSTEM_OVERVIEW.md (mô tả 6 vai — lỗi thời), 2M_Agency_Dashboard.html (dashboard tĩnh cũ), RUN_APP.bat (trùng 2_RUN.bat), ig_check_result.txt |
