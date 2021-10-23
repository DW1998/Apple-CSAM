class Server:
    def __init__(self, name):
        self.name = name
        self.client_list = list()
        self.client_id_list = list()

    def add_client(self, client):
        if client.id not in self.client_id_list:
            self.client_list.append(client)
            self.client_id_list.append(client.id)
            print("client " + str(client.id) + " was added")
        else:
            print("ID was already found")

    def show_clients(self):
        for c in self.client_list: print(c.id)

    def receive_voucher(self, client, voucher):
        print(self.name + "received voucher " + voucher + " from " + str(client.id))
