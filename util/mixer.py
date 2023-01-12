from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os 
import time

def get_frame_starters(w, h, l):
    x = int(np.random.rand() * w )
    y = int(np.random.rand() * h)
    x = x if x < w-l else w-l
    y = y if y < h-l else h-l
    
    return x, y

def collect_samples(image, box_dim, num_samples):
    fragments = []
    array = np.array(image)
    width, height , channels = array.shape
    for i in range(num_samples):
            x , y = get_frame_starters(width, height, box_dim)
            #print(x, y)
            
            fragment = image.crop((x, x, x+box_dim, x+box_dim))
            fragment = np.array(fragment)
            fragments.append(fragment)
            
            plt.imshow(fragment)
    print('num of fragments is', len(fragments))
    return fragments

def repurpose(base, fragments, box_dim, obscure = False):
    width, height , channels = base.shape
    for fragment in fragments:
        x, y = get_frame_starters(width, height, box_dim)
    
        for i in range(box_dim-1):
            for j in range(box_dim-1):
                base[x+i][y+j] = 0 if obscure else fragment[i][j]

    new_image = Image.fromarray(base)
    
    return new_image


def save_result(img, folder):
    now = int(time.time())
    os.makedirs('results\\'+folder, exist_ok=True)
    out_path = 'results\\'+folder+'\\'+str(now)+'.JPG'
    print('saved ',out_path)
    img.save(out_path)