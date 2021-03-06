# Copyright (c) 2021 Anish Athalye. Released under the MIT license.
import tensorflow as tf
from scipy.ndimage.filters import gaussian_filter
import os

import util
from util_collide import *

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

DEFAULT_MODEL_PATH = 'model.onnx'
DEFAULT_SEED_PATH = 'neuralhash_128x96_seed1.dat'
DEFAULT_TARGET_HASH = '59a34eabe31910abfb06f308'
DEFAULT_ITERATIONS = 30
DEFAULT_SAVE_ITERATIONS = 0
DEFAULT_LR = 2.0
DEFAULT_COMBINED_THRESHOLD = 2
DEFAULT_K = 10.0
DEFAULT_CLIP_RANGE = 0.1
DEFAULT_W_L2 = 2e-3
DEFAULT_W_TV = 1e-4
DEFAULT_W_HASH = 0.8
DEFAULT_BLUR = 0


def collide(img_path, nnhash, num_iter, blur):
    tf.compat.v1.disable_eager_execution()

    model = load_model(DEFAULT_MODEL_PATH)
    image = model.tensor_dict['image']
    logits = model.tensor_dict['leaf/logits']
    seed = load_seed(DEFAULT_SEED_PATH)

    original = load_image(img_path)
    h = hash_from_hex(nnhash)

    with model.graph.as_default():
        with tf.compat.v1.Session() as sess:
            sess.run(tf.compat.v1.global_variables_initializer())

            proj = tf.reshape(tf.linalg.matmul(seed, tf.reshape(logits, (128, 1))), (96,))
            # proj is in R^96; it's interpreted as a 96-bit hash by mapping
            # entries < 0 to the bit '0', and entries >= 0 to the bit '1'
            normalized, _ = tf.linalg.normalize(proj)
            hash_output = tf.sigmoid(normalized * DEFAULT_K)
            # now, hash_output has entries in (0, 1); it's interpreted by
            # mapping entries < 0.5 to the bit '0' and entries >= 0.5 to the
            # bit '1'

            # we clip hash_output to (clip_range, 1-clip_range); this seems to
            # improve the search (we don't "waste" perturbation tweaking
            # "strong" bits); the sigmoid already does this to some degree, but
            # this seems to help
            hash_output = tf.clip_by_value(hash_output, DEFAULT_CLIP_RANGE, 1.0 - DEFAULT_CLIP_RANGE) - 0.5
            hash_output = hash_output * (0.5 / (0.5 - DEFAULT_CLIP_RANGE))
            hash_output = hash_output + 0.5

            # hash loss: how far away we are from the target hash
            hash_loss = tf.math.reduce_sum(tf.math.squared_difference(hash_output, h))

            perturbation = image - original
            # image loss: how big / noticeable is the perturbation?
            img_loss = DEFAULT_W_L2 * tf.nn.l2_loss(perturbation) + DEFAULT_W_TV * tf.image.total_variation(perturbation)[0]

            # combined loss: try to minimize both at once
            combined_loss = DEFAULT_W_HASH * hash_loss + (1 - DEFAULT_W_HASH) * img_loss

            # gradients of all the losses
            g_hash_loss, = tf.gradients(hash_loss, image)
            g_img_loss, = tf.gradients(img_loss, image)
            g_combined_loss, = tf.gradients(combined_loss, image)

            # perform attack

            x = original
            best = (float('inf'), 0)  # (distance, image quality loss)
            dist = float('inf')

            perfect_collision_list = list()

            for i in range(num_iter):
                # we do an alternating projections style attack here; if we
                # haven't found a colliding image yet, only optimize for that;
                # if we have a colliding image, then minimize the size of the
                # perturbation; if we're close, then do both at once
                if dist == 0:
                    loss_name, loss, g = 'image', img_loss, g_img_loss
                elif best[0] == 0 and dist <= DEFAULT_COMBINED_THRESHOLD:
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
                if score < best or (DEFAULT_SAVE_ITERATIONS > 0 and (i + 1) % DEFAULT_SAVE_ITERATIONS == 0):
                    img_dir = util.collide_dir + nnhash + "/"
                    try:
                        os.mkdir(img_dir, 0o777)
                        print("added dir: " + img_dir)
                    except OSError:
                        pass
                    save_image(x, os.path.join(img_dir, 'dist={:02d}_q={:.3f}_iter={:05d}.png'.format(
                        dist, img_loss_v, i + 1
                    )))
                if score < best:
                    best = score

                # gradient descent step
                g_v_norm = g_v / np.linalg.norm(g_v)
                x = x - DEFAULT_LR * g_v_norm
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
                if nnhash == str(hash_to_hex(hash_output_v)):
                    perfect_collision_list.append(i + 1)
            if len(perfect_collision_list) == 0:
                print("No perfect collision found")
            else:
                print("Perfect collisions at:", end=" ")
                print(perfect_collision_list)


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
