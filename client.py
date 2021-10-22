
class Client:
    def __init__(self, id, server):
        self.id = id
        self.server = server
        self.pictures = list()
        self.register(server)

    def register(self, server):
        server.add_client(self)

    def show_server(self):
        print(self.server)

    def send_voucher(self, voucher):
        self.server.receive_voucher(self, voucher)