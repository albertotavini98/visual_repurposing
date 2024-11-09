from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os 
import time 
import random


#so it will save results naming them with increasing numbers as dates and hours pass
def save_result(img, folder):
    #this function gets the number of tics since 01/01/1970
    now = int(time.time())
    os.makedirs('results\\'+folder, exist_ok=True)
    out_path = 'results\\'+folder+'\\'+str(now)+'.JPG'
    print('saved ',out_path)
    img.save(out_path)

def get_frame_starters(w, h, l):
    x = int(np.random.rand() * w )
    y = int(np.random.rand() * h)
    x = x if x < w-l else w-l
    y = y if y < h-l else h-l
    
    return x, y

#this fuinction is mmeant to load square pieces from images which are box_dim by box_dim in dimension
def collect_samples(path, num_samples, box_dim):
    fragments = []
    for file in os.listdir(path):
        if '.jpg' or '.JPG' in str(file):
            filename = os.path.join(path,file)
            image = Image.open(filename).convert('RGB')
            array = np.array(image)     
            width, height , channels = array.shape
            for i in range(num_samples):
                x , y = get_frame_starters(width, height, box_dim)
                #check if here it is correct y+box_dim or it should be as it was before x+box_dim ( i had bugs and i blindly fixed it)
                fragment = image.crop((x, y, x+box_dim, y+box_dim))
                fragment = np.array(fragment)
                fragments.append(fragment)
            
                #plt.imshow(fragment)

    print('num of fragments is ', len(fragments))
    return fragments
#this function is meant to load entire images for repurposing
def load_samples(path, resize_width = 0, grayscale=False):
    fragments = []
    for file in os.listdir(path):
        if '.jpg' or '.JPG' in str(file):
            filename = os.path.join(path,file)
            image = Image.open(filename).convert('RGB')
            w, h = image.size
            if resize_width == 0:
                resized = image.resize((int(w/3), int(h/3)), Image.BICUBIC)
            else:
                resized = image.resize((resize_width, int(resize_width*h/w)), Image.BICUBIC)
            if grayscale:
                resized = resized.convert('L')
            array = np.array(resized)
            fragments.append(array)
    print('we have collected samples', len(fragments))
    return fragments

#this function is just to draw the samples in an ordinate way
def plot_samples(fragments):
    l = len(fragments)
    n = int(np.sqrt(l) ) +1
    print('square root is ', n)
    plt.figure(figsize=(n*5,n*7))
    for i , fragment in enumerate(fragments):
        plt.subplot(n, n, i+1)
        plt.imshow(fragment)
        plt.title('fragment '+str(i))

#this function check if we are not in the preserve box of the images and returns true
#added more than one preserve box functioning, in that case we need a list of 4 int lists
def can_we_draw_here(x, y, borders):
    if type(borders[0]) == int:
        l = len(borders)
        if l == 0: return True
        #each of the preserve boxes must have four coordinates
        if l % 4 != 0:
            raise Exception('the borders of the preserve box are not a multiple of four')
        #if we are in one of the boxes that need to be preserved, we return false
        for i in range(0, l, 4):
            if borders[i]< x < borders[i+1] and borders[i+2] < y < borders[i+3]: 
                return False
    elif type(borders[0]) == list:
        for single_border in borders:
            l = len(single_border)
            if l == 0: return True
            #each of the preserve boxes must have four coordinates
            if l % 4 != 0:
                raise Exception('the borders of the preserve box are not a multiple of four')
            #if we are in one of the boxes that need to be preserved, we return false
            for i in range(0, l, 4):
                if single_border[i]< x < single_border[i+1] and single_border[i+2] < y < single_border[i+3]: 
                    return False

    
    return True

#this function is called to place fragments of other images collected through the collect_samples function, 
#so it only works with square images of box_dim by box_dim shape
def repurpose_fragments( fragments,  base, num,  preserve, box_dim, obscure = False, reutilize = False):
    #random.shuffle(fragments)
    width, height, channels = base.shape
    to_use = fragments[:num]
    if reutilize :
        remaining = fragments
    else:
        remaining = fragments[num:]
    for fragment in to_use:
        x, y = get_frame_starters(width, height, box_dim)
    
        for i in range(box_dim-1):
            for j in range(box_dim-1):
                if can_we_draw_here(x+i, y+j, preserve) or obscure:
                    base[x+i][y+j] = 0 if obscure else fragment[i][j]

    new_image = Image.fromarray(base)
    return new_image, remaining
    
