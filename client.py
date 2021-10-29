from Crypto.Random import get_random_bytes

import util

# Parent Directory
parent_dir = "D:/Apple-CSAM-Files/"
clients_dir = parent_dir + "Clients/"


class Voucher:
    def __init__(self, id, Q1, ct1, Q2, ct2, rct):
        self.id = id
        self.Q1 = Q1
        self.ct1 = ct1
        self.Q2 = Q2
        self.ct2 = ct2
        self.rct = rct





class Client:
    def __init__(self, id, server):
        self.id = id
        self.server = server
        self.triples = list()
        self.hkey = 0  # DHF, K
        self.adkey = get_random_bytes(16)  # (Enc, Dec), K'
        self.fkey = 0  # PRF, K''
        self.sh_pol = 0  # shamir secret sharing

    def show_server(self):
        print(self.server)

    def add_triple(self, triple):
        self.triples.append(triple)
        print(triple.y)
        print(triple.id)
        print(triple.ad)
        print("triple" + str(triple.id) + " was added for client " + str(self.id))
        self.send_voucher(triple)

    def generate_voucher(self, triple):
        adct = util.aes128_enc(self.adkey, triple.ad)
        # path = clients_dir + "/" + str(self.id) + "/" + str(triple.id) + ".png"
        # self.dec_image(path, adct)
        voucher = Voucher(0, 0, 0, 0, 0, 0)
        return voucher

    def send_voucher(self, triple):
        voucher = self.generate_voucher(triple)
        self.server.receive_voucher(self, voucher)

    def dec_image(self, path, adct):
        img_as_byte = util.aes128_dec(self.adkey, adct)
        f = open(path, 'wb')
        f.write(img_as_byte)
        f.close()
