import pickle
import shutil
from shutil import copyfile

import nnhash
import PySimpleGUI as sg
import os

import util
from client import Client
from server import Server

# Parent Directory
parent_dir = "D:/Apple-CSAM-Files/"
clients_dir = parent_dir + "Clients/"
client_id_file = "Client_IDs.csv"


def save_object(obj, path):
    try:
        with open(path, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
            print("saved to %s" % path)
    except Exception as e:
        print("Error during pickling object:", e)


def load_object(f_name):
    try:
        with open(f_name, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print("Error during unpickling object:", e)


class Triple:
    def __init__(self, y, id, ad):
        self.y = y
        self.id = id
        self.ad = ad


if os.path.isfile("server.pickle"):
    server = load_object("server.pickle")
else:
    server = Server("Apple")
    try:
        shutil.rmtree(clients_dir)
        os.mkdir(clients_dir, 0o777)
        print("Deleted contents in folder %s" % clients_dir)
    except Exception as exe:
        print("Failed to delete %s because of %s" % (clients_dir, exe))

for cl in server.client_list:
    print(cl.adkey)
    print(int.from_bytes(cl.adkey, "big"))

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
        sg.In(size=(22, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
        sg.Button("Upload"),
        sg.Button("Process Vouchers")
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
    [sg.Image(key="-IMAGE-", size=(500, 500))],
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
filename = ""

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
        except Exception as ex:
            file_list = []
            print("file_list is empty", ex)
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
            window["-IMAGE-"].update(filename=filename, size=(500, 500))
        except Exception as ex:
            print("could not update filename", ex)
    elif event == "Add Client":
        if values["-ID-"] == "":
            print("need to enter ID")
        else:
            server.add_client(Client(values["-ID-"], server))
        window["-CLIENT LIST-"].update(server.client_id_list)
    elif event == "Delete Client":
        if len((values["-CLIENT LIST-"])) > 0:
            server.delete_client(values["-CLIENT LIST-"][0])
        else:
            print("need to select client")
        window["-CLIENT LIST-"].update(server.client_id_list)
    elif event == "Upload":
        print("------------------------------------------------------------------------------------------------------")
        if len(values["-CLIENT LIST-"]) == 0:
            print("need to select client")
        elif len(values["-FILE LIST-"]) == 0:
            print("need to select file")
        else:
            dst_name = clients_dir + values["-CLIENT LIST-"][0] + "/" + values["-FILE LIST-"][0]
            copyfile(filename, dst_name)
            print("uploaded file from %s to %s" % (filename, dst_name))
            with open(dst_name, "rb") as imageFile:
                byte_arr = bytearray(imageFile.read())
            triple = Triple(nnhash.calc_nnhash(dst_name), server.cur_id, byte_arr)
            server.inc_cur_id()
            index = server.client_id_list.index(values["-CLIENT LIST-"][0])
            server.client_list[index].add_triple(triple)
    elif event == "Process Vouchers":
        server.process_vouchers()

window.close()

save_object(server, "server.pickle")
