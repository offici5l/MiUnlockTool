from miunlock.utils import _send
from miunlock.commands import get_device_token, get_product
import random
import hashlib
import io
import subprocess
import time
from pathlib import Path
from migate.config import console


def unlock_device(domain, service, fastboot_cmd):

    cookies = service["cookies"]
    ssecurity = service['servicedata']["ssecurity"]
    deviceId = service['servicedata']["deviceId"]

    r = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=16))
    nonce_resp = _send("/api/v2/nonce", {"r": r}, domain, ssecurity, cookies)
    if "error" in nonce_resp:
        console.print(f"\n[red]{nonce_resp['error']}[/red]\n")
        return
    if nonce_resp["code"] != 0:
        console.print(f"\n[red]{nonce_resp}[/red]\n")
        return
    nonce = nonce_resp["nonce"]

    console.print("\n[green][[/green] [orange]Ensure your Xiaomi device is in fastboot mode[/orange] [green]] < [/green]\n")

    product = get_product(fastboot_cmd)
    if isinstance(product, dict) and "error" in product:
        console.print(f"\n[red]{product['error']}[/red]\n")
        return

    clear = _send("/api/v2/unlock/device/clear", {"appId": "1", "data": {"product": product}, "nonce": nonce}, domain, ssecurity, cookies)
    if "error" in clear:
        console.print(f"\n[red]{clear['error']}[/red]\n")
        return
    if clear["code"] != 0:
        console.print(f"\n[red]{clear}[/red]\n")
        return

    console.print(f"\n[orange]notice: {clear['notice']}[/orange]\n")
    if clear["cleanOrNot"] == 1:
        console.print("\n[red]The device will clear user data when unlocked[/red]\n")
    else:
        console.print("\n[green]Unlocking this device will not erase user data[/green]\n")

    console.input("\n[white]Press 'Enter' to continue — unlock(encryptData)[/white]")

    device_token = get_device_token(fastboot_cmd)
    if isinstance(device_token, dict) and "error" in device_token:
        console.print(f"\n[red]{device_token['error']}[/red]\n")
        return

    data = {
        "clientId": "2",
        "clientVersion": "7.6.727.43",
        "deviceInfo": {"boardVersion": "", "deviceName": "", "product": product, "socId": ""},
        "deviceToken": device_token,
        "language": "en",
        "operate": "unlock",
        "pcId": hashlib.md5(deviceId.encode()).hexdigest(),
        "region": "",
        "uid": cookies.get("userId"),
    }

    unlock_result = _send("/api/v3/ahaUnlock", {"appId": "1", "data": data, "nonce": nonce}, domain, ssecurity, cookies)
    if "error" in unlock_result:
        console.print(f"\n[red]{unlock_result['error']}[/red]\n")
        return
    if unlock_result["code"] != 0:
        if "descEN" in unlock_result:
            console.print(f"\n[orange]code: {unlock_result['code']}\ndescription: {unlock_result['descEN']}[/orange]\n")
        else:
            console.print(f"\n[orange]{unlock_result}[/orange]\n")
        return

    encryptData = unlock_result["encryptData"]
    ed = io.BytesIO(bytes.fromhex(encryptData))
    filename = Path.home() / f"{int(time.time())}encryptData"
    with open(filename, "wb") as edfile:
        edfile.write(ed.getvalue())

    try:
        subprocess.run([fastboot_cmd, "stage", filename], check=True, capture_output=True, text=True)
        subprocess.run([fastboot_cmd, "oem", "unlock"], check=True, capture_output=True, text=True)
        console.print("\n[green]Unlock successful[/green]\n")
    except subprocess.CalledProcessError as e:
        console.print(f"\n[red]{e.stderr}[/red]\n")