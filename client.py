import json

from Crypto.Random import get_random_bytes

import util

# Parent Directory
parent_dir = "D:/Apple-CSAM-Files/"
clients_dir = parent_dir + "Clients/"


class Voucher:
    def __init__(self, id, Q1, ct1, Q2, ct2, rct):
        self.id = id
        self.Q1 = Q1
        self.ct1 = ct1
        self.Q2 = Q2
        self.ct2 = ct2
        self.rct = rct


class Client:
    def __init__(self, id, server):
        self.id = id
        self.server = server
        self.triples = list()
        self.hkey = list()  # DHF, K
        for i in range(1, server.s + 1):
            p = list()
            for j in range(0, server.t):
                a = int.from_bytes(get_random_bytes(16), "big") % util.dhf_l
                p.append(a)
            self.hkey.append(p)
        print(len(self.hkey))
        print(len(self.hkey[0]))
        print(self.hkey)
        self.adkey = get_random_bytes(16)  # (Enc, Dec), K'
        self.fkey = get_random_bytes(16)  # PRF, K''
        self.a = util.init_sh_poly(self.adkey, server.t)

    def show_server(self):
        print(self.server)

    def add_triple(self, triple):
        self.triples.append(triple)
        print(triple.y)
        print(triple.id)
        print(triple.ad)
        print("triple " + str(triple.id) + " was added for client " + str(self.id))
        self.send_voucher(triple)

    def generate_voucher(self, triple):
        adct = util.aes128_enc(self.adkey, triple.ad)
        # path = clients_dir + "/" + str(self.id) + "/" + str(triple.id) + ".png"
        # self.dec_image(path, adct)
        prf_sh_x, prf_sh_z, prf_x, prf_r = util.calc_prf(self.fkey, triple.id, self.server.s)
        r = util.calc_dhf(self.hkey, prf_x)
        sh_z = util.calc_poly(prf_sh_x, self.a)
        json_k = ['x', 'z']
        json_v = [prf_sh_x, sh_z]
        sh = json.dumps(dict(zip(json_k, json_v)))
        rkey = get_random_bytes(16)
        rct = util.calc_rct(rkey, r, adct, sh)
        print(rct)
        voucher = Voucher(0, 0, 0, 0, 0, 0)
        return voucher

    def send_voucher(self, triple):
        voucher = self.generate_voucher(triple)
        self.server.receive_voucher(self, voucher)

    def dec_image(self, path, adct):
        img_as_byte = util.aes128_dec(self.adkey, adct)
        f = open(path, 'wb')
        f.write(img_as_byte)
        f.close()
