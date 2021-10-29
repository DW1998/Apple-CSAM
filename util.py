from Crypto.Cipher import AES
import json
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes


def aes128_enc(adkey, ad):
    header = b"header"
    nonce = get_random_bytes(12)
    cipher = AES.new(adkey, AES.MODE_GCM, nonce=nonce)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(ad)

    json_k = ['nonce', 'header', 'ciphertext', 'tag']
    json_v = [ b64encode(x).decode('utf-8') for x in [cipher.nonce, header, ciphertext, tag]]
    adct = json.dumps(dict(zip(json_k, json_v)))
    print("adct is: %s" % adct)
    return adct


def aes128_dec(adkey, adct):
    try:
        b64 = json.loads(adct)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k:b64decode(b64[k]) for k in json_k}
        cipher = AES.new(adkey, AES.MODE_GCM, nonce=jv['nonce'])
        cipher.update(jv['header'])
        ad = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        print("ad is: %s" % ad)
    except (ValueError, KeyError):
        print("Incorrect decryption")
    return ad
