import os
from PIL import Image, ImageEnhance
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

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
test_dir = root_dir + "Test/"


# plot
# fig, ax = plt.subplots()

# resolution
x_points_resolution = [i * 5 for i in range(0, 21)]
y_points_resolution_sub_minus_one = [1, 8, 36, 48, 60, 65, 73, 67, 80, 76, 77, 80, 82, 88, 83, 88, 93, 98, 96, 96, 98]
y_points_resolution_sub_zero = [1, 8, 38, 47, 55, 64, 73, 69, 75, 77, 76, 80, 82, 88, 82, 91, 93, 97, 98, 97, 98]
y_points_resolution_sub_one = [1, 8, 36, 48, 57, 63, 72, 69, 76, 77, 76, 81, 82, 89, 82, 91, 93, 96, 98, 97, 97]
y_points_resolution_sub_two = [1, 8, 36, 48, 60, 65, 73, 67, 80, 76, 77, 80, 82, 88, 83, 88, 93, 98, 96, 96, 98]

# ax.plot(x_points_resolution, y_points_resolution_sub_minus_one, "-s", label="subsampling -1")
# ax.plot(x_points_resolution, y_points_resolution_sub_zero, "-o", label="subsampling 0")
# ax.plot(x_points_resolution, y_points_resolution_sub_one, "-x", label="subsampling 1")
# ax.plot(x_points_resolution, y_points_resolution_sub_two, "-|", label="subsampling 2")

# resize
x_points_resize = [i * 5 for i in range(0, 21)]
y_points_resize = [0, 4, 40, 64, 73, 78, 86, 89, 93, 92, 96, 93, 95, 94, 96, 96, 95, 95, 98, 97, 98]

# ax.plot(x_points_resize, y_points_resize, "-x")

# crop
x_points_crop = [i / 2 for i in range(12, -1, -1)]
y_points_crop = [0, 0, 1, 1, 2, 2, 2, 5, 7, 15, 34, 48, 98]

# ax.plot(x_points_crop, y_points_crop, "-x")

# rotation

x_points_rotation = [i for i in range(-10, 11, 1)]
y_points_rotation_expand_false = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 98, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
y_points_rotation_expand_true = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 98, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# ax.plot(x_points_rotation, y_points_rotation_expand_false, "-o", label="expand = False")
# ax.plot(x_points_rotation, y_points_rotation_expand_true, "-x", label="expand = True")

# logo

x_points_logo = [i * 5 for i in range(0, 11)]
y_points_logo = [98, 64, 46, 23, 13, 12, 4, 2, 1, 0, 0]

# ax.plot(x_points_logo, y_points_logo, "-x")

# contrast

x_points_contrast = [i * 10 for i in range(0, 17)]
y_points_contrast = [0, 12, 40, 53, 69, 76, 81, 85, 86, 86, 98, 34, 10, 3, 1, 0, 0]

# ax.plot(x_points_contrast, y_points_contrast, "-x")

# color

x_points_color = [i * 10 for i in range(0, 31)]
y_points_color = [41, 47, 51, 56, 61, 70, 80, 75, 78, 80, 98, 75, 72, 58, 63, 57, 52, 46, 45, 39, 40, 36, 33, 30, 24, 21, 19, 18, 16, 13, 16]

# ax.plot(x_points_color, y_points_color, "-x")

# brightness

x_points_brightness = [i * 10 for i in range(0, 17)]
y_points_brightness = [0, 5, 7, 37, 56, 67, 74, 87, 87, 82, 98, 38, 10, 3, 3, 0, 0]

# ax.plot(x_points_brightness, y_points_brightness, "-x")

# sharpness

x_points_sharpness = [i * 10 for i in range(0, 31)]
y_points_sharpness = [86, 81, 79, 82, 83, 84, 85, 84, 85, 85, 98, 86, 89, 87, 87, 88, 83, 79, 79, 76, 84, 71, 71, 69, 68, 69, 64, 64, 62, 62, 63]

# ax.plot(x_points_sharpness, y_points_sharpness, "-x")

# ax.xaxis.set_major_formatter(mtick.PercentFormatter())
# ax.yaxis.set_major_formatter(mtick.PercentFormatter())

# plt.xlabel("Sharpness")
# plt.ylabel("Unchanged hashes")
# plt.legend()
# plt.grid(True)
# plt.show()


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


def generate_and_compare_resolution(res, sub):
    result_dir = resolution_dir + "Subsampling=" + str(sub) + "/res" + str(res) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        # print("created folder %s" % result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img.save(result_dir + img_file, quality=res, subsampling=sub)
    compare_images_jpg(result_dir)


def generate_and_compare_resize(scale):
    result_dir = resize_dir + "scale" + str(scale) + "/"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        # print("created folder %s" % result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        width, height = img.size
        img_resize = img.resize((int(width * scale), int(height * scale))).convert('RGB')
        img_resize.save(result_dir + img_file.split(".")[0] + ".png")
    compare_images_png(result_dir)


def generate_and_compare_resize_360x360():
    if not os.path.exists(resize360x360dir):
        os.makedirs(resize360x360dir)
        # print("created folder %s % resize360x360dir)
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
        # print("created folder %s" % result_dir)
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
        # print("created folder %s" % result_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img.rotate = img.rotate(degree, expand=exp).convert('RGB')
        img.rotate.save(result_dir + img_file.split(".")[0] + ".png")
    compare_images_png(result_dir)


def generate_and_compare_flip():
    if not os.path.exists(flip_dir):
        os.makedirs(flip_dir)
        # print("created folder %s" % flip_dir)
    for img_file in os.listdir(standard_dir):
        img = Image.open(standard_dir + img_file)
        img_flip = img.transpose(Image.FLIP_LEFT_RIGHT).convert('RGB')
        img_flip.save(flip_dir + img_file.split(".")[0] + ".png")
    compare_images_png(flip_dir)


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
        # print("created folder %s" % result_dir)
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
        out_lines.append(line[:-1] + ", " + str(offset))
    with open("C:/Git Repos/Apple-CSAM/results_offset.txt", 'w') as f:
        for line in out_lines:
            f.write(line)
            f.write('\n')
    print("printed offset to txt file")


if __name__ == '__main__':
    pass
    calc_avg_offset()
    # conv_to_png()
    # for i in range(-1, 3):
    #    ctr = 0
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
    #    per = float(val_crop) / 20
    #    generate_and_compare_crop(per)
    #    val_crop -= 5
    # for i in range(0, 4):
    #    generate_and_compare_rotation(i * 90, False)
    # for i in range(1, 11):
    #    generate_and_compare_rotation(i / 10, False)
    #    generate_and_compare_rotation(-i / 10, False)
    # for i in range(0, 4):
    #    generate_and_compare_rotation(i * 90, True)
    # for i in range(1, 11):
    #    generate_and_compare_rotation(i / 10, True)
    #    generate_and_compare_rotation(-i / 10, True)
    # generate_and_compare_flip()
    # for i in range(1, 21):
    #    generate_and_compare_logo(i / 40)
    # for i in range(0, 21):
    #    generate_and_compare_enhancement(1, i / 10)
    # for i in range(0, 41):
    #    generate_and_compare_enhancement(2, i / 10)
    # for i in range(0, 21):
    #    generate_and_compare_enhancement(3, i / 10)
    # generate_and_compare_resize_360x360()
