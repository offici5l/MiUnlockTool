from miunlock.login.login import get_pass_token
from miunlock.config import get_domain
from miunlock.service import get_service_data
from miunlock.unlock import unlock_device
from pathlib import Path
from miunlock.platform_tools import check_fastboot

def main():

    fastboot_cmd = check_fastboot()
    if isinstance(fastboot_cmd, dict) and "error" in fastboot_cmd:
        print(f"\n{fastboot_cmd['error']}\n")
        return

    pass_token = get_pass_token()
    if "error" in pass_token:
        print(f"\n{pass_token['error']}\n")
        return

    domain = get_domain(pass_token)
    if "error" in domain:
        print(f"\n{domain['error']}\n")
        return

    service_data = get_service_data(pass_token)
    if "error" in service_data:
        print(f"\n{service_data['error']}\n")
        return
    cookies = service_data["cookies"]
    ssecurity = service_data["ssecurity"]
    pcId = service_data["pcId"]

    unlock = unlock_device(domain, ssecurity, cookies, pcId, fastboot_cmd)

    if "success" in unlock:
        print(f"\n{unlock['success']}\n")
    elif "info" in unlock:
        if "descEN" in unlock['info']:
            print(f"\ncode: {unlock['info']['code']}\ndescription: {unlock['info']['descEN']}\n")
        else:
            print(unlock)
    else:
        print(f"\n{unlock['error']}\n")

    return 

