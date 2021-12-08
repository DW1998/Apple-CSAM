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


# plot
# fig, ax = plt.subplots()

# resolution
x_points_resolution = [i * 5 for i in range(0, 21)]
y_points_resolution_sub_minus_one = [1, 8, 36, 48, 60, 65, 73, 67, 80, 76, 77, 80, 82, 88, 83, 88, 93, 98, 96, 96, 98]
y_points_resolution_sub_zero = [1, 8, 38, 47, 55, 64, 73, 69, 75, 77, 76, 80, 82, 88, 82, 91, 93, 97, 98, 97, 98]
y_points_resolution_sub_one = [1, 8, 36, 48, 57, 63, 72, 69, 76, 77, 76, 81, 82, 89, 82, 91, 93, 96, 98, 97, 97]
y_points_resolution_sub_two = [1, 8, 36, 48, 60, 65, 73, 67, 80, 76, 77, 80, 82, 88, 83, 88, 93, 98, 96, 96, 98]
y_points_resolution_error_sub_minus_one = [6.89, 3.71, 1.24, 0.85, 0.53, 0.44, 0.35, 0.37, 0.23, 0.28, 0.27, 0.23, 0.21, 0.13, 0.18, 0.12, 0.07, 0.02, 0.04, 0.04, 0.02]
y_points_resolution_error_sub_zero = [6.95, 3.69, 1.23, 0.87, 0.59, 0.49, 0.36, 0.34, 0.27, 0.27, 0.28, 0.21, 0.2, 0.13, 0.19, 0.09, 0.07, 0.03, 0.02, 0.03, 0.02]
y_points_resolution_error_sub_one = [6.95, 3.7, 1.22, 0.86, 0.56, 0.49, 0.36, 0.34, 0.27, 0.27, 0.29, 0.2, 0.21, 0.12, 0.19, 0.09, 0.07, 0.04, 0.02, 0.03, 0.03]
y_points_resolution_error_sub_two = [6.89, 3.71, 1.24, 0.85, 0.53, 0.44, 0.35, 0.37, 0.23, 0.28, 0.27, 0.23, 0.21, 0.13, 0.18, 0.12, 0.07, 0.02, 0.04, 0.04, 0.02]

# ax.plot(x_points_resolution, y_points_resolution_sub_minus_one, "-s", label="subsampling -1")
# ax.plot(x_points_resolution, y_points_resolution_sub_zero, "-o", label="subsampling 0")
# ax.plot(x_points_resolution, y_points_resolution_sub_one, "-x", label="subsampling 1")
# ax.plot(x_points_resolution, y_points_resolution_sub_two, "-|", label="subsampling 2")

# ax.plot(x_points_resolution, y_points_resolution_error_sub_minus_one, "-s", label="subsampling -1")
# ax.plot(x_points_resolution, y_points_resolution_error_sub_zero, "-o", label="subsampling 0")
# ax.plot(x_points_resolution, y_points_resolution_error_sub_one, "-x", label="subsampling 1")
# ax.plot(x_points_resolution, y_points_resolution_error_sub_two, "-|", label="subsampling 2")


# resize
x_points_resize = [i * 5 for i in range(1, 21)]
y_points_resize = [4, 42, 62, 73, 79, 85, 89, 93, 93, 96, 92, 96, 97, 96, 97, 96, 97, 98, 96, 100]
y_points_resize_error = [4.79, 1.16, 0.56, 0.36, 0.24, 0.16, 0.12, 0.08, 0.08, 0.04, 0.08, 0.04, 0.03, 0.04, 0.03, 0.04, 0.03, 0.02, 0.04, 0.0]

# ax.plot(x_points_resize, y_points_resize, "-x")

# ax.plot(x_points_resize, y_points_resize_error, "-x")

# crop
x_points_crop = [i / 4 for i in range(20, -1, -1)]
y_points_crop = [0, 1, 1, 1, 2, 2, 2, 3, 2, 3, 5, 5, 7, 11, 14, 20, 32, 41, 48, 75, 100]
y_points_crop_error = [5.97, 5.64, 5.46, 5.21, 4.91, 4.69, 4.39, 4.02, 3.77, 3.54, 3.19, 2.83, 2.54, 2.26, 1.96, 1.69, 1.34, 1.1, 0.87, 0.34, 0.0]

# ax.plot(x_points_crop, y_points_crop, "-x")
# ax.plot(x_points_crop, y_points_crop_error, "-x")

# rotation

x_points_rotation = [i / 10 for i in range(-10, 11, 1)]
y_points_rotation_expand_false = [0, 0, 0, 0, 0, 0, 2, 6, 8, 35, 100, 29, 6, 3, 2, 1, 1, 1, 2, 2, 2]
y_points_rotation_expand_true = [0, 0, 1, 1, 1, 1, 1, 1, 1, 7, 100, 3, 0, 1, 1, 1, 1, 0, 0, 0, 0]
y_points_rotation_error_expand_false = [5.33, 5.27, 5.16, 5.05, 4.91, 4.6, 4.36, 3.96, 3.06, 1.46, 0, 1.53, 3.23, 4.03, 4.51, 4.76, 5.03, 5.04, 5.19, 5.23, 5.29]
y_points_rotation_error_expand_true = [6.08, 6.06, 6.02, 5.93, 5.85, 5.64, 5.46, 5.19, 4.88, 3.85, 0, 3.97, 5.01, 5.22, 5.42, 5.54, 5.71, 5.68, 5.77, 5.81, 5.88]

