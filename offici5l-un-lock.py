import re, requests, json, hmac, random, binascii, urllib, hashlib, os, urllib.parse, time, codecs, sys, webbrowser, io
from urllib3.util.url import Url
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from termcolor import colored
from urllib.parse import urlparse

filename = "account_info.txt"



text_to_print = """
Go to Settings » Additional settings » Developer options:\n\n- Enable OEM unlocking and USB debugging.\n- Tap Mi Unlock status » Agree » Add account and device.\n\n"After successful binding, you'll see a confirmation message: Added successfully."
"""
input(colored(f"\n{'='*15}github.com/offici5l/MiTool{'='*15}\n{text_to_print}\n{'='*56}\n", 'green') + "\nIf you complete the steps successfully, press Enter")

while os.path.isfile(filename):
    pr = input(f"\ndo you want to use previous information in \033[92m{filename}\033[0m (yes/no) ? : ").lower()
    if pr == "yes":
        break
    elif pr == "no":
        os.remove(filename)
        break
    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")



with open(filename, "a+") as file:
    file.seek(0)
    content = file.read()
    if "Username:" not in content:
        username = input("Enter username or email or number (Xiaomi Account): ")
        file.write(f"\nUsername: {username}\n")
    if "Password:" not in content:
        password = input("Enter password: ")
        file.write(f"\nPassword: {password}\n")
    if "command:" not in content:
        c = input("Use 1 for Windows, 2 for Mac, or 3 for Linux: ")
        if c == "1":
            file.write(f"\ncommand: fastboot\n")
        elif c == "2":
            file.write(f"\ncommand: ./fastboot\n")
        elif c == "3":
            file.write(f"\ncommand: fastboot\n")
        else:
            print("Invalid choice. exit")
            exit()

if "wb_value:" not in open(filename).read():
    input("\nPress Enter to open confirmation page in your default browser. After seeing {\"R\":\"\",\"S\":\"OK\"}, copy Link from address bar. Come back here")
    webbrowser.open('https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&checkSafeAddress=true')
    wbinput = input("\nEnter Link: ")
    wbinput_list = wbinput.split('sts?d=')

    if len(wbinput_list) > 1:
        wbinputmatch = wbinput_list[1].split('&ticket')[0]

        with open(filename, "a") as file:
            file.write(f"\nwb_value: {wbinputmatch}\n")
    else:
        print("Invalid URL")
        exit()

username = next((line.split(' ', 1)[1].strip() for line in open(filename) if "Username:" in line), None)
password = next((line.split(' ', 1)[1].strip() for line in open(filename) if "Password:" in line), None)

headers={"User-Agent": "XiaomiPCSuite"}
session = requests.Session()

response = session.post("https://account.xiaomi.com/pass/serviceLoginAuth2?sid=unlockApi&_json=true", data={"user": username, "hash": hashlib.md5(password.encode()).hexdigest().upper()}, headers=headers, cookies={"deviceId": next((line.split(' ', 1)[1].strip() for line in open(filename) if "wb_value:" in line), None)}).text.replace("&&&START&&&", "")

if json.loads(response)["securityStatus"] == 16:
    error_message = f'\n\033[91msecurityStatus {json.loads(response)["securityStatus"]}\033[0m\n\n\033[92mPlease go to: settings > Mi Account > Devices > select Current device > Find device "enable Find device"\033[0m\n'
    print(error_message)
    exit()

if json.loads(response)["code"] == 70016:
    error_message = f'\n\033[91mcodeStatus {json.loads(response)["code"]} Error descEN: The account ID or password you entered is incorrect. \n\033[0m'
    print(error_message)
    exit()

region = re.search(r'p_idc=(.*?)&nonce', response).group(1)

final_region = region if region.lower() in ['india', 'europe', 'russia', 'china'] else 'Global'

