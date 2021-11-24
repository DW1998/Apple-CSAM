import pickle
import shutil

import collide
import nnhash
import PySimpleGUI as sg
import os
from shutil import copyfile

import util
from client import Client
from server import Server


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
        shutil.rmtree(util.clients_dir)
        os.mkdir(util.clients_dir, 0o777)
        print("Deleted contents in folder %s" % util.clients_dir)
    except Exception as exe:
        print("Failed to delete %s because of %s" % (util.clients_dir, exe))
    try:
        shutil.rmtree(util.dec_img_dir)
        os.mkdir(util.dec_img_dir, 0o777)
        print("Deleted contents in folder %s" % util.dec_img_dir)
    except Exception as exe:
        print("Failed to delete %s because of %s" % (util.dec_img_dir, exe))

collide_management_column = [
    [
        sg.Text('Collide Section', size=(27, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)
    ],
    [
        sg.Button("Select as Image"),
        sg.In(size=(56, 1), enable_events=True, key="-COLLIDE IMAGE-"),
    ],
    [
        sg.Button("Select as Target Hash"),
        sg.In(size=(51, 1), enable_events=True, key="-TARGET HASH-"),
    ],
    [
        sg.Text("Select Iterations"),
        sg.Slider(range=(1, 10000), orientation='h', size=(45, 20), default_value=5000, key="-SLIDER ITERATIONS-")
    ],
    [
        sg.Text("Select Blur"),
        sg.InputCombo((0.0, 0.5, 1.0), size=(24, 1), default_value=0.0, key="-BLUR-"),
        sg.Button("Try Collision"),
        sg.Button("Clear Collision Directory")
    ],
    [
        sg.Text('Compare Section', size=(27, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)
    ],
    [
        sg.Button("Select as Hash 1"),
        sg.In(size=(55, 1), enable_events=True, key="-HASH 1-")
    ],
    [
        sg.Button("Select as Hash 2"),
        sg.In(size=(55, 1), enable_events=True, key="-HASH 2-")
    ],
    [
        sg.Button("Compare Hashes"),
        sg.In(size=(55, 1), enable_events=True, key="-HASH XOR-")
    ]
]

client_management_column = [
    [
        sg.Text('Client Management', size=(27, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)
    ],
    [
        sg.Text("Enter ID"),
        sg.InputText(size=(39, 1), do_not_clear=False, key="-ID-"),
        sg.Button("Add Client"),
        sg.Button("Delete Client")
    ],
    [
        sg.Listbox(
            values=server.client_id_list, enable_events=True, size=(70, 42), key="-CLIENT LIST-"
        )
    ]
]

file_list_column = [
    [
        sg.Text('Image Selection', size=(27, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)
    ],
    [
        sg.Text("Image Folder"),
        sg.In(size=(42, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
        sg.Button("Upload")
    ],
    [
        sg.Button("Send Synth Voucher"),
        sg.Button("Process Vouchers"),
        sg.Button("Show Neural Hash")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(70, 40), key="-FILE LIST-"
        )
    ],
]

image_viewer_column = [
    [
        sg.Text('Image Display', size=(27, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)
    ],
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-", size=(515, 700))],
]

# ----- Full layout -----

layout = [
    [
        sg.Column(collide_management_column),
        sg.VSeperator(),
        sg.Column(client_management_column),
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
               and f.lower().endswith((".png", ".gif", ".jpeg", ".jpg"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename, size=(515, 700))
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
            dst_name = util.clients_dir + values["-CLIENT LIST-"][0] + "/" + values["-FILE LIST-"][0]
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
    elif event == "Send Synth Voucher":
        if len(values["-CLIENT LIST-"]) == 0:
            print("need to select client")
        else:
            triple = Triple(None, server.cur_id, None)
            server.inc_cur_id()
            index = server.client_id_list.index(values["-CLIENT LIST-"][0])
            server.client_list[index].add_triple(triple)
    elif event == "Show Neural Hash":
        if len(values["-FILE LIST-"]) == 0:
            print("need to select file")
        else:
            neural_hash = nnhash.calc_nnhash(filename)
            print(neural_hash)
            print(bin(int(neural_hash, 16))[2:].zfill(96))
    elif event == "Select as Image":
        if len(values["-FILE LIST-"]) == 0:
            print("need to select file")
        else:
            window["-COLLIDE IMAGE-"].update(filename)
    elif event == "Select as Target Hash":
        if len(values["-FILE LIST-"]) == 0:
            print("need to select file")
        else:
            window["-TARGET HASH-"].update(nnhash.calc_nnhash(filename))
    elif event == "Try Collision":
        col_img = values["-COLLIDE IMAGE-"]
        targ_hash = values["-TARGET HASH-"]
        num_iter = int(values["-SLIDER ITERATIONS-"])
        blur = values["-BLUR-"]
        if len(col_img) == 0:
            print("need to select a collide image")
        elif len(targ_hash) == 0:
            print("need to select a target hash")
        else:
            print("starting collision on target hash %s with image %s, (iterations: %s, blur: %s)" % (targ_hash, col_img, num_iter, blur))
            collide.collide(col_img, targ_hash, num_iter, blur)
    elif event == "Clear Collision Directory":
        try:
            shutil.rmtree(util.collide_dir)
            os.mkdir(util.collide_dir, 0o777)
            print("Deleted contents in folder %s" % util.collide_dir)
        except Exception as ex:
            print("Failed to delete %s because of %s" % (util.collide_dir, ex))
    elif event == "Select as Hash 1":
        if len(values["-FILE LIST-"]) == 0:
            print("need to select file")
        else:
            window["-HASH 1-"].update(nnhash.calc_nnhash(filename))
    elif event == "Select as Hash 2":
        if len(values["-FILE LIST-"]) == 0:
            print("need to select file")
        else:
            window["-HASH 2-"].update(nnhash.calc_nnhash(filename))
    elif event == "Compare Hashes":
        if len(values["-HASH 1-"]) == 0 or len(values["-HASH 2-"]) == 0:
            print("Please select 2 Hashes to compare")
        else:
            hash1 = bin(int(values["-HASH 1-"], 16))[2:].zfill(96)
            hash2 = bin(int(values["-HASH 2-"], 16))[2:].zfill(96)
            xor = int(hash1, 2) ^ int(hash2, 2)
            out_hex = hex(xor)[2:].zfill(24)
            window["-HASH XOR-"].update(out_hex)

window.close()

save_object(server, "server.pickle")
