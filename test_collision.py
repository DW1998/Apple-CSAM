# Copyright (c) 2021 Anish Athalye. Released under the MIT license.
import sys
from itertools import chain
from statistics import mean

import tensorflow as tf
from scipy.ndimage.filters import gaussian_filter
import os

import nnhash
from util_collide import *

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

DEFAULT_MODEL_PATH = 'model.onnx'
DEFAULT_SEED_PATH = 'neuralhash_128x96_seed1.dat'
DEFAULT_TARGET_HASH = '59a34eabe31910abfb06f308'
DEFAULT_ITERATIONS = 3
DEFAULT_SAVE_ITERATIONS = 0
DEFAULT_LR = 2.0
DEFAULT_COMBINED_THRESHOLD = 2
DEFAULT_K = 10.0
DEFAULT_CLIP_RANGE = 0.1
DEFAULT_W_L2 = 2e-3
DEFAULT_W_TV = 1e-4
DEFAULT_W_HASH = 0.8
DEFAULT_BLUR = 0

collide_dir = "D:/Apple-CSAM-Files/Collide-Attacks/"
collide_img_dir = collide_dir + "Collide-Images/"
target_img_dir = collide_dir + "Target-Images/"
attack_dir = collide_dir + "Attacks/"
combine_dir = collide_dir + "Combine-Outputs/"


def collide(img_path, t_hash, num_iter, save_iter, lr, comb_t, k, clip_r, w_l2, w_tv, w_hash, blur, t_img, c_img,
            folder):
    tf.compat.v1.disable_eager_execution()

    model = load_model(DEFAULT_MODEL_PATH)
    image = model.tensor_dict['image']
    logits = model.tensor_dict['leaf/logits']
    seed = load_seed(DEFAULT_SEED_PATH)

    original = load_image(img_path)
    h = hash_from_hex(t_hash)

    with model.graph.as_default():
        with tf.compat.v1.Session() as sess:
            sess.run(tf.compat.v1.global_variables_initializer())

            proj = tf.reshape(tf.linalg.matmul(seed, tf.reshape(logits, (128, 1))), (96,))
            # proj is in R^96; it's interpreted as a 96-bit hash by mapping
            # entries < 0 to the bit '0', and entries >= 0 to the bit '1'
            normalized, _ = tf.linalg.normalize(proj)
            hash_output = tf.sigmoid(normalized * k)
            # now, hash_output has entries in (0, 1); it's interpreted by
            # mapping entries < 0.5 to the bit '0' and entries >= 0.5 to the
            # bit '1'

            # we clip hash_output to (clip_range, 1-clip_range); this seems to
            # improve the search (we don't "waste" perturbation tweaking
            # "strong" bits); the sigmoid already does this to some degree, but
            # this seems to help
            hash_output = tf.clip_by_value(hash_output, clip_r, 1.0 - clip_r) - 0.5
            hash_output = hash_output * (0.5 / (0.5 - clip_r))
            hash_output = hash_output + 0.5

            # hash loss: how far away we are from the target hash
            hash_loss = tf.math.reduce_sum(tf.math.squared_difference(hash_output, h))

            perturbation = image - original
            # image loss: how big / noticeable is the perturbation?
            img_loss = w_l2 * tf.nn.l2_loss(perturbation) + w_tv * tf.image.total_variation(perturbation)[0]

            # combined loss: try to minimize both at once
            combined_loss = w_hash * hash_loss + (1 - w_hash) * img_loss

            # gradients of all the losses
            g_hash_loss, = tf.gradients(hash_loss, image)
            g_img_loss, = tf.gradients(img_loss, image)
            g_combined_loss, = tf.gradients(combined_loss, image)

            # perform attack

            x = original
            best = (float('inf'), 0)  # (distance, image quality loss)
            dist = float('inf')

            for i in range(num_iter):
                # we do an alternating projections style attack here; if we
                # haven't found a colliding image yet, only optimize for that;
                # if we have a colliding image, then minimize the size of the
                # perturbation; if we're close, then do both at once
                if dist == 0:
                    loss_name, loss, g = 'image', img_loss, g_img_loss
                elif best[0] == 0 and dist <= comb_t:
                    loss_name, loss, g = 'combined', combined_loss, g_combined_loss
                else:
                    loss_name, loss, g = 'hash', hash_loss, g_hash_loss

                # compute loss values and gradient
                xq = quantize(x)  # take derivatives wrt the quantized version of the image
                hash_output_v, img_loss_v, loss_v, g_v = sess.run([hash_output, img_loss, loss, g],
                                                                  feed_dict={image: xq})
                dist = np.sum((hash_output_v >= 0.5) != (h >= 0.5))

                # if it's better than any image found so far, save it
                score = (dist, img_loss_v)
                if score < best or (save_iter > 0 and (i + 1) % save_iter == 0):
                    # img_dir = attack_dir + t_img.split(".")[0] + "/" + c_img.split(".")[0] + "/"
                    img_dir_folder = f"{attack_dir}{folder}/"
                    img_dir_target = f"{img_dir_folder}{t_img}/"
                    img_dir_collide = f"{img_dir_target}{c_img}/"
                    try:
                        os.mkdir(img_dir_folder, 0o777)
                    except OSError:
                        pass
                    try:
                        os.mkdir(img_dir_target, 0o777)
                    except OSError:
                        pass
                    try:
                        os.mkdir(img_dir_collide, 0o777)
                    except OSError:
                        pass
                    save_image(x, os.path.join(img_dir_collide, 'dist={:02d}_q={:.3f}_iter={:05d}.png'.format(
                        dist, img_loss_v, i + 1
                    )))
                if score < best:
                    best = score
                if save_iter > 0 and ((i + 1) % save_iter == 0 or i == 0):
                    with open(f"{img_dir_folder}output{t_img}.txt", 'a+') as f:
                        f.write(f"{c_img}, {best[0]}, {best[1]:.3f}, {i + 1}")
                        f.write('\n')

                # gradient descent step
                g_v_norm = g_v / np.linalg.norm(g_v)
                x = x - lr * g_v_norm
                if blur > 0:
                    x = blur_perturbation(original, x, blur)
                x = x.clip(-1, 1)
                print('iteration: {}/{}, best: ({}, {:.3f}), hash: {}, distance: {}, loss: {:.3f} ({})'.format(
                    i + 1,
                    num_iter,
                    best[0],
                    best[1],
                    hash_to_hex(hash_output_v),
                    dist,
                    loss_v,
                    loss_name
                ))


