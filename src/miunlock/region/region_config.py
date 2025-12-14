import json
import requests

def region_config(region):
    headers = {"User-Agent": "XiaomiPCSuite"}
    try:
        response = requests.get("https://account.xiaomi.com/pass2/config?key=regionConfig", headers=headers)
        response.raise_for_status()
        config_data = json.loads(response.text[11:])
        region_config_dict = config_data.get("regionConfig", {})
        
        region_config = next(
            (k for k, v in region_config_dict.items()
             if v.get("region.codes") and region in v["region.codes"]),
            None
        )
        
        if not region_config:
            return {"error": f"Region config not found for region: {region}"}

        print(f"\nregionConfig: {region_config}\n")

        return {"regionConfig": region_config}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        return {"error": f"Failed to parse response: {e}"}