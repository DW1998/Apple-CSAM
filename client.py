class Client:
    def __init__(self, id, server):
        self.id = id
        self.server = server
        self.triples = list()
        self.hkey = 0  # DHF, K
        self.adkey = 0  # (Enc, Dec), K'
        self.fkey = 0  # PRF, K''
        self.sh_pol = 0  # shamir secret sharing

    def show_server(self):
        print(self.server)

    def add_triple(self, t):
        self.triples.append(t)
        print("triple" + str(t.id) + " was added for client " + str(self.id))

    def send_voucher(self, voucher):
        self.server.receive_voucher(self, voucher)
