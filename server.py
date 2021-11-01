import os
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
            print(img)
            nh = nnhash.calc_nnhash(mal_img_dir + img)
            print(nh)
            x.append(nh)
    print(x)
    x = list(dict.fromkeys(x))
    print(x)
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
        self.e_dash = 0.3
        self.cuckoo = self.create_cuckoo_table()
        for i in self.x:
            self.cuckoo_insert(i, 0, 0)
        print(self.cuckoo)

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

    def create_cuckoo_table(self):
        n_dash = int((1 + self.e_dash) * len(self.x))
        print(n_dash)
        cuckoo = dict.fromkeys((range(n_dash)))
        print(cuckoo)
        return cuckoo

    def cuckoo_insert(self, x, n, cnt):
        n_dash = len(self.cuckoo)
        h1 = util.calc_h(x, n_dash, 1)
        h2 = util.calc_h(x, n_dash, 2)
        hashes = list()
        hashes.append(h1)
        hashes.append(h2)
        if self.cuckoo[h1] == x or self.cuckoo[h2] == x:
            return
        if cnt == n_dash:
            print("Cycle detected, %s discarded" % x)
            return
        if self.cuckoo[hashes[n]] is None:
            self.cuckoo[hashes[n]] = x
            return
        else:
            old_x = self.cuckoo[hashes[n]]
            self.cuckoo[hashes[n]] = x
            self.cuckoo_insert(old_x, 1, cnt + 1)

    def receive_voucher(self, client, voucher):
        print("%s received voucher with ID %s from %s" % (self.name, voucher.id, client.id))
