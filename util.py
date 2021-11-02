import hashlib

from Crypto.Cipher import AES
import json
from base64 import b64encode, b64decode

from Crypto.PublicKey import ECC
from Crypto.Random import get_random_bytes
import hmac
import pem

dhf_l = (2 ** 64) - 59
sh_p = (2 ** 128) - 1
test_num = 339177328369128880911409701061729234965
hash_list = list()
hash_list.append(hashlib.sha1)
hash_list.append(hashlib.sha256)
hash_list.append(hashlib.md5)
hash_list.append(hashlib.sha3_224)
hash_list.append(hashlib.sha3_256)
hash_list.append(hashlib.sha3_384)
hash_list.append(hashlib.sha3_512)
ecc_p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
ecc_q = 115792089210356248762697446949407573529996955224135760342422259061068512044369
ecc_gen_x = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
ecc_gen_y = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
ecc_gen = ECC.EccPoint(x=int(ecc_gen_x), y=int(ecc_gen_y), curve='p256')


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
        return None
    return ad


def calc_prf(fkey, id, s):
    # x, z, x', r' el_of F^2_sh * X * R, X is domain of DHF, R is range of DHF
    h = hmac.new(fkey, bytes(id), hashlib.sha1).hexdigest()
    print("h: %s, length of h: %s" % (h, len(h)))
    print("h as int: %s, length of h as int: %s" % (int.from_bytes(h.encode(), "big"),
                                                    len(str(int.from_bytes(h.encode(), "big")))))
    print("sh_p: %s, length of sh_p: %s" % (sh_p, len(str(sh_p))))
    print("dhf_l: %s, length of dhl_l %s" % (dhf_l, len(str(dhf_l))))
    sh_x = int.from_bytes(h.encode(), "big") % sh_p
    print("sh_x: %s" % sh_x)
    h = hmac.new(fkey, h.encode(), hashlib.sha1).hexdigest()
    sh_z = int.from_bytes(h.encode(), "big") % sh_p
    print("sh_z: %s" % sh_z)
    h = hmac.new(fkey, h.encode(), hashlib.sha1).hexdigest()
    x = int.from_bytes(h.encode(), "big") % dhf_l
    print("x: %s" % x)
    r = list()
    for i in range(0, s + 1):
        h = hmac.new(fkey, h.encode(), hashlib.sha1).hexdigest()
        r.append(int.from_bytes(h.encode(), "big") % dhf_l)
    print("prf r: %s" % r)
    return sh_x, sh_z, x, r


def calc_dhf(hkey, x):
    # K x X -> R, l = 64, s = upper bound of set S, t + 1 = threshold number
    # K := F^s*t_l, X := F_l, R := F^s+1_lk
    r = list()
    r.append(x)
    for p in hkey:
        r.append(calc_poly(x, p) % dhf_l)
    print("dhf r: %s" % r)
    return r


def init_sh_poly(adkey, t):
    a = list()
    a.append(int.from_bytes(adkey, "big"))
    for i in range(1, t + 1):
        a.append(int.from_bytes(get_random_bytes(16), "big") - 1)
    print(a)
    return a


def calc_poly(x, pol):
    res = 0
    for i in range(0, len(pol)):
        res += pol[i] * (x ** i)
    return res % sh_p


def calc_rct(rkey, r, adct, sh):
    json_k = ['r', 'adct', 'sh']
    json_v = [r, adct, sh]
    rct_data = json.dumps(dict(zip(json_k, json_v))).encode()
    print("rct_data is: %s" % rct_data)
    rct = aes128_enc(rkey, rct_data)
    print("rct is: %s" % rct)
    rct_dec = aes128_dec(rkey, rct)
    print("rct_dec is: %s" % rct_dec)
    return rct


def calc_h(u, n_dash, h1_i, h2_i):
    key = b'password'
    h1 = hmac.new(key, u.encode(), hash_list[h1_i]).hexdigest()
    h2 = hmac.new(key, u.encode(), hash_list[h2_i]).hexdigest()
    out1 = int.from_bytes(h1.encode(), "big") % n_dash
    out2 = int.from_bytes(h2.encode(), "big") % n_dash
    return out1, out2


def gen_ecc():
    return


def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
        return True


def H(i):
    out = ecc_gen + ecc_gen
    return out
