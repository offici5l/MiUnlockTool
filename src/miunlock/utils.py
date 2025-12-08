import json
import hashlib
import hmac
import binascii
from base64 import b64encode, b64decode
import requests

from miunlock.aes import aes_cbc_encrypt, aes_cbc_decrypt

def _send(path, params_raw, domain, ssecurity, cookies):

    headers = {"User-Agent": "XiaomiPCSuite"}
    ssecurity_key = b64decode(ssecurity)    
    iv = b'0102030405060708'
    key = b'2tBeoEyJTunmWUGq7bQH2Abn0k2NhhurOaqBfyxCuLVgn4AVj7swcawe53uDUno'
    params_raw["sid"] = "miui_unlocktool_client"

    if 'data' in params_raw:
        params_raw['data'] = json.dumps(params_raw['data'])
        params_raw['data'] = b64encode(params_raw['data'].encode()).decode()

    param_order = sorted(params_raw.keys())
    
    sign_params = '&'.join(f"{k}={params_raw[k]}" for k in param_order)

    sign_str = f"POST\n{path}\n{sign_params}"

    sign_hash_hex = binascii.hexlify(hmac.new(key, sign_str.encode(), hashlib.sha1).digest()).decode().encode()

    pad_len = 16 - len(sign_hash_hex) % 16
    padded_sign = sign_hash_hex + bytes([pad_len]) * pad_len
    
    current_sign = b64encode(aes_cbc_encrypt(padded_sign, ssecurity_key, iv)).decode()

    encoded_params = []
    for k in param_order:
        data = params_raw[k].encode()
        pad_len = 16 - len(data) % 16
        padded_data = data + bytes([pad_len]) * pad_len
        encrypted = b64encode(aes_cbc_encrypt(padded_data, ssecurity_key, iv)).decode()
        encoded_params.append(f"{k}={encrypted}")
    
    encoded_params.extend([f"sign={current_sign}", ssecurity])

    sha1_input = f"POST&{path}&{'&'.join(encoded_params)}"

    signature = b64encode(hashlib.sha1(sha1_input.encode()).digest()).decode()

    post_params = {}
    for k in param_order:
        data = params_raw[k].encode()
        pad_len = 16 - len(data) % 16
        padded_data = data + bytes([pad_len]) * pad_len
        post_params[k] = b64encode(aes_cbc_encrypt(padded_data, ssecurity_key, iv)).decode()
    
    post_params.update({'sign': current_sign, 'signature': signature})
    
    try:
        response = requests.post(f"{domain}{path}", params=post_params, cookies=cookies, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return {"error": "network request failed"}

    if not response.text:
        return {"error": "empty response"}

    if len(response.text) % 4 != 0:
        return {"error": "invalid base64 response"}

    try:
        encrypted_data = b64decode(response.text)
        decrypted = aes_cbc_decrypt(encrypted_data, ssecurity_key, iv)
    except:
        return {"error": "decrypt failed"}

    if not decrypted:
        return {"error": "empty decrypted data"}
    if len(decrypted) % 16 != 0:
        return {"error": "decrypted data not aligned"}

    pad_len = decrypted[-1]
    if pad_len < 1 or pad_len > 16:
        return {"error": "invalid padding length"}
    if decrypted[-pad_len:] != bytes([pad_len]) * pad_len:
        return {"error": "invalid padding"}

    clean_data = decrypted[:-pad_len]

    try:
        inner_b64 = b64decode(clean_data)
    except:
        return {"error": "inner base64 invalid"}

    try:
        clean_response = json.loads(inner_b64.decode())
        if "code" in clean_response:
            return clean_response
        else:
            return {"error": clean_response}
    except:
        return {"error": "json parse failed"}