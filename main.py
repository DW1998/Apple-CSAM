from PIL import Image

import nnhash
import PySimpleGUI as sg

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

def get_input():
    client_id = int(input("Enter next client id"))
    pic = input("Enter next picture")
    triple3 = Triple(nnhash.run(pic), get_id(), Image.open(pic))
    index = server.client_id_list.index(client_id)
    server.client_list[index].add_triple(triple3)


layout = [[sg.Text("GUI test")], [sg.Button("OK")]]

window = sg.Window("Demo", layout)

while True:
    event, values = window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()

if __name__ == '__main__':
    server = Server("Apple")
    c1 = Client(1, server)
    c2 = Client(2, server)

    while True:
        get_input()
        stop = input("end input? Y or N")
        if (stop == "Y"):
            break

    hash_val = nnhash.run("dog.png")
    triple1 = Triple(nnhash.run("dog.png"), get_id(), Image.open("dog.png"))
    triple2 = Triple(nnhash.run("dog.png"), get_id(), Image.open("dog.png"))
    print(hash_val)
