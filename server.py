from client import Client


class Server:
    def __init__(self, name, client_ids):
        self.name = name
        self.client_list = list()
        self.client_id_list = list()
        self.add_clients(client_ids)

    def add_clients(self, client_ids):
        for c_id in client_ids:
            client = Client(c_id, self)

    def add_client(self, client):
        if client.id not in self.client_id_list:
            self.client_list.append(client)
            self.client_id_list.append(client.id)
            print("client " + str(client.id) + " was added")
        else:
            print("ID " + str(client.id) + " was already found")

    def delete_client(self, client_id):
        if client_id in self.client_id_list:
            index = self.client_id_list.index(client_id)
            self.client_list.pop(index)
            self.client_id_list.pop(index)
        else:
            print("ID " + str(client_id) + " was not found")

    def show_clients(self):
        for c in self.client_list: print(c)

    def receive_voucher(self, client, voucher):
        print(self.name + "received voucher " + voucher + " from " + str(client.id))
