from PIL import Image

import nnhash

from client import Client
from server import Server

cur_id = 0

class Triple:
    def __init__(self, y, id, ad):
        self.y = y
        self.id = id
        self.ad = ad

def get_id():
    global cur_id
    cur_id = cur_id + 1
    return cur_id

if __name__ == '__main__':
    server = Server("Apple")
    c1 = Client(1, server)
    c2 = Client(2, server)

    #server.show_clients()
    #c1.send_voucher(str(500))

    hash_val = nnhash.run("dog.png")
    triple1 = Triple(nnhash.run("dog.png"), get_id(), Image.open("dog.png"))
    triple2 = Triple(nnhash.run("dog.png"), get_id(), Image.open("dog.png"))
    print(triple1.id)
    print(triple2.id)
    print(hash_val)