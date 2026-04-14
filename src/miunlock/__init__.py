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
    param = {"sid": service_id}
    param["checkSafeAddress"] = True

    passToken = migate.get_passtoken(param)
   
    service = migate.get_service(passToken, param)
    cookies = service["cookies"]
    ssecurity = service['servicedata']["ssecurity"]
    deviceId = service['servicedata']["deviceId"]

    pcId = hashlib.md5(deviceId.encode()).hexdigest()

    domain = get_domain(passToken)
    if "error" in domain:
        console.print(f"\n[red]{domain['error']}[/red]\n")
        return

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

