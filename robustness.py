import os
from PIL import Image
from collections import Counter

import nnhash

root_dir = "D:/Apple-CSAM-Files/Image-Database/"
standard_dir = root_dir + "Standard/"
greyscale_dir = root_dir + "Greyscale/"
resolution_dir = root_dir + "Resolution/"
png_dir = root_dir + "PNG-Images/"

# Results:
# D:/Apple-CSAM-Files/Image-Database/Greyscale/ Counter({0: 43, 1: 29, 2: 18, 3: 6, 4: 3, 5: 1}), 43
# D:/Apple-CSAM-Files/Image-Database/Resolution/res1/ Counter({5: 14, 4: 12, 3: 11, 6: 10, 7: 10, 9: 9, 2: 8, 8: 7, 10: 5, 11: 2, 13: 2, 18: 2, 1: 1, 16: 1, 23: 1, 32: 1, 12: 1, 0: 1, 15: 1, 14: 1}), 1
# D:/Apple-CSAM-Files/Image-Database/Resolution/res5/ Counter({3: 23, 4: 13, 2: 13, 1: 11, 6: 11, 5: 11, 0: 8, 9: 3, 7: 3, 8: 2, 10: 1, 11: 1}), 8
# D:/Apple-CSAM-Files/Image-Database/Resolution/res10/ Counter({0: 39, 1: 32, 2: 13, 3: 8, 5: 4, 4: 3, 6: 1}), 39
# D:/Apple-CSAM-Files/Image-Database/Resolution/res15/ Counter({0: 47, 1: 31, 2: 14, 3: 5, 4: 2, 5: 1}), 47
# D:/Apple-CSAM-Files/Image-Database/Resolution/res20/ Counter({0: 55, 1: 32, 2: 12, 3: 1}), 55
# D:/Apple-CSAM-Files/Image-Database/Resolution/res25/ Counter({0: 63, 1: 27, 2: 7, 3: 3}), 63
# D:/Apple-CSAM-Files/Image-Database/Resolution/res30/ Counter({0: 73, 1: 18, 2: 9}), 73
# D:/Apple-CSAM-Files/Image-Database/Resolution/res35/ Counter({0: 69, 1: 28, 2: 3}), 69
# D:/Apple-CSAM-Files/Image-Database/Resolution/res40/ Counter({0: 74, 1: 24, 2: 2}), 74
# D:/Apple-CSAM-Files/Image-Database/Resolution/res45/ Counter({0: 76, 1: 21, 2: 2, 3: 1}), 76
# D:/Apple-CSAM-Files/Image-Database/Resolution/res50/ Counter({0: 77, 1: 19, 2: 4}), 77
# D:/Apple-CSAM-Files/Image-Database/Resolution/res55/ Counter({0: 80, 1: 19, 2: 1}), 80
# D:/Apple-CSAM-Files/Image-Database/Resolution/res60/ Counter({0: 82, 1: 16, 2: 2}), 82
# D:/Apple-CSAM-Files/Image-Database/Resolution/res65/ Counter({0: 87, 1: 12, 2: 1}), 87
# D:/Apple-CSAM-Files/Image-Database/Resolution/res70/ Counter({0: 82, 1: 17, 2: 1}), 82
# D:/Apple-CSAM-Files/Image-Database/Resolution/res75/ Counter({0: 91, 1: 9}), 91
# D:/Apple-CSAM-Files/Image-Database/Resolution/res80/ Counter({0: 93, 1: 7}), 93
# D:/Apple-CSAM-Files/Image-Database/Resolution/res85/ Counter({0: 97, 1: 3}), 97
# D:/Apple-CSAM-Files/Image-Database/Resolution/res90/ Counter({0: 98, 1: 2}), 98
# D:/Apple-CSAM-Files/Image-Database/Resolution/res95/ Counter({0: 97, 1: 3}), 97
# D:/Apple-CSAM-Files/Image-Database/Resolution/res100/ Counter({0: 98, 1: 2}), 98


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


def generate_greyscale():
    if not os.path.exists(greyscale_dir):
        os.makedirs(greyscale_dir)
        print("created folder %s" % greyscale_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img_greyscale = img.convert('L')
        img_greyscale.save(greyscale_dir + img_file)
        print(img_file)


def generate_and_compare_resolution(res):
    res_dir = resolution_dir + "res" + str(res) + "/"
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
        print("created folder %s" % res_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img.save(res_dir + img_file, quality=res, subsampling=0)
        print(img_file)
    compare_images(res_dir)


def compare_images(compare_folder):
    if not os.path.exists(compare_folder):
        print("compare folder doesnt exist")
    else:
        dist_lst = list()
        for img_file in os.listdir(standard_dir):
            print("comparing %s" % img_file)
            nnhash_standard = nnhash.calc_nnhash(standard_dir + img_file)
            nnhash_other = nnhash.calc_nnhash(compare_folder + img_file)
            nnhash_standard_bin = bin(int(nnhash_standard, 16))[2:].zfill(96)
            nnhash_other_bin = bin(int(nnhash_other, 16))[2:].zfill(96)
            xor = int(nnhash_standard_bin, 2) ^ int(nnhash_other_bin, 2)
            xor_str = str(bin(xor).zfill(96))
            dist = xor_str.count('1')
            dist_lst.append(dist)
        print(compare_folder, Counter(dist_lst))


if __name__ == '__main__':
    pass
