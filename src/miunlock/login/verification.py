import json
import time
import platform
import requests
from pathlib import Path
import subprocess

headers = {"User-Agent": "XiaomiPCSuite"}

def verification(notificationUrl, cookies, data):
    response = requests.get(notificationUrl, headers=headers, cookies=cookies)
    cookies.update(response.cookies.get_dict())

    urllist = notificationUrl.replace(
        "https://account.xiaomi.com/identity/authStart?",
        "https://account.xiaomi.com/identity/list?"
    )

    response = requests.get(urllist, headers=headers, cookies=cookies)
    cookies.update(response.cookies.get_dict())

    resultJson = json.loads(response.text[11:])
    options = resultJson.get('options', [])

    if 8 in options and 4 in options:
        while True:
            print("\nChoose verification method:")
            print("1 = phone verification (CAPTCHA required)")
            print("2 = email verification")
            choice = input("Enter 1 or 2: ").strip()
            if choice == "1":
                method = "Phone"
                break
            elif choice == "2":
                method = "Email"
                break
            else:
                print("\nInvalid choice!\n")
    elif 4 in options:
        method = "Phone"
    elif 8 in options:
        method = "Email"
    else:
        return {"error": resultJson}

    base = "https://account.xiaomi.com"
    urlsv = base + "/identity/auth/"
    urlsend = urlsv + "send" + method + "Ticket"
    urlverify = urlsv + "verify" + method

    data_icode = {'icode': "", '_json': "true"}

    while True:
        r2 = requests.post(urlsend, data=data_icode, cookies=cookies, headers=headers)
        r2_text = json.loads(r2.text[11:])

        if r2_text.get("code") == 87001:
            print(r2_text.get("reason", ""))
            captchaUrl = r2_text.get("captchaUrl")
            path = Path.home() / f"{int(time.time())}_captcha.jpg"

            rc = requests.get(f"{base}{captchaUrl}", cookies=cookies, headers=headers)
            cookies.update(rc.cookies.get_dict())

            with open(path, "wb") as f:
                f.write(rc.content)

            input('\nPress Enter to open the CAPTCHA image')

            if platform.system() == 'Windows':
                subprocess.run(['start', str(path)], shell=True)
            elif platform.system() == 'Darwin':
                subprocess.run(['open', str(path)])
            else:
                subprocess.run(['xdg-open', str(path)])

            print(f"\nCaptcha displayed from {path}")

            icode = input("\nEnter captcha code: ").strip()
            data_icode.update({'icode': icode})

            path.unlink()

        elif r2_text.get("code") == 0:
            print(f"\nVerification code sent to your {method}")
            break
        else:
            if r2_text.get("code") == 70022:
                return {"error": r2_text.get("tips", "Unknown error")}
            else:
                return {"error": r2_text}

    while True:
        ticket = input("Enter code: ").strip()
        send_data = {
            "ticket": ticket,
            "trust": "true"
        }
        r3 = requests.post(urlverify, data=send_data, headers=headers, cookies=cookies)
        r3_text = json.loads(r3.text[11:])

        if r3_text.get("code") == 70014:
            print(r3_text.get("tips", ""))
            continue
        elif r3_text.get("code") == 0:
            break
        else:
            return {"error": r3_text}

    location = r3_text.get('location')
    cookies.update(r3.cookies.get_dict())

    r4 = requests.get(location, headers=headers, cookies=cookies, allow_redirects=False)
    cookies.update(r4.cookies.get_dict())

    end_url = r4.headers.get("Location")

    r5 = requests.get(end_url, headers=headers, cookies=cookies, allow_redirects=False)
    cookies.update(r5.cookies.get_dict())

    r6 = requests.post("https://account.xiaomi.com/pass/serviceLoginAuth2", data=data, headers=headers, cookies=cookies)

    cookies = r6.cookies.get_dict()
    if 'passToken' not in cookies:
        return {"error": "verification: pass token was not found"}

    return cookies