import math
import os
import random
import shutil

import util
from client import Client
import nnhash

# Parent Directory
parent_dir = "D:/Apple-CSAM-Files/"
clients_dir = parent_dir + "Clients/"
mal_img_dir = parent_dir + "Malicious Images/"


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

    def receive_voucher(self, client, voucher):
        print("%s received voucher with ID %s from %s" % (self.name, voucher.id, client.id))
