"""Implementation of script to turn image to greyscale on CPU and GPU."""

__authors__ = "Mgr. Ing. Matúš Jókay, PhD., Tomáš Vavro, Matúš Vetrík"
__licence__ = "MIT"

from PIL import Image
from numba import cuda
import numpy as np
import time
from math import ceil
import os
import matplotlib.pyplot as plt


INPUT_FILE_NAME = "./assets/images/"


@cuda.jit
def grayscale_kernel(img, gray_img):
    """Greyscale formula on cuda.

        Arguments:
            img -- rgb array
            gray_img -- output imagw
    """
    i, j = cuda.grid(2)
    if i < img.shape[0] and j < img.shape[1]:
        gray = 0.2989 * img[i][j][0] + 0.5870 * img[i][j][1] + 0.1140 * img[i][j][2]
        gray_img[i][j] = [gray, gray, gray]


def to_grayscale(img):
    """Greyscale function on cuda.

        Arguments:
            img -- rgb array
    """
    gray_img = img.copy()

    tpb = (16, 16)
    bpg = (ceil(img.shape[0] / tpb[0]), ceil(img.shape[1] / tpb[1]))

    grayscale_kernel[bpg, tpb](img, gray_img)

    return gray_img


def main():
    """Main function on GPU."""
    s = 0
    for filename in os.listdir(INPUT_FILE_NAME):
        img = np.array(Image.open(f'./assets/images/{filename}'))

        start = time.time()
        gray = to_grayscale(img)
        end = time.time()
        s += end - start
        print(f"Time: {end - start} sec")

        plt.imsave(f"./assets/output2/{filename}", gray)
    print(f"Sum: {s}")


def transform_to_grayscale(img):
    """Greyscale formula.

        Arguments:
            img -- rgb array
    """
    gray = img.copy()
    for i in range(len(img)):
        for j in range(len(img[0])):
            gray_value = 0.2989 * img[i][j][0] + 0.5870 * img[i][j][1] + 0.1140 * img[i][j][2]
            gray[i][j] = [gray_value, gray_value, gray_value]
    return gray


def main_seq():
    """Main function on CPU."""
    s = 0
    for filename in os.listdir(INPUT_FILE_NAME):
        img = plt.imread(f'./assets/images/{filename}')

        start = time.time()
        gray = transform_to_grayscale(img)
        end = time.time()
        s += end-start
        print(f"Time: {end - start} sec")

        plt.imsave(f"./assets/output/{filename}", gray)
    print(f"Sum: {s}")


main()
# main_seq()