def quantize(x):
    x = (x + 1.0) * (255.0 / 2.0)
    x = x.astype(np.uint8).astype(np.float32)
    x = x / (255.0 / 2.0) - 1.0
    return x


def blur_perturbation(original, x, sigma):
    perturbation = x - original
    perturbation = gaussian_filter_by_channel(perturbation, sigma=sigma)
    return original + perturbation


def gaussian_filter_by_channel(x, sigma):
    return np.stack([gaussian_filter(x[0, ch, :, :], sigma) for ch in range(x.shape[1])])[np.newaxis]


def test_collide():
    for t_img in os.listdir(target_img_dir):
        t_hash = nnhash.calc_nnhash(target_img_dir + t_img)
        for c_img in os.listdir(collide_img_dir):
            c_img_path = collide_img_dir + c_img
            collide(c_img_path, t_hash, 1000, 25, DEFAULT_LR, DEFAULT_COMBINED_THRESHOLD, DEFAULT_K,
                    DEFAULT_CLIP_RANGE, DEFAULT_W_L2, DEFAULT_W_TV, DEFAULT_W_HASH, DEFAULT_BLUR,
                    t_img.split(".")[0], c_img.split(".")[0], "Default")
            range_K = chain(range(5, 10), range(11, 21))
            for i in range_K:
                s = f"K{i}"
                collide(c_img_path, t_hash, 1000, 25, DEFAULT_LR, DEFAULT_COMBINED_THRESHOLD, i,
                        DEFAULT_CLIP_RANGE, DEFAULT_W_L2, DEFAULT_W_TV, DEFAULT_W_HASH, DEFAULT_BLUR,
                        t_img.split(".")[0], c_img.split(".")[0], s)
            range_LR = chain(range(1, 4), range(5, 21))
            for i in range_LR:
                j = float(i / 2)
                s = f"LR{j}"
                collide(c_img_path, t_hash, 1000, 25, DEFAULT_LR, DEFAULT_COMBINED_THRESHOLD, j,
                        DEFAULT_CLIP_RANGE, DEFAULT_W_L2, DEFAULT_W_TV, DEFAULT_W_HASH, DEFAULT_BLUR,
                        t_img.split(".")[0], c_img.split(".")[0], s)
            range_Comb_T0 = chain(range(0, 2), range(3, 5))
            for i in range_Comb_T0:
                s = f"Comb_T{i}"
                collide(c_img_path, t_hash, 1000, 25, DEFAULT_LR, i, DEFAULT_K,
                        DEFAULT_CLIP_RANGE, DEFAULT_W_L2, DEFAULT_W_TV, DEFAULT_W_HASH, DEFAULT_BLUR,
                        t_img.split(".")[0], c_img.split(".")[0], s)
            for i in range(1, 10):
                j = float(i / 10)
                s = f"Blur{j}"
                collide(c_img_path, t_hash, 1000, 25, DEFAULT_LR, DEFAULT_COMBINED_THRESHOLD, DEFAULT_K,
                        DEFAULT_CLIP_RANGE, DEFAULT_W_L2, DEFAULT_W_TV, DEFAULT_W_HASH, j,
                        t_img.split(".")[0], c_img.split(".")[0], s)
            range_Clip_R = chain(range(0, 2), range(3, 10))
            for i in range_Clip_R:
                j = float(i / 20)
                s = f"Clip_R{j}"
                collide(c_img_path, t_hash, 1000, 25, DEFAULT_LR, DEFAULT_COMBINED_THRESHOLD, DEFAULT_K,
                        j, DEFAULT_W_L2, DEFAULT_W_TV, DEFAULT_W_HASH, DEFAULT_BLUR,
                        t_img.split(".")[0], c_img.split(".")[0], s)
            collide(c_img_path, t_hash, 1000, 25, 8.5, DEFAULT_COMBINED_THRESHOLD, 15,
                    DEFAULT_CLIP_RANGE, DEFAULT_W_L2, DEFAULT_W_TV, DEFAULT_W_HASH, DEFAULT_BLUR,
                    t_img.split(".")[0], c_img.split(".")[0], "Optimized")
            for i in range(1, 10):
                j = float(i / 10)
                s = f"Optimized_Blur{j}"
                collide(c_img_path, t_hash, 1000, 25, 8.5, DEFAULT_COMBINED_THRESHOLD, 15,
                        DEFAULT_CLIP_RANGE, DEFAULT_W_L2, DEFAULT_W_TV, DEFAULT_W_HASH, j,
                        t_img.split(".")[0], c_img.split(".")[0], s)


