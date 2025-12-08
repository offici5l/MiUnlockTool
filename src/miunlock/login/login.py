import os
import json
import hashlib
import time
import platform
import webbrowser
from urllib.parse import urlparse, parse_qs
import requests
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pathlib import Path
import subprocess
import platform
import pickle
from pathlib import Path
from .captcha_verify import verify
from .verification import verification
from .auth_utils import get_creds

cookies_file = Path.home() / ".miunlock" / "cookies.pkl"

headers = {"User-Agent": "XiaomiPCSuite"}

def get_pass_token():

    if cookies_file.exists():
        pass_token = pickle.load(open(cookies_file, "rb"))
        choice = input(f"\nAlready logged in\nAccount ID: {pass_token['userId']}\n\nPress 'Enter' to continue\n(To log out, type 2 and press Enter.)").strip().lower()
        if choice == "2":
            cookies_file.unlink()
        else:
            return pass_token

    creds = get_creds()
    if "error" in creds:
        return creds
        
    user_id = creds["user_id"]
    print(f'\naccount id: {user_id}')

    device_id = creds["device_id"]

    response = requests.get('https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi', headers=headers, cookies={'deviceId': creds["device_id"]})
    cookies = response.cookies.get_dict()

    pwd = hashlib.md5(input("\nEnter password: ").encode()).hexdigest().upper()

    data = {'_json':'true','callback':'https://unlock.update.miui.com/sts','sid':'unlockApi','qs':'%3Fsid%3DunlockApi','_sign':'CiofaOM8ndWC+UjNoI6pjSx8sPM=','serviceParam':'{"checkSafePhone":false,"checkSafeAddress":false,"lsrp_score":0.0}','_locale':'en_US','useManMachine':'false','user':user_id, 'hash': pwd}

    response = requests.post("https://account.xiaomi.com/pass/serviceLoginAuth2", data=data, headers=headers, cookies=cookies)
        
    response_text = json.loads(response.text[11:])

    if response_text.get("code") == 70016:
        return {"error": "Invalid password"}      
    elif response_text.get("code") == 87001:
        print('\nCAPTCHA verification required !')
        cookies = verify(response_text["captchaUrl"], response.cookies.get_dict(), data)
    elif 'notificationUrl' in response_text:
        notificationUrl = response_text.get("notificationUrl")
        if "BindAppealOrSafePhone" in notificationUrl:
            return {"error": "Please link the account to a phone number, then try again."} 
        elif "SetEmail" in notificationUrl:
            return {"error": "Please link your account to an email address and then try again."}
        else:
            print('\nverification required !')
            cookies = verification(notificationUrl, cookies, data)
            if "error" in cookies:
                return cookies
    else:
        cookies = response.cookies.get_dict()
        if 'passToken' not in cookies:
            return {"error": "pass token was not found"}

    required = {"deviceId", "passToken", "userId"}
    missing = required - cookies.keys()
    if missing:
        return {"error": f"Missing keys: {', '.join(missing)}"}
    cookies = {k: v for k, v in cookies.items() if k in required}

    cookies_file.parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(cookies, open(cookies_file, "wb"))
    print("Login successful")

    return cookies
        
    