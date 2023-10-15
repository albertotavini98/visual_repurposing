from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os 
import time
import random
from util import blender

def get_frame_starters(w, h, l):
    x = random.randint(0,  w -l )
    y = random.randint(0,  h - l)
    
    return x, y

def collect_samples(image, box_dim, num_samples):
    fragments = []
    array = np.array(image)
    
    height , width,  channels = array.shape
    print('height is {} while width is {}'.format(height, width))
    for i in range(num_samples):
            x , y = get_frame_starters(width, height, box_dim)
            #print('x is {} while y is {}'.format(x, y))
            
            fragment = image.crop((x, y, x+box_dim, y+box_dim))
            fragment = np.array(fragment)
            fragments.append(fragment)
            
            plt.imshow(fragment)
    print('num of fragments is', len(fragments))
    return fragments

def repurpose(base, fragments, box_dim, preserve_box, obscure = False):
    width, height , channels = base.shape
    for fragment in fragments:
        x, y = get_frame_starters(width, height, box_dim)
    
        for i in range(box_dim-1):
            for j in range(box_dim-1):
                if blender.can_we_draw_here(x+i, y+j, preserve_box) or obscure:
                    base[x+i][y+j] = 0 if obscure else fragment[i][j]

    new_image = Image.fromarray(base)
    
    return new_image


def save_result(img, folder):
    now = int(time.time())
    os.makedirs('results\\'+folder, exist_ok=True)
    out_path = 'results\\'+folder+'\\'+str(now)+'.JPG'
    print('saved ',out_path)
    img.save(out_path)