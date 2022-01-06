import json
import random
import util

from Crypto.Random import get_random_bytes
from Crypto.PublicKey import ECC


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
        self.adkey = int.to_bytes(random.randint(0, util.sh_p), 16, "big")  # (Enc, Dec), K'
        self.fkey = get_random_bytes(16)  # PRF, K''
        self.a = util.init_sh_poly(self.adkey, server.t)
        self.pdata = self.validate_pdata()
        self.num_synth = 0

    def show_server(self):
        print(self.server)

    def add_triple(self, triple):
        self.triples.append(triple)
        print(f"triple {triple.id} was added for client {self.id}")
        self.send_voucher(triple)

    def validate_pdata(self):
        return self.server.pdata

    def generate_voucher(self, triple):
        adct = util.aes128_enc(self.adkey, triple.ad)
        prf_sh_x, prf_sh_z, prf_x, prf_r = util.calc_prf(self.fkey, triple.id, self.server.s)
        r = util.calc_dhf(self.hkey, prf_x)
        sh_z = util.calc_poly(prf_sh_x, self.a)
        json_k = ['x', 'z']
        json_v = [prf_sh_x, sh_z]
        sh = json.dumps(dict(zip(json_k, json_v)))
        rkey = get_random_bytes(16)
        rct = util.calc_rct(rkey, r, adct, sh)
        w1, w2 = util.calc_h(triple.y, self.server.n_dash, self.server.h1_index, self.server.h2_index)
        L = ECC.EccPoint(x=self.pdata[0][0], y=self.pdata[0][1], curve='p256')
        beta1 = random.randint(0, util.ecc_q)
        gamma1 = random.randint(0, util.ecc_q)
        Q1 = beta1 * util.calc_H(triple.y) + gamma1 * util.ecc_gen
        Q1_tuple = (int(Q1.x), int(Q1.y))
        P_w1 = ECC.EccPoint(x=self.pdata[w1 + 1][0], y=self.pdata[w1 + 1][1], curve='p256')
        S1 = beta1 * P_w1 + gamma1 * L
        H_dash_S1 = util.calc_H_dash(S1)
        ct1 = util.calc_ct(H_dash_S1, rkey)
        beta2 = random.randint(0, util.ecc_q)
        gamma2 = random.randint(0, util.ecc_q)
        Q2 = beta2 * util.calc_H(triple.y) + gamma2 * util.ecc_gen
        Q2_tuple = (int(Q2.x), int(Q2.y))
        P_w2 = ECC.EccPoint(x=self.pdata[w2 + 1][0], y=self.pdata[w2 + 1][1], curve='p256')
        S2 = beta2 * P_w2 + gamma2 * L
        H_dash_S2 = util.calc_H_dash(S2)
        ct2 = util.calc_ct(H_dash_S2, rkey)
        if random.randint(1, 2) == 1:
            voucher = Voucher(triple.id, Q1_tuple, ct1, Q2_tuple, ct2, rct)
        else:
            voucher = Voucher(triple.id, Q2_tuple, ct2, Q1_tuple, ct1, rct)
        return voucher

    def send_voucher(self, triple):
        voucher = self.generate_voucher(triple)
        self.server.receive_voucher(self, voucher)
