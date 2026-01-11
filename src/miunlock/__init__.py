from miunlock.login.login import get_pass_token
from miunlock.region.config import get_domain
from miunlock.service import get_service_data
from miunlock.unlock import unlock_device
from pathlib import Path
from miunlock.config import config_s
import hashlib
from colorama import init, Fore

def main():
    init(autoreset=True)

    result = config_s()    
    if "error" in result:
        print(f"\n{Fore.RED}{result['error']}\n")
        return
    else:
        fastboot_cmd = result['path']

    pass_token = get_pass_token()
    if "error" in pass_token:
        print(f"\n{Fore.RED}{pass_token['error']}\n")
        return
   
    pcId = hashlib.md5(pass_token.get('deviceId').encode()).hexdigest()

    domain = get_domain(pass_token)
    if "error" in domain:
        print(f"\n{Fore.RED}{domain['error']}\n")
        return

    service_data = get_service_data(pass_token)
    if "error" in service_data:
        print(f"\n{Fore.RED}{service_data['error']}\n")
        return
    cookies = service_data["cookies"]
    ssecurity = service_data["ssecurity"]

    unlock = unlock_device(domain, ssecurity, cookies, pcId, fastboot_cmd)

    if "success" in unlock:
        print(f"\n{Fore.GREEN}{unlock['success']}\n")
    elif "info" in unlock:
        if "descEN" in unlock['info']:
            print(f"\n{Fore.YELLOW}code: {unlock['info']['code']}\ndescription: {unlock['info']['descEN']}\n")
        else:
            print(f"\n{Fore.YELLOW}{unlock}\n")
    else:
        print(f"\n{Fore.RED}{unlock['error']}\n")

    return 

