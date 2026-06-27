"""
Chạy script này 1 lần để kết nối Facebook & Instagram vào 2M Agency AI
Tự động: lấy Page Token, Page ID, IG Account ID → ghi vào .env
"""
import requests, json, os, re

LONG_TOKEN = "EAAOTXnXFEFgBR2E4xDg18mDsWv4aiQMcPgAmw8WjzcAPh7BHihxZBnn9DRiUirMAs4LFqvF7RZB5mZAi6BApvNrhVhIQXdG4gKRNnIfrQ1oJvBZBMCLduNGkvgSbXwaKyqoVAP8Q3A98yc5LHfZAN6BRPSm7OLm7HjnGHxIHY9b9bKKmMZAi2HKtz4WjHwTSduPjxdkZCmZBYZBXvjuEKcV1SwPSUTXFdGuxzNS0Yfwkp"
GRAPH = "https://graph.facebook.com/v19.0"
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

def set_env(content, key, value):
    pattern = rf"^{key}=.*$"
    replacement = f"{key}={value}"
    if re.search(pattern, content, re.MULTILINE):
        return re.sub(pattern, replacement, content, flags=re.MULTILINE)
    return content + f"\n{key}={value}"

print("=" * 50)
print("2M Agency AI — Facebook & Instagram Setup")
print("=" * 50)

# Bước 1: Lấy danh sách Pages
print("\n[1/3] Đang lấy danh sách Facebook Pages...")
r = requests.get(f"{GRAPH}/me/accounts", params={
    "access_token": LONG_TOKEN,
    "fields": "name,id,access_token"
})

if r.status_code != 200:
    print(f"❌ Lỗi: {r.json()}")
    input("\nNhấn Enter để thoát...")
    exit(1)

pages = r.json().get("data", [])
if not pages:
    print("❌ Không tìm thấy Page nào. Hãy đảm bảo token có quyền pages_show_list.")
    input("\nNhấn Enter để thoát...")
    exit(1)

print(f"✅ Tìm thấy {len(pages)} Page:")
for i, p in enumerate(pages):
    print(f"   {i+1}. {p['name']} (ID: {p['id']})")

# Dùng page đầu tiên (hoặc chọn nếu có nhiều)
if len(pages) > 1:
    choice = input(f"\nChọn page (1-{len(pages)}, mặc định 1): ").strip()
    idx = int(choice) - 1 if choice.isdigit() and 1 <= int(choice) <= len(pages) else 0
else:
    idx = 0

page = pages[idx]
PAGE_TOKEN = page["access_token"]
PAGE_ID = page["id"]
PAGE_NAME = page["name"]
print(f"\n✅ Đã chọn: {PAGE_NAME} (ID: {PAGE_ID})")

# Bước 2: Lấy Instagram Business Account
print("\n[2/3] Đang tìm Instagram Business Account...")
r2 = requests.get(f"{GRAPH}/{PAGE_ID}", params={
    "access_token": PAGE_TOKEN,
    "fields": "instagram_business_account,name"
})

IG_ID = ""
if r2.status_code == 200:
    IG_ID = r2.json().get("instagram_business_account", {}).get("id", "")

if IG_ID:
    print(f"✅ Instagram Business Account ID: {IG_ID}")
else:
    print("⚠️  Không tìm thấy Instagram (chưa kết nối IG với Facebook Page hoặc chưa là Business account)")

# Bước 3: Ghi vào .env
print(f"\n[3/3] Đang ghi vào .env...")
with open(ENV_PATH, "r", encoding="utf-8") as f:
    env_content = f.read()

env_content = set_env(env_content, "FB_PAGE_ACCESS_TOKEN", PAGE_TOKEN)
env_content = set_env(env_content, "FB_PAGE_ID", PAGE_ID)
if IG_ID:
    env_content = set_env(env_content, "IG_BUSINESS_ACCOUNT_ID", IG_ID)

with open(ENV_PATH, "w", encoding="utf-8") as f:
    f.write(env_content)

print("\n" + "=" * 50)
print("✅ HOÀN TẤT! Đã lưu vào .env:")
print(f"   FB_PAGE_ACCESS_TOKEN = {PAGE_TOKEN[:30]}...")
print(f"   FB_PAGE_ID           = {PAGE_ID}")
if IG_ID:
    print(f"   IG_BUSINESS_ACCOUNT_ID = {IG_ID}")
print("\n👉 Khởi động lại app (2_RUN.bat) để kết nối có hiệu lực.")
print("=" * 50)
input("\nNhấn Enter để thoát...")
