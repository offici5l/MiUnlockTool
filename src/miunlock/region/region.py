import json
import requests

def region(pass_token):
    headers = {"User-Agent": "XiaomiPCSuite"}
    try:
        response = requests.get(
            "https://account.xiaomi.com/pass/user/login/region",
            headers=headers,
            cookies=pass_token
        )
        response.raise_for_status()
        region_data = json.loads(response.text[11:])
        region = region_data.get("data", {}).get("region")
        if not region:
            return {"error": "Failed to get region"}
        print(f"\nAccount Region: {region}\n")
        return {"success": f"{region}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        return {"error": f"Failed to parse response: {e}"}

