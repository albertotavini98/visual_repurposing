from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os 
import time 
from itertools import product
import random
from util import blender, pianoforte

def RGB_substitution(im1, im2, im3, order=[1,2,3]):
    if str(type(im1)) == '<class \'numpy.ndarray\'>':
        im1_bw = Image.fromarray(im1).convert('L')
        im2_bw = Image.fromarray(im2).convert('L')
        im3_bw = Image.fromarray(im3).convert('L')
    else:
        im1_bw = im1.convert('L')
        im2_bw = im2.convert('L')
        im3_bw = im3.convert('L')
    arr1 = np.array(im1_bw)
    arr2 = np.array(im2_bw)
    arr3 = np.array(im3_bw)
    arr_rgb = np.stack((arr1, arr2, arr3), axis=-1)
    plt.figure(figsize=(9, 9))
    plt.imshow(arr_rgb)
    im_rgb = Image.fromarray(arr_rgb).convert('L')
    plt.figure(figsize=(9, 9))
    plt.imshow(im_rgb, cmap='gray')

    plt.figure()
    plt.imshow(im1_bw, cmap='gray')
    plt.figure()
    plt.imshow(im2_bw, cmap='gray')
    plt.figure()
    plt.imshow(im3_bw, cmap='gray')