# ax.plot(x_points_rotation, y_points_rotation_expand_false, "-o", label="expand = False")
# ax.plot(x_points_rotation, y_points_rotation_expand_true, "-x", label="expand = True")

# ax.plot(x_points_rotation, y_points_rotation_error_expand_false, "-o", label="expand = False")
# ax.plot(x_points_rotation, y_points_rotation_error_expand_true, "-x", label="expand = True")

# logo

x_points_logo = [i * 2.5 for i in range(0, 21)]
y_points_logo = [100, 81, 65, 57, 46, 33, 24, 18, 13, 11, 12, 8, 4, 4, 2, 3, 1, 0, 0, 0, 0]
y_points_logo_error = [0.0, 0.23, 0.64, 0.94, 1.26, 1.75, 2.3, 2.94, 3.47, 4.06, 4.44, 5.09, 5.93, 6.58, 7.52, 8.51, 9.65, 10.88, 12.04, 13.23, 14.78]

# ax.plot(x_points_logo, y_points_logo, "-x")
# ax.plot(x_points_logo, y_points_logo_error, "-x")

# contrast

x_points_contrast = [i * 10 for i in range(0, 21)]
y_points_contrast = [0, 35, 60, 75, 83, 82, 84, 87, 91, 90, 100, 34, 12, 4, 1, 0, 0, 0, 0, 0, 0]
y_points_contrast_error = [47.0, 1.74, 0.68, 0.33, 0.22, 0.21, 0.17, 0.16, 0.1, 0.11, 0.0, 1.83, 4.22, 7.03, 9.72, 12.26, 14.48, 16.58, 18.4, 20.23, 21.86]

# ax.plot(x_points_contrast, y_points_contrast, "-x")
# ax.plot(x_points_contrast, y_points_contrast_error, "-x")

# color

x_points_color = [i * 10 for i in range(0, 41)]
y_points_color = [41, 46, 47, 54, 61, 68, 78, 80, 81, 84, 100, 79, 79, 73, 65, 62, 55, 49, 44, 42, 40, 39, 35, 31, 25, 21, 23, 21, 18, 17, 17, 15, 13, 12, 11, 9, 8, 8, 7, 7, 5]
y_points_color_error = [1.02, 0.9, 0.81, 0.64, 0.52, 0.39, 0.27, 0.24, 0.21, 0.17, 0.0, 0.3, 0.37, 0.51, 0.66, 0.77, 0.99, 1.21, 1.42, 1.59, 1.71, 1.86, 2.07, 2.28, 2.6, 2.89, 3.14, 3.36, 3.63, 4.0, 4.35, 4.63, 4.92, 5.33, 5.7, 5.99, 6.28, 6.64, 6.82, 7.22, 7.54]

# ax.plot(x_points_color, y_points_color, "-x")
# ax.plot(x_points_color, y_points_color_error, "-x")

# brightness

x_points_brightness = [i * 10 for i in range(0, 21)]
y_points_brightness = [0, 3, 10, 39, 59, 66, 80, 90, 89, 89, 100, 42, 11, 4, 3, 0, 0, 0, 0, 0, 0]
y_points_brightness_error = [46.83, 4.85, 2.52, 1.1, 0.57, 0.45, 0.26, 0.12, 0.13, 0.13, 0.0, 2.44, 6.56, 10.9, 15.54, 19.98, 23.38, 26.01, 28.5, 30.49, 32.38]

# flip: 0, 29.63

# resize360x360: 100, 0.0

# ax.plot(x_points_brightness, y_points_brightness, "-x")
# ax.plot(x_points_brightness, y_points_brightness_error, "-x")

# ax.xaxis.set_major_formatter(mtick.PercentFormatter())
# ax.yaxis.set_major_formatter(mtick.PercentFormatter())

# plt.xlabel("brightness")
# plt.ylabel("average error")
# plt.ylabel("unchanged hashes")
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
        out_lines.append(line[:-1] + ", " + str(offset))
        offsets.append(str(offset) + ", ")
    with open("C:/Git Repos/Apple-CSAM/results_error.txt", 'w') as f:
        for line in out_lines:
            f.write(line)
            f.write('\n')
    with open("C:/Git Repos/Apple-CSAM/error.txt", 'w') as f:
        for o in offsets:
            f.write(o)
    with open("C:/Git Repos/Apple-CSAM/unchanged.txt", 'w') as f:
        for line in out_lines:
            f.write(line.split(",")[-2] + ",")
    print("printed offset to txt file")


if __name__ == '__main__':
    pass
    # calc_avg_offset()
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