#this function is meant to draw entire images on the base image, so it is flexible and allows also images that are not square
def repurpose_images( fragments,  base, num, borders, obscure = False, reutilize = False):
    width, height, channels = base.shape
    #we take the first elements and return the rest
    to_use = fragments[:num]
    if reutilize:
        remaining = fragments
    else:
        remaining = fragments[num:]
    
    for fragment in to_use:
        x_len = fragment.shape[0] -1
        y_len = fragment.shape[1] -1
        #we make it so in puts an image in the upper part and one in the lower part alternatingly
        border = int((x_len + y_len) /2 + width/12)
        x, y = get_frame_starters(width, height, border)
        for i in range(x_len ):
            for j in range(y_len):
                if can_we_draw_here(x+i, y+j, borders) or obscure:
                    #we need to add a check not to go out of border
                    if(x +i < width and y+j < height):
                        
                        base[x+i][y+j] = 0 if obscure else fragment[i][j]

    new_image = Image.fromarray(base)
    return new_image, remaining


def reorder_by_indexes(arr,indexes):
    n = len(arr)
    temp = [0] * n;
 
    for i in range(0,n):
        # element which in the new array is at i is the one that was in the original array at index[i]
        temp[i] = arr[indexes[i]]
 
    return temp

#function that computes for a set of fragments the average on each of the RGB averages and returns them
def get_rgb_averages(fragments, as_list=False):
   
    rgb_averages = None
    if not as_list:
        for frag in fragments:
            width, height, channels = frag.shape
            red = frag[:,:,0]
            green = frag[:,:,1]
            blue = frag[:,:,2]
            red_avg = np.mean(red)
            green_avg = np.mean(green)
            blue_avg = np.mean(blue)
            if rgb_averages is None:
                rgb_averages = np.array([[red_avg, green_avg, blue_avg]])
            else:
                rgb_averages = np.concatenate((rgb_averages,[[red_avg, green_avg, blue_avg]]) , axis =0)
        print('rgb averages is an array of '+str(len(fragments))+' 3 dimensional vectors')
    else:
        rgb_averages = []
        for frag in fragments:
            rgb_averages.append(np.mean(frag, axis=(0, 1)))
    
    return rgb_averages

#a utility function that i don't remember correctly why it does stuff it does and where should it be used, maybe it's usless now
def sort_by_colour_averages(fragments, do_print=False):
    rgb_averages = get_rgb_averages(fragments)

    reds = rgb_averages[:, 0]
    print(reds.shape)
    greens = rgb_averages[:, 1]
    blues = rgb_averages[:, 2]

    red_indexes = np.argsort(reds)[::-1]
    blue_indexes= np.argsort(blues)[::-1]
    green_indexes = np.argsort(greens)[::-1]
    if do_print:
        print('red indexes are \n', red_indexes)
        print('green indexes are \n', green_indexes)
        print('blue indexes are \n', blue_indexes)
    frags_by_red = reorder_by_indexes(fragments, red_indexes)
    frags_by_green = reorder_by_indexes(fragments, green_indexes)
    frags_by_blue = reorder_by_indexes(fragments, blue_indexes)
    return frags_by_red, frags_by_green, frags_by_blue


#function to do clustering based on the RGB averages of the images
def Kmeans_sort_by_RGB_averages(fragments, num_clusters):
    from sklearn.cluster import KMeans

    rgb_averages = get_rgb_averages(fragments)
    # Use KMeans to cluster the images based on the average values
    kmeans = KMeans(n_clusters=num_clusters).fit(rgb_averages)
    X = rgb_averages
    y_pred = kmeans.predict(X)

    # we show the 3d plot of the results of the clustering
    fig = plt.figure(figsize=(14,14))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:,0], X[:,1], X[:,2], c=y_pred, cmap='tab10')
    plt.show()

    #this part of the code sorts the image according to the clustering
    cluster_assignments = kmeans.predict(rgb_averages)
    # Zip the cluster assignments and the original list of images together
    clustered_images = zip(cluster_assignments, fragments)
    # Sort the list of tuples based on the cluster assignment
    sorted_images = sorted(clustered_images, key=lambda x: x[0])
    # Unzip the sorted list of tuples back into a list of images
    _, sorted_collection = zip(*sorted_images)
    cluster_starts = []
    # Iterate over the cluster assignments and find the starting index of each cluster
    current_cluster = sorted_images[0][0]
    cluster_starts.append(0)
    for i, (cluster, _) in enumerate(sorted_images):
        if cluster != current_cluster:
            cluster_starts.append(i)
            current_cluster = cluster
    # Add the index of the last image to the list of cluster starts
    cluster_starts.append(len(sorted_images))

    print('the images are sorted, and the indexes where the clusters start are: ', cluster_starts)
    return sorted_collection, cluster_starts
    