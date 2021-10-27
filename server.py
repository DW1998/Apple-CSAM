import csv
import os
import shutil

from client import Client

# Parent Directory
parent_dir = "D:/Apple-CSAM-Files/"
clients_dir = parent_dir + "Clients/"


class Server:
    def __init__(self, name, client_ids):
        self.name = name
        self.client_list = list()
        self.client_id_list = list()
        self.add_clients(client_ids)
        self.cur_id = 0

    def add_clients(self, client_ids):
        for c_id in client_ids:
            Client(c_id, self)

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

    def receive_voucher(self, client, voucher):
        print(self.name + "received voucher " + voucher + " from " + str(client.id))
