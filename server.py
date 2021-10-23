
class Server:
    def __init__(self, name):
        self.name = name
        self.client_list = list()
        self.client_id_list = list()

    def add_client(self, client):
        self.client_list.append(client)
        self.client_id_list.append(client.id)

    def show_clients(self):
        for c in self.client_list: print(c.id)

    def receive_voucher(self, client, voucher):
        print("received voucher " + voucher + " from " + str(client.id))
