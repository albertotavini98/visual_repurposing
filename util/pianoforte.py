from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os 
import time 
import random
from util import blender

def cluster_indexes_initializer(l, n):
    array = [i*n for i in range(l)] + [l*n]
    return array

def divide_in_subcollections(collection, num_collections, cluster_dims):
    #this function can be used to divide a collection in subcollections, it will also given the indexes of the initial clusters
    #correctly initialized
    cluster_indexes = []
    collections = []
    if (len(collection) % num_collections != 0):
        raise Exception('division is not exact!')
    num = len(collection) // num_collections
    for i in range(num_collections):
        cluster_indexes.append(cluster_indexes_initializer(num, cluster_dims ))
        collections.append(collection[i*num : (i+1)*num])
    return collections, cluster_indexes


def pick_cluster_ranges(cluster_indexes, p):
        #this function takes as input a list of indexes that indicates where a cluster begins and ends in a collection of images
        #and returns randomly extracted clusters as the set of their begin and ends
        num_clusters = len(cluster_indexes) -1
        active_clusters = []
        extraction = np.random.rand()
        first = np.ceil(extraction*num_clusters)
        active_clusters.append(int(first))
        while(extraction < p):
            extraction = np.random.rand()
            other = np.ceil(extraction*num_clusters)
            if other not in active_clusters: active_clusters.append(int(other))
            if len(active_clusters) == num_clusters:
                break
        ranges = []
        for n in active_clusters:
            ranges.append([cluster_indexes[n-1], cluster_indexes[n]])
        return ranges
        

def compose_visual_melody( num_generations, cluster_indexes, p1, p2):
    #given indexes indicating where clusters of a set of images begin and end, this function will return a num_generations long list of masks indicating which of the images
    #will be activated as notes in each generation.
    #it will randomly choose one or more clusters and activate only certain images among those clusters
    #p1 is the probability we include other clusters, p2 is the one for which each image in selected clusters will be activated
    masks = []
    for i in range(num_generations):
        ranges = pick_cluster_ranges( cluster_indexes, p1)
        mask =np.zeros(cluster_indexes[-1])
        print('we used the ranges', sorted(ranges))
        for couple in ranges:
            start = couple[0]
            end = couple[1]
            for j in range(start, end):
                mask[j] = np.random.binomial(1, p2, 1)
        
        masks.append(mask)
    return masks
                
def find_largest_factors(n, vertical=True):
    max_factor1 = 0
    max_factor2 = 0
    for i in range(1, int(np.sqrt(n)) + 1 ):
        if n % i == 0:
                max_factor1 = i
                max_factor2 = n//i
    if vertical:
        return max_factor1, max_factor2
    else:
        return max_factor2, max_factor1

def fill_this_box(array, fragment, row, col, w, h):
    res = array
    b1 = row*h
    b2= col*w
    for i in range(0, h):
        for j in range(0, w):
            if b1+i <res.shape[0] and b2+j <res.shape[1] and i<fragment.shape[0] and j<fragment.shape[1]:
                res[b1+i][b2+j]= fragment[i][j]
            else:
                break
    return res


def play_and_repurpose(fragments, masks, path, factors = None, vertical = True ):
    #we chose the maximum size if there are different shapes
    width = height = 0
    for fragment in fragments:
        if(fragment.shape[0] >width) :
            height =width= fragment.shape[0]
        if(fragment.shape[1] > height):
            width= fragment.shape[1]
    print('maximum height is {} and max width is {}'.format(height, width))
    
    if factors:
        f1, f2 = factors[0], factors[1]
    else: 
        f1, f2 = find_largest_factors(len(fragments), vertical)
    #we generate a background that can contain all of the images in an ordered manner
    print("we explore {} on height and {} on width".format(f2, f1))
    background = Image.new("RGB", (f1*width, f2*height  ), (0, 0, 0))
    print('we use a background that will be {} wide and {} high'.format(f1*width, f2*height))
    b_arr = np.array(background)
    print('background shape is', b_arr.shape)
    
    for mask in masks:
        b_arr = np.array(background)
        for i in range(0, f2):
            for j in range(0, f1):
                #if that box needs to be activated, we fill it
                index = f1*i+j
                if index < len(mask):
                    if mask[index] == 1: 
                        b_arr = fill_this_box(b_arr, fragments[index],  i , j, width, height)
                        
        image = Image.fromarray(b_arr)
        blender.save_result(image, path)

        