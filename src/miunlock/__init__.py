from miunlock.region.config import get_domain
from miunlock.unlock import unlock_device
from pathlib import Path
from miunlock.config import config_s
import hashlib
from migate.config import (
    console
)
import migate

def main():


    result = config_s()    
    if "error" in result:
        console.print(f"\n[red]{result['error']}[/red]\n")
        return
    else:
        fastboot_cmd = result['path']
    
    service_id = 'unlockApi'
    service_param = {"sid": service_id}
    service_param["checkSafeAddress"] = True

    pass_token = migate.get_passtoken(service_param)
    if "error" in pass_token:
        console.print(f"\n[red]{pass_token['error']}[/red]\n")
        return
   
    pcId = hashlib.md5(pass_token.get('deviceId').encode()).hexdigest()

    domain = get_domain(pass_token)
    if "error" in domain:
        console.print(f"\n[red]{domain['error']}[/red]\n")
        return

    service_data = migate.get_service(pass_token, service_id)
    if "error" in service_data:
        console.print(f"\n[red]{service_data['error']}[/red]\n")
        return
    cookies = service_data["cookies"]
    ssecurity = service_data['servicedata']["ssecurity"]

    unlock = unlock_device(domain, ssecurity, cookies, pcId, fastboot_cmd)

    if "success" in unlock:
        console.print(f"\n[green]{unlock['success']}[/green]\n")
    elif "info" in unlock:
        if "descEN" in unlock['info']:
            console.print(f"\n[orange]code: {unlock['info']['code']}\ndescription: {unlock['info']['descEN']}[/orange]\n")
        else:
            console.print(f"\n[orange]{unlock}[/orange]\n")
    else:
        console.print(f"\n[red]{unlock['error']}[/red]\n")

    return 

