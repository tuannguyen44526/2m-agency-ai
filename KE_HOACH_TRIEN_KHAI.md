# KẾ HOẠCH TRIỂN KHAI — 2M MARKETING AGENCY AI
*Cập nhật: 07/07/2026 · Sau khi tối ưu cấu trúc dự án*

---

## GIAI ĐOẠN 1 — BẢO MẬT (làm NGAY hôm nay, ~30 phút)

- [ ] **Revoke GitHub token cũ:** vào github.com/settings/tokens → xóa token `ghp_...` (đã lộ trong lịch sử git)
- [ ] **Tạo GitHub token mới** (chỉ quyền `repo`) → dùng khi push, KHÔNG lưu vào file trong dự án
- [ ] **Thu hồi Facebook token cũ:** vào developers.facebook.com → app 2M → xóa/làm mới token (2 token đã lộ trên GitHub)
- [ ] **Lấy FB long-lived token mới** → điền vào `.env`: `FB_LONG_LIVED_TOKEN=...`
- [ ] Chạy `scripts/3_SETUP_FACEBOOK.bat` → tự lấy Page Token + IG ID mới vào `.env`
- [ ] **Tạo imgbb key mới** tại api.imgbb.com → điền `IMGBB_API_KEY=` vào `.env`
- [ ] Chạy `scripts/4_CHECK_IG.bat` xác nhận Instagram kết nối OK

## GIAI ĐOẠN 2 — ĐỒNG BỘ CODE & DEPLOY (~30 phút, sau Giai đoạn 1)

- [ ] Mở GitHub Desktop → commit toàn bộ thay đổi: *"Restructure: archive old versions, remove secrets"* → Push
- [ ] Vào share.streamlit.io → app 2m-agency-ai → **Settings → Secrets** → cập nhật đủ 7 keys (thêm `IMGBB_API_KEY`)
- [ ] Reboot app trên Streamlit Cloud → test 1 lệnh nhanh xem chạy OK
- [ ] Test local: double-click `2_RUN.bat` → chạy thử 1 campaign → kiểm tra file xuất ra `CAMPAIGNS/` + `PUBLISH_QUEUE/`

## GIAI ĐOẠN 3 — VẬN HÀNH MARKETING TUẦN 28+ (routine hằng tuần)

**Thứ 2 (30 phút):**
- [ ] Cập nhật `WEEKLY_PLAN.md` — 6 lệnh cho tuần mới (tuần 28: 6/7–12/7, dịch vụ trọng tâm tự chọn theo mùa)
- [ ] Chạy app → tạo content cả tuần trong 1 buổi

**Thứ 3–CN (10 phút/ngày):**
- [ ] Duyệt bài trong `PUBLISH_QUEUE/` → chỉnh nếu cần → đăng (FB/IG qua app, Nextdoor/GBP copy thủ công)
- [ ] Trả lời comment/inbox trong ngày

**Cuối tuần (15 phút):**
- [ ] Chạy lệnh báo cáo tuần trong app → xem bài nào hiệu quả → điều chỉnh `WEEKLY_PLAN.md` tuần sau

**Gợi ý trọng tâm theo mùa (Huntsville):**
| Tháng | Dịch vụ đẩy mạnh |
|-------|-----------------|
| 7–8 | Epoxy garage, concrete patio, sơn ngoại thất (nắng khô) |
| 9–10 | Deck/fence trước mùa lễ, sàn trong nhà |
| 11–12 | Nội thất: tủ bếp, drywall, sơn trong nhà, "làm đẹp nhà đón lễ" |

## GIAI ĐOẠN 4 — NÂNG CẤP (tùy chọn, khi Giai đoạn 3 đã ổn định)

- [ ] Bổ sung ảnh thật dự án vào bài đăng (before/after tăng engagement mạnh nhất)
- [ ] Bật Google Business Profile posting đều đặn (SEO map pack)
- [ ] Xem lại kế hoạch OpenClaw 11 agent trong `_ARCHIVE/v3_openclaw_plan/` — chỉ làm khi app hiện tại không đủ dùng
- [ ] Theo dõi chi phí API tại console.anthropic.com (dự kiến < $5/tháng)

---

**Nguyên tắc:** AI soạn — Tuan duyệt — rồi mới đăng. Không bỏ qua bước duyệt.
