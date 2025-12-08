import os
import time
import platform
import webbrowser
from urllib.parse import urlparse, parse_qs
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

headers = {"User-Agent": "XiaomiPCSuite"}

def create_session_with_retry():
    session = requests.Session()

    retry = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[401],
        allowed_methods=["GET"],
        raise_on_status=False
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def get_creds():
    input("\nPress Enter to open confirmation page, \n copy url after seeing \"R\":\"\",\"S\":\"OK\", \n  and return here")
    config_url = 'https://account.xiaomi.com/pass/serviceLogin?sid=unlockApi&checkSafeAddress=true'
    if platform.system() == "Linux":
        os.system("xdg-open '" + config_url + "'")
    else:
        webbrowser.open(config_url)

    time.sleep(2)
    url = input("\nEnter url: ").strip()
    
    if urlparse(url).netloc != "unlock.update.miui.com":
        return {"error": "Invalid URL"}

    try:
        device_id = parse_qs(urlparse(url).query).get('d', [None])[0]
        if device_id is None:
            return {"error": "Invalid URL"}
    except (ValueError, IndexError):
        return {"error": "Invalid URL"}

    session = create_session_with_retry()
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        user_id = response.cookies.get('userId')
        if user_id:
            return {"user_id": user_id, "device_id": device_id}
        return {"error": "User ID not found in cookies!"}

    if response.status_code == 401:
        print('\nURL(Auth) expired ...')
        return get_creds()

    return {"error": f"Unexpected status code: {response.status_code}"}