from PIL import Image

import nnhash
import PySimpleGUI as sg
import os.path
import csv

from client import Client
from server import Server


class Triple:
    def __init__(self, y, id, ad):
        self.y = y
        self.id = id
        self.ad = ad


def get_id():
    global cur_id
    cur_id += 1
    return cur_id


def get_input():
    client_id = int(input("Enter next client id"))
    pic = input("Enter next picture")
    triple3 = Triple(nnhash.run(pic), get_id(), Image.open(pic))
    index = server.client_list.index(client_id)
    server.client_list[index].add_triple(triple3)


def read_client_ids():
    client_ids = list()
    f = open('D:\Apple-CSAM-Files\Client_IDs.csv', 'r')
    reader = csv.reader(f)
    for row in reader:
        client_ids.append(row[0])
    return client_ids


def save_client_ids():
    f = open('D:\Apple-CSAM-Files\Client_IDs.csv', 'w', encoding='UTF8', newline='')
    writer = csv.writer(f)
    for c in server.client_list:
        l = [c.id]
        writer.writerow(l)
    f.close()
    print("wrote data")


cur_id = 0
server = Server("Apple", read_client_ids())
test = list()
for ID in server.client_id_list:
    test.append(ID)

file_client_column = [
    [
        sg.Text("Enter ID"),
        sg.InputText(size=(19, 1), do_not_clear=False, key="-ID-"),
        sg.Button("Add Client"),
        sg.Button("Delete Client")
    ],
    [
        sg.Listbox(
            values=server.client_id_list, enable_events=True, size=(50, 30), key="-CLIENT LIST-"
        )
    ]
]

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(31, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(50, 30), key="-FILE LIST-"
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
        sg.Column(file_client_column),
        sg.VSeperator(),
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Apple CSAM", layout)

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
    elif event == "Add Client":
        if values["-ID-"] == "":
            print("need to enter ID")
        else:
            Client(values["-ID-"], server)

        window["-CLIENT LIST-"].update(server.client_id_list)
    elif event == "Delete Client":
        if len((values["-CLIENT LIST-"])) > 0:
            server.delete_client(values["-CLIENT LIST-"][0])
        else:
            print("need to select client")
        window["-CLIENT LIST-"].update(server.client_id_list)

window.close()

save_client_ids()
