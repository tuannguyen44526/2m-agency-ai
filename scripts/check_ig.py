import requests, json, re, os
from dotenv import load_dotenv

# .env nằm ở thư mục gốc dự án (script này nằm trong scripts/)
ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT, ".env")
LOG      = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ig_check_result.txt")
load_dotenv(ENV_PATH)

# KHÔNG hardcode token! Đọc từ .env
LONG_TOKEN = os.environ.get("FB_LONG_LIVED_TOKEN", "")
PAGE_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN", "")
PAGE_ID    = os.environ.get("FB_PAGE_ID", "")
GRAPH      = "https://graph.facebook.com/v19.0"

if not PAGE_TOKEN or not PAGE_ID:
    print("❌ Thiếu FB_PAGE_ACCESS_TOKEN hoặc FB_PAGE_ID trong .env — chạy 3_SETUP_FACEBOOK.bat trước.")
    exit(1)

def set_env(content, key, value):
    pattern = rf"^{key}=.*$"
    if re.search(pattern, content, re.MULTILINE):
        return re.sub(pattern, f"{key}={value}", content, flags=re.MULTILINE)
    return content + f"\n{key}={value}"

lines = []
IG_ID = ""

# Try 1: /page/instagram_accounts with page token
for tok_name, tok in [("PAGE_TOKEN", PAGE_TOKEN), ("LONG_TOKEN", LONG_TOKEN)]:
    if not tok:
        continue
    r = requests.get(f"{GRAPH}/{PAGE_ID}/instagram_accounts",
        params={"access_token": tok, "fields": "id,name,username"}, timeout=10)
    d = r.json()
    lines.append(f"[{tok_name}] /instagram_accounts: {json.dumps(d)[:300]}")
    ig_list = d.get("data", [])
    if ig_list:
        IG_ID = ig_list[0]["id"]
        lines.append(f"GOT IG ID = {IG_ID}")
        break

# Try 2: /page?fields=instagram_business_account with page token
if not IG_ID:
    for tok_name, tok in [("PAGE_TOKEN", PAGE_TOKEN), ("LONG_TOKEN", LONG_TOKEN)]:
        if not tok:
            continue
        r = requests.get(f"{GRAPH}/{PAGE_ID}",
            params={"access_token": tok, "fields": "instagram_business_account"}, timeout=10)
        d = r.json()
        lines.append(f"[{tok_name}] instagram_business_account: {json.dumps(d)[:300]}")
        IG_ID = d.get("instagram_business_account", {}).get("id", "")
        if IG_ID:
            lines.append(f"GOT IG ID = {IG_ID}")
            break

# Save
if IG_ID:
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        env = f.read()
    env = set_env(env, "IG_BUSINESS_ACCOUNT_ID", IG_ID)
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write(env)
    lines.append(f"SAVED to .env: IG_BUSINESS_ACCOUNT_ID={IG_ID}")
else:
    lines.append("FAILED — need new token with pages_read_engagement + instagram_basic")

result = "\n".join(lines)
open(LOG, "w", encoding="utf-8").write(result)
print(result)
