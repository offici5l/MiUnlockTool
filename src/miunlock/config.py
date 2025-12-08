import json
import requests

def get_domain_by_region(region_config=None):
    domains = {
        "Singapore": "https://unlock.update.intl.miui.com",
        "China": "https://unlock.update.miui.com",
        "India": "https://in-unlock.update.intl.miui.com",
        "Russia": "https://ru-unlock.update.intl.miui.com",
        "Europe": "https://eu-unlock.update.intl.miui.com",
    }
    
    if region_config is None:
        return list(domains.keys())
    
    return domains.get(region_config)

def select_region_manually():
    available_regions = get_domain_by_region()
    
    print("\n" + "="*50)
    print("Available Regions:")
    for idx, region in enumerate(available_regions, 1):
        print(f"  {idx}. {region}")
    print("="*50)
    
    while True:
        choice = input(f"\nSelect region number (1-{len(available_regions)}): ").strip()
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_regions):
                selected = available_regions[choice_idx]
                print(f"\nregionConfig Selected: {selected}")
                return selected
            else:
                print(f"\nInvalid choice. Please enter a number between 1 and {len(available_regions)}.")
        except ValueError:
            print(f"\nInvalid input. Please enter a number between 1 and {len(available_regions)}.")



def get_region_config(pass_token):
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
        print(f"\nAccount Region: {region}")
        response = requests.get(
            "https://account.xiaomi.com/pass2/config?key=regionConfig",
            headers=headers,
            cookies=pass_token
        )
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

        return {"region_config": region_config}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        return {"error": f"Failed to parse response: {e}"}

def get_domain(pass_token):
    regionConfig = get_region_config(pass_token)
    if "error" in regionConfig:
        return regionConfig

    user_input = input(f"\nregionConfig: {regionConfig['region_config']}\n\nPress 'Enter' to continue\n(type 'm' and press Enter to select it manually)").strip().lower()

    if user_input == 'm':
        manual_region = select_region_manually()
        if manual_region:
            regionConfig["region_config"] = manual_region

    domain = get_domain_by_region(regionConfig["region_config"])
    if not domain:
        return {"error": "Failed to get domain for the region"}

    return domain