def set_key(dictionary, key, value_dist, value_loss):
    if key not in dictionary:
        dictionary[key] = (list(), list())
        dictionary[key][0].append(int(value_dist))
        dictionary[key][1].append(float(value_loss))
    else:
        dictionary[key][0].append(int(value_dist))
        dictionary[key][1].append(float(value_loss))


def set_key2(dictionary, key, value_dist, value_loss):
    if key not in dictionary:
        dictionary[key] = (list(), list())
        dictionary[key][0].append(value_dist)
        dictionary[key][1].append(value_loss)
    else:
        dictionary[key][0].append(value_dist)
        dictionary[key][1].append(value_loss)


def calc_avg():
    for att_folder in os.listdir(attack_dir):
        dict_avg = dict()
        base_folder = f"{attack_dir}{att_folder}/"
        for txt_file in os.listdir(base_folder):
            if txt_file.endswith(".txt") and txt_file != "output_average.txt":
                with open(f"{base_folder}{txt_file}", 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        data = line.split(',')
                        set_key(dict_avg, data[3][1:-1], data[1][1:], data[2][1:])
        with open(f"{base_folder}output_average.txt", 'w') as f:
            for k, v in dict_avg.items():
                f.write(f"{k}: {mean(v[0]):.3f}, {mean(v[1]):.3f}")
                f.write('\n')
    calc_hits()


def calc_hits():
    for att_folder in os.listdir(attack_dir):
        base_folder = f"{attack_dir}{att_folder}/"
        hits = 0
        hits_iterations = list()
        for d in os.listdir(base_folder):
            if os.path.isdir(f"{base_folder}{d}"):
                target_base_folder = f"{base_folder}{d}/"
                for img_folder in os.listdir(target_base_folder):
                    target_img_folder = f"{target_base_folder}{img_folder}"
                    best_iter = sys.maxsize
                    for img in os.listdir(target_img_folder):
                        dist = int(img.split('=')[1].split('_')[0])
                        # q = img.split('=')[2].split('_')[0]
                        i = int(img.split("=")[3].split('.')[0])
                        if dist == 0 and i < best_iter:
                            best_iter = i
                    if best_iter < sys.maxsize:
                        hits += 1
                        hits_iterations.append(best_iter)
        if hits > 0:
            with open(f"{base_folder}output_average.txt", 'a+') as f:
                f.write(f"hits:{hits}, avg_iter:{mean(hits_iterations):.3f}")
                f.write('\n')


def combine_outputs(name):
    combined = list()
    for txt_file in os.listdir(combine_dir):
        if txt_file.endswith(".txt"):
            lst1 = list()
            lst2 = list()
            lst1.append(f"{txt_file}_1")
            lst2.append(f"{txt_file}_2")
            with open(f"{combine_dir}{txt_file}", 'r') as f:
                lines = f.readlines()
                for line in lines:
                    data_h = line.split(':')
                    if data_h[0] == "hits":
                        val_h = data_h[1].split(',')[0]
                        val_a = data_h[2][:-1]
                        lst1.append(int(val_h))
                        lst2.append(float(val_a))
                    else:
                        values = line.split(':')[1].split(',')
                        val_d = values[0][1:]
                        val_l = values[1][1:][:-1]
                        lst1.append(float(val_d))
                        lst2.append(float(val_l))
            combined.append(lst1)
            combined.append(lst2)
    with open(f"{combine_dir}Results/{name}.txt", 'w') as f:
        for line in combined:
            f.write(str(line))
            f.write('\n')


if __name__ == '__main__':
    pass
    test_collide()
    calc_avg()
