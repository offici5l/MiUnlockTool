from miunlock.utils import _send
from miunlock.commands import get_device_token, get_product
import random
import hashlib
import io
import subprocess
import os
import time
from pathlib import Path

def unlock_device(domain, ssecurity, cookies, pcId, fastboot_cmd):
        
    r = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=16))
    params_raw = {"r": r}
    nonce_resp = _send("/api/v2/nonce", params_raw, domain, ssecurity, cookies)

    if "error" in nonce_resp:
        return nonce_resp
    elif nonce_resp["code"] != 0:
        return {"error": nonce_resp}
    else:
        nonce = nonce_resp.get("nonce")

    print("\nEnsure your Xiaomi device is in fastboot mode ...\n")

    product = get_product(fastboot_cmd)

    data = {"product": product}
    params_raw = {"appId": "1", "data": data, "nonce": nonce}
    clear = _send("/api/v2/unlock/device/clear", params_raw, domain, ssecurity, cookies)

    if "error" in clear:
        return clear
    elif clear["code"] != 0:
        return {"error": clear}
    else:
        print('notice:', clear["notice"])
        if clear['cleanOrNot'] == 1:
            print('\nThe device will clear user data when unlocked')
        else:
            print('\nUnlocking this device will not erase user data')

    input("\nPress 'Enter' to continue — unlock(encryptData)")

    device_token = get_device_token(fastboot_cmd)

    data = {
        "clientId": "2",
        "clientVersion": "7.6.727.43",
        "deviceInfo": {
            "boardVersion": "",
            "deviceName": "",
            "product": product,
            "socId": ""
        },
        "deviceToken": device_token,
        "language": "en",
        "operate": "unlock",
        "pcId": hashlib.md5(pcId.encode()).hexdigest(),
        "region": "",
        "uid": cookies.get("userId")
    }

    params_raw =  {"appId": "1", "data": data, "nonce": nonce}
    unlock_result = _send("/api/v3/ahaUnlock", params_raw, domain, ssecurity, cookies)

    if "error" in unlock_result:
        return unlock_result
    elif unlock_result["code"] != 0:
        return {'info': unlock_result}
    else:
        encryptData = unlock_result["encryptData"]
        ed = io.BytesIO(bytes.fromhex(encryptData))
        filename = Path.home() / f"{int(time.time())}encryptData"
        with open(filename, "wb") as edfile:
            edfile.write(ed.getvalue())
        print(f"\nEncrypted data saved to: {filename}")
        try:
            result_stage = subprocess.run([fastboot_cmd, "stage", filename], check=True, capture_output=True, text=True)
            result_unlock = subprocess.run([fastboot_cmd, "oem", "unlock"], check=True, capture_output=True, text=True)
            return {"success": "Unlock successful"}
        except subprocess.CalledProcessError as e:
            return {'error': e.stderr}