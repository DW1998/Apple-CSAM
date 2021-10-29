import hashlib

from Crypto.Cipher import AES
import json
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes
import hmac

dhf_l = (2 ** 64) - 59


def aes128_enc(adkey, ad):
    header = b"header"
    nonce = get_random_bytes(12)
    cipher = AES.new(adkey, AES.MODE_GCM, nonce=nonce)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(ad)

    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = [b64encode(x).decode('utf-8') for x in [cipher.nonce, header, ciphertext, tag]]
    adct = json.dumps(dict(zip(json_k, json_v)))
    print("adct is: %s" % adct)
    return adct


def aes128_dec(adkey, adct):
    try:
        b64 = json.loads(adct)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k: b64decode(b64[k]) for k in json_k}
        cipher = AES.new(adkey, AES.MODE_GCM, nonce=jv['nonce'])
        cipher.update(jv['header'])
        ad = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        print("ad is: %s" % ad)
    except (ValueError, KeyError):
        print("Incorrect decryption")
    return ad


def calc_prf(fkey, id):
    # x, z, x', r' el_of F^2_sh * X * R, X is domain of DHF, R is range of DHF
    message = bytes(id)
    h = hmac.new(fkey, message, hashlib.sha1).hexdigest()
    print(h)
    print(len(h))
    return h


def calc_dhf(hkey, x):
    # K x X -> R, l = 64, s = upper bound of set S, t + 1 = threshold number
    # K := F^s*t_l, X := F_l, R := F^s+1_l
    return 0


def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
        return True
