import requests
import json
import hashlib

def get_service_data(cookies):
    device_id = cookies.get('deviceId')
    if not device_id:
        return {"error": "Missing deviceId in cookies"}
        
    pcId = hashlib.md5(device_id.encode()).hexdigest()
    url = 'https://account.xiaomi.com/pass/serviceLogin'
    params = {'sid': 'unlockApi'}
    headers = {"User-Agent": "XiaomiPCSuite"}
    
    try:
        r = requests.get(url, params=params, cookies=cookies, headers=headers)

        r.raise_for_status()
        
        if not r.history:
            return {"error": "Request history is empty"}
        
        pragma = r.history[0].headers.get("extension-pragma")
        if not pragma:
            return {"error": "Missing extension-pragma in headers"}
            
        data = json.loads(pragma)
        ssecurity = data.get("ssecurity")
        if not ssecurity:
            return {"error": "Missing ssecurity in response"}
            
        return {"cookies": r.cookies.get_dict(), "ssecurity": ssecurity, "pcId": pcId}
        
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        return {"error": f"Failed to parse response: {e}"}