region_urls = {
    "India": "https://in-unlock.update.intl.miui.com",
    "Global": "https://unlock.update.intl.miui.com",
    "China": "https://unlock.update.miui.com",
    "Russia": "https://ru-unlock.update.intl.miui.com",
    "Europe": "https://eu-unlock.update.intl.miui.com"
}

url = region_urls.get(final_region, '')

result2 = response.replace(response.split('"location":"')[1].split('/sts?d=')[0], url)

data = json.loads(result2)

ssecurity, psecurity, userid, c_userid, code, nonce, location = (data["ssecurity"], data["psecurity"], data["userId"], data["cUserId"], data["code"], data["nonce"], data["location"])

response_cookies = session.get( location + "&clientSign=" + urllib.parse.quote_plus(b64encode(hashlib.sha1(f"nonce={nonce}".encode("utf-8") + b"&" + ssecurity.encode("utf-8")).digest())), headers=headers ).cookies

cookies = response_cookies

if not cookies:
    wbe = next((line.split(' ', 1)[1].strip() for line in open(filename) if "wb_value:" in line), None)
    error_message = f'\n\033[91mdescEN: Error information not obtained from server.\nInvalid wb_value: {wbe} \n\033[0m\033[92m'
    print(error_message)
    exit()
else:
    pass

cmd = next((line.split(' ', 1)[1].strip() for line in open(filename) if "command:" in line), None)

with open(filename, "a+") as file:
    file.seek(0)
    content = file.read()
    if "token:" not in content or "product:" not in content:
        input("\nConnect the device in Fastboot mode and press Enter\033[0m ") 
        output = os.popen(f"{cmd} getvar all 2>&1").read()
        token_match = re.search(r"token:(.*)", output)
        product_match = re.search(r"product:(.*)", output)
        token = token_match.group(1).strip() if token_match else None
        product = product_match.group(1).strip() if product_match else None
        print("\ndevice token:")
        print(token)
        print("\ndevice product:")
        print(product)
        file.write(f"\ntoken: {token}\nproduct: {product}\n")

params = {k.encode("utf-8") if isinstance(k, str) else k: v.encode("utf-8") if isinstance(v, str) else b64encode(json.dumps(v).encode("utf-8")) if not isinstance(v, bytes) else v for k, v in {"appId": "1", "data": {"clientId": "2", "clientVersion": "5.5.224.55", "language": "en", "operate": "unlock", "pcId": hashlib.md5(next((line.split(' ', 1)[1].strip() for line in open(filename) if "wb_value:" in line), None).encode("utf-8")).hexdigest(), "product": next((line.split(' ', 1)[1].strip() for line in open(filename) if "product:" in line), None), "deviceInfo": {"product": next((line.split(' ', 1)[1].strip() for line in open(filename) if "product:" in line), None)}, "deviceToken": next((line.split(' ', 1)[1].strip() for line in open(filename) if "token:" in line), None)}
}.items()}

psiggn = bytes.fromhex("327442656f45794a54756e6d57554771376251483241626e306b324e686875724f61714266797843754c56676e3441566a3773776361776535337544556e6f")

def get_params(sep):
    return b"POST" + sep + "/api/v3/ahaUnlock".encode("utf-8") + sep + b"&".join([k + b"=" + v for k, v in params.items()])

def add_sign():
    params[b"sign"] = binascii.hexlify(hmac.digest(psiggn, get_params(b"\n"), "sha1"))

