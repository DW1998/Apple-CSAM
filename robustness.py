import os
from PIL import Image
from collections import Counter

import nnhash

root_dir = "D:/Apple-CSAM-Files/Image-Database/"
standard_dir = root_dir + "Standard/"
greyscale_dir = root_dir + "Greyscale/"
resolution_dir = root_dir + "Resolution/"
resize_dir = root_dir + "Resize/"
png_dir = root_dir + "PNG-Images/"


def conv_to_png():
    if not os.path.exists(png_dir):
        os.makedirs(png_dir)
        print("created folder %s" % png_dir)
    for img_file in os.listdir(standard_dir):
        if img_file.endswith(".jpg"):
            img = Image.open(standard_dir + img_file)
            img.save(png_dir + img_file.split(".")[0] + ".png")
        if img_file.endswith(".webp"):
            img = Image.open(standard_dir + img_file).convert('RGB')
            img.save(png_dir + img_file.split(".")[0] + ".png")


def generate_and_compare_greyscale():
    if not os.path.exists(greyscale_dir):
        os.makedirs(greyscale_dir)
        print("created folder %s" % greyscale_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img_greyscale = img.convert('L')
        img_greyscale.save(greyscale_dir + img_file)
        print(img_file)
    compare_images(greyscale_dir)


def generate_and_compare_resolution(res, sub):
    res_dir = resolution_dir + "Subsampling=" + str(sub) + "/res" + str(res) + "/"
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
        # print("created folder %s" % res_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img.save(res_dir + img_file, quality=res, subsampling=sub)
        # print(img_file)
    compare_images(res_dir)


def compare_images(compare_folder):
    if not os.path.exists(compare_folder):
        print("compare folder doesnt exist")
    else:
        dist_lst = list()
        for img_file in os.listdir(standard_dir):
            # print("comparing %s" % img_file)
            nnhash_standard = nnhash.calc_nnhash(standard_dir + img_file)
            nnhash_other = nnhash.calc_nnhash(compare_folder + img_file)
            nnhash_standard_bin = bin(int(nnhash_standard, 16))[2:].zfill(96)
            nnhash_other_bin = bin(int(nnhash_other, 16))[2:].zfill(96)
            xor = int(nnhash_standard_bin, 2) ^ int(nnhash_other_bin, 2)
            xor_str = str(bin(xor).zfill(96))
            dist = xor_str.count('1')
            dist_lst.append(dist)
        print(compare_folder, Counter(dist_lst), ",", Counter(dist_lst).get(0))


def generate_and_compare_resize(scale):
    res_dir = resize_dir + "scale" + str(scale) + "/"
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
        # print("created folder %s" % res_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        width, height = img.size
        img_resize = img.resize((int(width * scale), int(height * scale)))
        img_resize.save(res_dir + img_file, quality=100, subsampling=-1)
    compare_images(res_dir)


if __name__ == '__main__':
    # conv_to_png()
    # generate_and_compare_greyscale()
    # for i in range(-1, 3):
    #    generate_and_compare_resolution(1, i)
    #    ctr = 5
    #    while ctr <= 100:
    #        generate_and_compare_resolution(ctr, i)
    #        ctr += 5
    # val = 1
    # while val <= 20:
    #    sca = float(val) / 20
    #    generate_and_compare_resize(sca)
    #    val += 1
    pass
