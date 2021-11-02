import math
import os
import random
import shutil

import util
from client import Client
import nnhash
from Crypto.PublicKey import ECC

# Parent Directory
parent_dir = "D:/Apple-CSAM-Files/"
clients_dir = parent_dir + "Clients/"
mal_img_dir = parent_dir + "Malicious Images/"
ecc_p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
ecc_q = 115792089210356248762697446949407573529996955224135760342422259061068512044369
ecc_gen_x = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
ecc_gen_y = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
ecc_gen = ECC.EccPoint(x=int(ecc_gen_x), y=int(ecc_gen_y), curve='p256')


def process_X():
    x = list()
    for img in os.listdir(mal_img_dir):
        if img.endswith(".jpg") or img.endswith(".png"):
            nh = nnhash.calc_nnhash(mal_img_dir + img)
            x.append(nh)
    x = list(dict.fromkeys(x))
    return x


class Server:
    def __init__(self, name):
        self.name = name
        self.client_list = list()
        self.client_id_list = list()
        self.cur_id = 0
        self.s = 10
        self.t = 5
        self.x = process_X()
        self.h1_index = 0
        self.h2_index = 1
        self.e_dash = 0.3
        self.n_dash = int((1 + self.e_dash) * len(self.x))
        self.check_rehash(0)
        self.cuckoo = list()
        self.create_cuckoo_table()
        self.alpha = random.randint(0, ecc_q)
        print("alpha: %s" % self.alpha)
        self.L = (self.alpha * ecc_gen).xy
        print("L.x: %s" % self.L[0])
        print("L.y: %s" % self.L[1])
        print("-p-: %s" % ecc_p)
        self.pdata = self.calc_pdata()
        print(self.pdata)

    def add_clients(self, client_ids):
        for c_id in client_ids:
            self.add_client(Client(c_id, self))

    def add_client(self, client):
        if client.id not in self.client_id_list:
            self.client_list.append(client)
            self.client_id_list.append(client.id)
            print("client " + str(client.id) + " was added")
            path = os.path.join(clients_dir, client.id)
            try:
                os.mkdir(path, 0o777)
                print("added dir: " + path)
            except OSError:
                pass
        else:
            print("ID " + str(client.id) + " was already found")

    def delete_client(self, client_id):
        if client_id in self.client_id_list:
            index = self.client_id_list.index(client_id)
            self.client_list.pop(index)
            self.client_id_list.pop(index)
            print("client " + str(client_id) + " was deleted")
            path = os.path.join(clients_dir, client_id)
            try:
                shutil.rmtree(path)
                print("deleted dir: " + path)
            except OSError:
                pass
        else:
            print("ID " + str(client_id) + " was not found")

    def show_clients(self):
        print(self.client_id_list)

    def inc_cur_id(self):
        self.cur_id += 1

    def check_rehash(self, cnt):
        if cnt == math.factorial(len(util.hash_list)):
            print("Could not find usable hash functions in %s tries" % cnt)
            return
        for i in self.x:
            h1_x, h2_x = util.calc_h(i, self.n_dash, self.h1_index, self.h2_index)
            if h1_x == h2_x:
                self.h1_index = random.randint(0, 6)
                self.h2_index = random.randint(0, 6)
                while self.h1_index == self.h2_index:
                    self.h2_index = random.randint(0, 6)
                self.check_rehash(cnt + 1)

    def create_cuckoo_table(self):
        self.cuckoo = dict.fromkeys((range(self.n_dash)))
        for i in self.x:
            h1, h2 = util.calc_h(i, self.n_dash, self.h1_index, self.h2_index)
            self.cuckoo_insert(i, 0, 0)
        print(self.cuckoo)

    def cuckoo_insert(self, x, n, cnt):
        h1_x, h2_x = util.calc_h(x, self.n_dash, self.h1_index, self.h2_index)
        hashes = list()
        hashes.append(h1_x)
        hashes.append(h2_x)
        if self.cuckoo[h1_x] == x or self.cuckoo[h2_x] == x:
            return
        if cnt == self.n_dash:
            print("Cycle detected, %s discarded" % x)
            return
        if self.cuckoo[hashes[n]] is None:
            self.cuckoo[hashes[n]] = x
            return
        else:
            old_x = self.cuckoo[hashes[n]]
            h1_old_x, h2_old_x = util.calc_h(old_x, self.n_dash, self.h1_index, self.h2_index)
            self.cuckoo[hashes[n]] = x
            new_n = 0
            if n == 0:
                if h1_old_x == h1_x:
                    new_n = 1
            else:
                if h1_old_x == h2_x:
                    new_n = 1
            self.cuckoo_insert(old_x, new_n, cnt + 1)

    def calc_pdata(self):
        pdata = list()
        L_list = list()
        L_list.append(int(self.L[0]))
        L_list.append(int(self.L[1]))
        pdata.append(L_list)
        for i in self.cuckoo:
            print(self.cuckoo[i])
            if self.cuckoo[i] is None:
                ran = random.randint(0, ecc_q)
                P = ran * ecc_gen
            else:
                P = self.alpha * util.H(i)
            P_list = list()
            P_list.append(int(P.x))
            P_list.append(int(P.y))
            print(P_list)
            pdata.append(P_list)
        return pdata

    def receive_voucher(self, client, voucher):
        print("%s received voucher with ID %s from %s" % (self.name, voucher.id, client.id))
