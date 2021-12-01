import os
from PIL import Image
from collections import Counter

import nnhash

root_dir = "D:/Apple-CSAM-Files/Image-Database/"
standard_dir = root_dir + "Standard/"
greyscale_dir = root_dir + "Greyscale/"
resolution_dir = root_dir + "Resolution/"
resize_dir = root_dir + "Resize/"
crop_dir = root_dir + "Crop/"
rotation_dir = root_dir + "Rotation/"
flip_dir = root_dir + "Flip/"
logo_dir = root_dir + "Logo/"
png_dir = root_dir + "PNG-Images/"
test_dir = root_dir + "Test/"


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
    result_dir = resolution_dir + "Subsampling=" + str(sub) + "/res" + str(res) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        # print("created folder %s" % result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img.save(result_dir + img_file, quality=res, subsampling=sub)
        # print(img_file)
    compare_images(result_dir)


def generate_and_compare_resize(scale):
    result_dir = resize_dir + "scale" + str(scale) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        # print("created folder %s" % result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        width, height = img.size
        img_resize = img.resize((int(width * scale), int(height * scale)))
        img_resize.save(result_dir + img_file, quality=100, subsampling=-1)
    compare_images(result_dir)


def generate_and_compare_crop(percent):
    result_dir = crop_dir + "percent" + str(percent) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        # print("created folder %s" % result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        width, height = img.size
        width_offset = int(float(width) * (percent / 100))
        height_offset = int(float(height) * (percent / 100))
        borders = (width_offset, height_offset, width - width_offset, height - height_offset)
        img_crop = img.crop(borders)
        img_crop.save(result_dir + img_file, quality=100, subsampling=-1)
    compare_images(result_dir)


def generate_and_compare_rotation(degree, exp):
    result_dir = rotation_dir + "expand=" + str(exp) + "/degree" + str(degree) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        # print("created folder %s" % result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img.rotate = img.rotate(degree, expand=exp)
        img.rotate.save(result_dir + img_file, quality=100, subsampling=-1)
    compare_images(result_dir)


def generate_and_compare_flip():
    if not os.path.exists(flip_dir):
        os.makedirs(flip_dir)
        # print("created folder %s" % flip_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img_flip = img.transpose(Image.FLIP_LEFT_RIGHT)
        img_flip.save(flip_dir + img_file, quality=100, subsampling=-1)
    compare_images(flip_dir)


def generate_and_compare_logo(scale):
    result_dir = logo_dir + "scale" + str(scale) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        # print("created folder %s" % result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        logo = Image.open(root_dir + "apple_logo.png").convert("RGBA")
        img_width, img_height = img.size
        logo_width, logo_height = logo.size
        img_ratio = img_width / img_height
        logo_ratio = logo_width / logo_height
        if img_ratio >= logo_ratio:
            # height is border
            logo_abs_height = img.height * scale
            scale_factor = logo_height / logo_abs_height
        else:
            # width is border
            logo_abs_width = img.width * scale
            scale_factor = logo.width / logo_abs_width
        logo_resize = logo.resize((int(logo_width / scale_factor), int(logo_height / scale_factor)))
        pos = ((img.width - logo_resize.width), img.height - logo_resize.height)
        img.paste(logo_resize, pos, logo_resize)
        img.save(result_dir + img_file, quality=100, subsampling=-1)
    compare_images(result_dir)


def test():
    ctr = 0
    for img_file in os.listdir(standard_dir):
        ctr += 1
        if ctr > 2:
            break
        img = Image.open(standard_dir + img_file)
        logo = Image.open(root_dir + "apple_logo.png").convert("RGBA")
        img_width, img_height = img.size
        logo_width, logo_height = logo.size
        img_ratio = img_width / img_height
        logo_ratio = logo_width / logo_height
        scale = 0.05
        if img_ratio >= logo_ratio:
            # height is border
            logo_abs_height = img.height * scale
            scale_factor = logo_height / logo_abs_height
        else:
            # width is border
            logo_abs_width = img.width * scale
            scale_factor = logo.width / logo_abs_width
        logo_resize = logo.resize((int(logo_width / scale_factor), int(logo_height / scale_factor)))
        pos = ((img.width - logo_resize.width), img.height - logo_resize.height)
        img.paste(logo_resize, pos, logo_resize)
        img.show()


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


if __name__ == '__main__':
    pass
    # conv_to_png()
    # generate_and_compare_greyscale()
    # for i in range(-1, 3):
    #    generate_and_compare_resolution(1, i)
    #    ctr = 5
    #    while ctr <= 100:
    #        generate_and_compare_resolution(ctr, i)
    #        ctr += 5
    # val_resize = 1
    # while val_resize <= 20:
    #    sca = float(val_resize) / 20
    #    generate_and_compare_resize(sca)
    #    val_resize += 1
    # val_crop = 100
    # while val_crop >= 0:
    #    per = float(val_crop) / 10
    #    generate_and_compare_crop(per)
    #    val_crop -= 5
    # for i in range(0, 4):
    #    generate_and_compare_rotation(i * 90, False)
    # for i in range(1, 11):
    #    generate_and_compare_rotation(i, False)
    #    generate_and_compare_rotation(-i, False)
    # for i in range(0, 4):
    #    generate_and_compare_rotation(i * 90, True)
    # for i in range(1, 11):
    #    generate_and_compare_rotation(i, True)
    #    generate_and_compare_rotation(-i, True)
    # generate_and_compare_flip()
    # for i in range(1, 21):
    #    generate_and_compare_logo(i / 20)


