import os

from PIL import Image, ImageEnhance
from collections import Counter

import nnhash

root_dir = "D:/Apple-CSAM-Files/Image-Database/"
standard_dir = root_dir + "Standard/"
resolution_dir = root_dir + "Resolution/"
resize_dir = root_dir + "Resize/"
resize360x360dir = root_dir + "Resize360x360/"
crop_dir = root_dir + "Crop/"
crop_test_dir = root_dir + "Crop-Test/"
rotation_dir = root_dir + "Rotation/"
flip_dir = root_dir + "Flip/"
logo_dir = root_dir + "Logo/"
enhancement_dir = root_dir + "Enhancement/"
png_dir = root_dir + "PNG-Images/"


def conv_to_png():
    if not os.path.exists(png_dir):
        os.makedirs(png_dir)
    for img_file in os.listdir(standard_dir):
        if img_file.endswith(".jpg"):
            img = Image.open(standard_dir + img_file)
            img.save(png_dir + img_file.split(".")[0] + ".png")
        if img_file.endswith(".webp"):
            img = Image.open(standard_dir + img_file).convert('RGB')
            img.save(png_dir + img_file.split(".")[0] + ".png")


def generate_and_compare_resolution(res, sub):
    result_dir = f"{resolution_dir}Subsampling={sub}/res{res}/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img.save(result_dir + img_file, quality=res, subsampling=sub)
    compare_images_jpg(result_dir)


def generate_and_compare_resize(scale):
    result_dir = resize_dir + "scale" + str(scale) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        width, height = img.size
        img_resize = img.resize((int(width * scale), int(height * scale))).convert('RGB')
        img_resize.save(result_dir + img_file.split(".")[0] + ".png")
    compare_images_png(result_dir)


def generate_and_compare_resize_360x360():
    if not os.path.exists(resize360x360dir):
        os.makedirs(resize360x360dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        width, height = img.size
        width_scale = width / 360
        height_scale = height / 360
        img_resize = img.resize((int(width / width_scale), int(height / height_scale))).convert('RGB')
        img_resize.save(resize360x360dir + img_file.split(".")[0] + ".png")
    compare_images_png(resize360x360dir)


def generate_and_compare_crop(percent):
    result_dir = crop_dir + "percent" + str(percent) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        width, height = img.size
        width_offset = int(float(width) * (percent / 100))
        height_offset = int(float(height) * (percent / 100))
        borders = (width_offset, height_offset, width - width_offset, height - height_offset)
        img_crop = img.crop(borders).convert('RGB')
        img_crop.save(result_dir + img_file.split(".")[0] + ".png")
    compare_images_png(result_dir)


def generate_and_compare_rotation(degree, exp):
    result_dir = rotation_dir + "expand=" + str(exp) + "/degree" + str(degree) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img.rotate = img.rotate(degree, expand=exp).convert('RGB')
        img.rotate.save(result_dir + img_file.split(".")[0] + ".png")
    compare_images_png(result_dir)


def generate_and_compare_flip():
    if not os.path.exists(flip_dir):
        os.makedirs(flip_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img_flip = img.transpose(Image.FLIP_LEFT_RIGHT).convert('RGB')
        img_flip.save(flip_dir + img_file.split(".")[0] + ".png")
    compare_images_png(flip_dir)


def generate_and_compare_logo(scale):
    result_dir = logo_dir + "scale" + str(scale) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
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
        img.convert('RGB').save(result_dir + img_file.split(".")[0] + ".png")
    compare_images_png(result_dir)


def generate_and_compare_enhancement(enhancement_val, factor):
    # contrast = 1
    # color = 2
    # brightness = 3
    # sharpness = 4
    if enhancement_val == 1:
        enh = "Contrast/"
    elif enhancement_val == 2:
        enh = "Color/"
    elif enhancement_val == 3:
        enh = "Brightness/"
    else:
        enh = "Sharpness/"
    result_dir = enhancement_dir + enh + str(factor) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        if enhancement_val == 1:
            enhancement = ImageEnhance.Contrast(img)
        elif enhancement_val == 2:
            enhancement = ImageEnhance.Color(img)
        elif enhancement_val == 3:
            enhancement = ImageEnhance.Brightness(img)
        else:
            enhancement = ImageEnhance.Sharpness(img)
        enhancement.enhance(factor).convert('RGB').save(result_dir + img_file.split(".")[0] + ".png")
    compare_images_png(result_dir)


def compare_images_jpg(compare_folder):
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


def compare_images_png(compare_folder):
    if not os.path.exists(compare_folder):
        print("compare folder doesnt exist")
    else:
        dist_lst = list()
        for img_file in os.listdir(standard_dir):
            # print("comparing %s" % img_file)
            nnhash_standard = nnhash.calc_nnhash(standard_dir + img_file)
            nnhash_other = nnhash.calc_nnhash(compare_folder + img_file.split(".")[0] + ".png")
            nnhash_standard_bin = bin(int(nnhash_standard, 16))[2:].zfill(96)
            nnhash_other_bin = bin(int(nnhash_other, 16))[2:].zfill(96)
            xor = int(nnhash_standard_bin, 2) ^ int(nnhash_other_bin, 2)
            xor_str = str(bin(xor).zfill(96))
            dist = xor_str.count('1')
            dist_lst.append(dist)
        print(compare_folder, Counter(dist_lst), ",", Counter(dist_lst).get(0))


def calc_avg_offset():
    with open("C:/Git Repos/Apple-CSAM/results.txt") as f:
        lines = f.readlines()
    out_lines = []
    offsets = []
    for line in lines:
        start_ind = line.find("{") + 1
        end_ind = line.find("}")
        ctr_values = line[start_ind:end_ind]
        ctr_arr = ctr_values.split(",")
        offset = 0
        for s in ctr_arr:
            x = int(s.split(":")[0])
            y = int(s.split(":")[1][1:])
            offset += x * y
        offset = offset / 100
        out_lines.append(f"{line[:-1]}, {offset}")
        offsets.append(f"{offset}, ")
    with open("C:/Git Repos/Apple-CSAM/results_error.txt", 'w') as f:
        for line in out_lines:
            f.write(line)
            f.write('\n')
    with open("C:/Git Repos/Apple-CSAM/error.txt", 'w') as f:
        for o in offsets:
            f.write(o)
    with open("C:/Git Repos/Apple-CSAM/unchanged.txt", 'w') as f:
        for line in out_lines:
            f.write(f"{line.split(',')[-2]},")
    print("printed offset to txt file")


if __name__ == '__main__':
    calc_avg_offset()
    conv_to_png()
    for i in range(-1, 3):
        ctr = 0
        while ctr <= 100:
            generate_and_compare_resolution(ctr, i)
            ctr += 5
    val_resize = 1
    while val_resize <= 20:
        sca = float(val_resize) / 20
        generate_and_compare_resize(sca)
        val_resize += 1
    val_crop = 100
    while val_crop >= 0:
        per = float(val_crop) / 20
        generate_and_compare_crop(per)
        val_crop -= 5
    for i in range(0, 4):
        generate_and_compare_rotation(i * 90, True)
    for i in range(1, 11):
        generate_and_compare_rotation(i / 10, True)
        generate_and_compare_rotation(-i / 10, True)
    generate_and_compare_flip()
    for i in range(1, 21):
        generate_and_compare_logo(i / 40)
    for i in range(0, 21):
        generate_and_compare_enhancement(1, i / 10)
    for i in range(0, 41):
        generate_and_compare_enhancement(2, i / 10)
    for i in range(0, 21):
        generate_and_compare_enhancement(3, i / 10)
    generate_and_compare_resize_360x360()
