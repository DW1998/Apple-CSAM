from PIL import Image

import nnhash
import PySimpleGUI as sg
import os.path

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


file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen

image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout)

# Run the Event Loop

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)

        except:
            pass

window.close()

if __name__ == '__main__':
    server = Server("Apple")
    c1 = Client(1, server)
    c2 = Client(2, server)

    hash_val = nnhash.run("dog.png")
    triple1 = Triple(nnhash.run("dog.png"), get_id(), Image.open("dog.png"))
    triple2 = Triple(nnhash.run("dog.png"), get_id(), Image.open("dog.png"))
    print(hash_val)
