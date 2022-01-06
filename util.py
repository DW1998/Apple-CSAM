import hashlib
import json
import hmac

from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.PublicKey import ECC
from Crypto.Random import get_random_bytes
from math import ceil

# Parent Directory (change this for different saving folder)
parent_dir = "D:/Apple-CSAM-Files/"
clients_dir = parent_dir + "Clients/"
mal_img_dir = parent_dir + "Malicious-Images/"
dec_img_dir = parent_dir + "Decrypted-Images/"
client_id_file = "Client_IDs.csv"
collide_dir = parent_dir + "Collide-Attacks/"

dhf_l = (2 ** 64) - 59
sh_p = 340282366920938463463374607431768211297
hash_func_list = list()
hash_func_list.append(hashlib.sha1)
hash_func_list.append(hashlib.sha256)
hash_func_list.append(hashlib.md5)
hash_func_list.append(hashlib.sha3_224)
hash_func_list.append(hashlib.sha3_256)
hash_func_list.append(hashlib.sha3_384)
hash_func_list.append(hashlib.sha3_512)
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
    return adct


def aes128_dec(adkey, adct):
    try:
        b64 = json.loads(adct)
        json_k = ['nonce', 'header', 'ciphertext', 'tag']
        jv = {k: b64decode(b64[k]) for k in json_k}
        cipher = AES.new(adkey, AES.MODE_GCM, nonce=jv['nonce'])
        cipher.update(jv['header'])
        ad = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
    except (ValueError, KeyError):
        return None
    return ad


def calc_prf(fkey, id, s):
    # x, z, x', r' el_of F^2_sh * X * R, X is domain of DHF, R is range of DHF
    h = hmac.new(fkey, bytes(id), hashlib.sha1).hexdigest()
    sh_x = int.from_bytes(h.encode(), "big") % sh_p
    h = hmac.new(fkey, h.encode(), hashlib.sha1).hexdigest()
    sh_z = int.from_bytes(h.encode(), "big") % sh_p
    h = hmac.new(fkey, h.encode(), hashlib.sha1).hexdigest()
    x = int.from_bytes(h.encode(), "big") % dhf_l
    r = list()
    for i in range(0, s + 1):
        h = hmac.new(fkey, h.encode(), hashlib.sha1).hexdigest()
        r.append(int.from_bytes(h.encode(), "big") % dhf_l)
    return sh_x, sh_z, x, r


def calc_dhf(hkey, x):
    # K x X -> R, l = 64, s = upper bound of set S, t + 1 = threshold number
    # K := F^s*t_l, X := F_l, R := F^s+1_lk
    r = list()
    r.append(x)
    for p in hkey:
        r.append(calc_poly(x, p) % dhf_l)
    return r


def init_sh_poly(adkey, t):
    a = list()
    a.append(int.from_bytes(adkey, "big"))
    for i in range(1, t + 1):
        a.append(int.from_bytes(get_random_bytes(16), "big") - 1)
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
    rct = aes128_enc(rkey, rct_data)
    rct_dec = aes128_dec(rkey, rct)
    return rct


def calc_h(u, n_dash, h1_i, h2_i):
    key = b'password'
    h1 = hmac.new(key, u.encode(), hash_func_list[h1_i]).hexdigest()
    h2 = hmac.new(key, u.encode(), hash_func_list[h2_i]).hexdigest()
    out1 = int.from_bytes(h1.encode(), "big") % n_dash
    out2 = int.from_bytes(h2.encode(), "big") % n_dash
    return out1, out2


def calc_H(x):
    int_x = int.from_bytes(x.encode(), "big") % ecc_q
    h = int_x * ecc_gen
    return h


def hmac_sha256(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()


def calc_H_dash(ikm):
    salt = b""
    info = b""
    ikm_bytes = int(ikm.x).to_bytes(32, "big")
    length = 16
    hash_len = 32
    if len(salt) == 0:
        salt = bytes([0] * hash_len)
    prk = hmac_sha256(salt, ikm_bytes)
    t = b""
    okm = b""
    for i in range(ceil(length / hash_len)):
        t = hmac_sha256(prk, t + info + bytes([1 + i]))
        okm += t
    return okm[:length]


def calc_ct(H_dash_S, rkey):
    ct = aes128_enc(H_dash_S, rkey)
    return ct


def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def recon_adkey(shares):
    values = list()
    for s in shares:
        sh = json.loads(s)
        values.append((sh['x'], sh['z']))
    adkey = 0
    for v in values:
        temp = 1
        for other in values:
            if v is not other:
                temp = (temp * (0 - other[0] * pow(v[0] - other[0], -1, sh_p))) % sh_p
        temp = (temp * v[1]) % sh_p
        adkey = (adkey + temp) % sh_p
    return adkey


def dec_image(tup, path):
    f = open(f"{path}{tup[0].png}", 'wb')
    f.write(tup[1])
    f.close()
