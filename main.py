import nnhash

from client import Client
from server import Server


class Triple:
    def __init__(self, y, id, ad):
        self.y = y
        self.id = id
        self.ad = ad


if __name__ == '__main__':
    server = Server("Apple")
    c1 = Client(1, server)
    c2 = Client(2, server)

    #server.show_clients()
    #c1.send_voucher(str(500))

    hash_val = nnhash.run("dog.png")
    print(hash_val)