import requests, json, re

LONG_TOKEN = "EAAOTXnXFEFgBR2E4xDg18mDsWv4aiQMcPgAmw8WjzcAPh7BHihxZBnn9DRiUirMAs4LFqvF7RZB5mZAi6BApvNrhVhIQXdG4gKRNnIfrQ1oJvBZBMCLduNGkvgSbXwaKyqoVAP8Q3A98yc5LHfZAN6BRPSm7OLm7HjnGHxIHY9b9bKKmMZAi2HKtz4WjHwTSduPjxdkZCmZBYZBXvjuEKcV1SwPSUTXFdGuxzNS0Yfwkp"
# NEW PAGE TOKEN - generated with pages_read_engagement + pages_manage_posts + pages_show_list
PAGE_TOKEN = "EAAOTXnXFEFgBR3KXuiZBFmpSHmWB1ZAdTShidlRLC0JcfNaLDuhdvf0PpKKX46sycgVxQe0AbDT0tNa7kJO4O1qVz9GTnTv9QgDLdDU966bfO1kTPyP1Aj0cXO5bahNlRSHsgPV4VEw232gY0846cVqn1xiPxcHtBBPZARWhFBZBk7chTKLffj1Sk8HsyQYAeMepp7c4UPNmyCtZC9vOmEZCbVG5DejeJKtPr7jNaqJ24ZD"
PAGE_ID    = "1002823072922245"
GRAPH      = "https://graph.facebook.com/v19.0"
LOG        = r"C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction\ig_check_result.txt"
ENV_PATH   = r"C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction\.env"

def set_env(content, key, value):
    pattern = rf"^{key}=.*$"
    if re.search(pattern, content, re.MULTILINE):
        return re.sub(pattern, f"{key}={value}", content, flags=re.MULTILINE)
    return content + f"\n{key}={value}"

lines = []
IG_ID = ""

# Try 1: /page/instagram_accounts with page token
for tok_name, tok in [("PAGE_TOKEN", PAGE_TOKEN), ("LONG_TOKEN", LONG_TOKEN)]:
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
