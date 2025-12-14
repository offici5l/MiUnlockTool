from .region import region
from .region_config import region_config
from .domain import domain, config_manually

def get_region(pass_token):
    return region(pass_token)

def get_region_config(region):
    return region_config(region)

def get_domain(pass_token):
    region = get_region(pass_token)
    if "error" in region:
        return region
    region_Config = get_region_config(region["success"])    
    if "error" in region_Config:
        return region_Config
    regionConfig = region_Config["regionConfig"]
    _domain = domain(regionConfig)
    user_input = input(f"\nPress 'Enter' to continue\n(type 'm' and press Enter to select it manually)").strip().lower()
    if user_input == 'm':
        manual_region = config_manually()
        _domain = domain(manual_region)

    return _domain