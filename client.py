
class Client:
    def __init__(self, id, server):
        self.id = id
        self.server = server
        self.triples = list()
        self.register(server)

    def register(self, server):
        server.add_client(self)

    def show_server(self):
        print(self.server)

    def add_triple(self, t):
        self.triples.append(t)
        print("triple" + str(t.id) + " was added for client " + str(self.id))

    def send_voucher(self, voucher):
        self.server.receive_voucher(self, voucher)