def _encrypt(value):
    return b64encode(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").encrypt((lambda s: s + (16 - len(s) % 16) * bytes([16 - len(s) % 16]))(value)))

def encrypt():
    params.update({k: _encrypt(v) for k, v in params.items()})

def add_signature():
    params[b"signature"] = b64encode(hashlib.sha1(get_params(b"&") + b"&" + ssecurity.encode("utf-8")).digest())

def add_nonce():
    r = unlock_device_request("/api/v2/nonce", {"r": ''.join(random.choices(list("abcdefghijklmnopqrstuvwxyz"), k=16)), "sid": "miui_unlocktool_client"})
    params[b"nonce"], params[b"sid"] = r["nonce"].encode("utf-8"), b"miui_unlocktool_client"

def _decrypt(value):
    ret = b64decode((lambda s: s[:-s[-1]])(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").decrypt(b64decode(value))))
    return ret

def run():
    add_sign()
    encrypt()
    add_signature()
    return json.loads(send())

def send():
    response = session.request("POST", Url(host=url, path="/api/v3/ahaUnlock").url, data=params, headers=headers, cookies=cookies)
    response.raise_for_status()
    return _decrypt(response.text)

def unlock_device_request(endpoint, params):
    request_params = {k.encode("utf-8") if isinstance(k, str) else k: v.encode("utf-8") if isinstance(v, str) else b64encode(json.dumps(v).encode("utf-8")) if not isinstance(v, bytes) else v for k, v in params.items()}

    def get_request_params(sep):
        return b"POST" + sep + endpoint.encode("utf-8") + sep + b"&".join([k + b"=" + v for k, v in request_params.items()])

    def add_sign():
        request_params[b"sign"] = binascii.hexlify(hmac.digest(psiggn, get_request_params(b"\n"), "sha1"))

    def _encrypt(value):
        return b64encode(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").encrypt((lambda s: s + (16 - len(s) % 16) * bytes([16 - len(s) % 16]))(value)))

    def encrypt():
        request_params.update({k: _encrypt(v) for k, v in request_params.items()})

    def add_signature():
        request_params[b"signature"] = b64encode(hashlib.sha1(get_request_params(b"&") + b"&" + ssecurity.encode("utf-8")).digest())

    def add_nonce():
        r = unlock_device_request("/api/v2/nonce", {"r": ''.join(random.choices(list("abcdefghijklmnopqrstuvwxyz"), k=16)), "sid": "miui_unlocktool_client"})
        request_params[b"nonce"], request_params[b"sid"] = r["nonce"].encode("utf-8"), b"miui_unlocktool_client"

    def _decrypt(value):
        ret = b64decode((lambda s: s[:-s[-1]])(AES.new(b64decode(ssecurity), AES.MODE_CBC, b"0102030405060708").decrypt(b64decode(value))))
        return ret

    def run():
        add_sign()
        encrypt()
        add_signature()
        return json.loads(send())

    def send():
        response = session.request("POST", Url(host=url, path=endpoint).url, data=request_params, headers=headers, cookies=cookies)
        response.raise_for_status()
        return _decrypt(response.text)

    return run()

add_nonce()
result = run()
session.close()

code = result.get("code", "")
descEN = result.get("descEN", "")

if "code" in result and result["code"] == 10000:
    print(f"\ncode: {code} descEN: {descEN}\nInvalid device token or product.\n")
    with open(filename, "r") as file:
        lines = [line for line in file.readlines() if "token:" not in line and "product:" not in line]
    with open(filename, "w") as file:
        file.writelines(lines)
    exec("\n".join(line for i, line in enumerate(codecs.open('offici5l-un-lock.py', 'r', 'utf-8').read().split('\n'), 1) if i not in range(10, 27)))
    exit()

if "encryptData" in result:
    unlock_token = result["encryptData"]
    binary_data = bytes.fromhex(unlock_token)
    bytes_io_data = io.BytesIO(binary_data)
    with open("token.bin", "wb") as token_file:
        token_file.write(bytes_io_data.getvalue())
    input("\nConnect the device in Fastboot mode and press Enter\033[0m ")
    time.sleep(3)
    os.system(f"{cmd} stage token.bin")
    time.sleep(3)
    os.system(f"{cmd} oem unlock")
else:
    formatted_result = json.dumps(result, indent=0, ensure_ascii=False, separators=('\n', ': '))[1:-1].replace('"', '')
    framed_result = colored(f"\n{'='*56}\n{formatted_result}\n{'='*56}\n", 'green')
    print(framed_result)

input("Press Enter to exit...")