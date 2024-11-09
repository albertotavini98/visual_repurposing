from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os 
import time 
from itertools import product
import random
import io
from util import blender, pianoforte

    


def fillWithCircles(fig, ax, begin,  side_dim, distance, radius, color):
    """
    Fill a matplotlib figure with circles.

    Parameters:
    - begin: Starting point for the loop in both x and y directions.
    - side_dim: The maximum value for both x and y coordinates.
    - distance: The spacing between circle centers.
    - radius: The radius of the circles.
    - color: The edge color of the circles.
    """

    for i in range( begin, side_dim, distance):
        for j in range(begin, side_dim, distance):
            circle = patches.Circle(( i, j), radius , edgecolor=color, facecolor='none')
            ax.add_patch(circle)

    return fig, ax

def fillWithEllipses(fig, ax, begin, side_dim, width, height, angle, color, fill=False):
    """
    Fill a matplotlib figure with ellipses.

    Parameters:
    
    - begin: Starting point for the loop in both x and y directions.
    - side_dim: The maximum value for both x and y coordinates.
    - width: The width of the ellipses.
    - height: The height of the ellipses.
    - angle: The rotation angle of the ellipses (in degrees).
    - color: The color of the ellipses.
    - fill: Boolean indicating whether to fill the ellipses.

    """
    # Iterate over x-axis with the given width spacing
    for i in range(begin, side_dim, width):
        # Iterate over y-axis with the given height spacing
        for j in range(begin, side_dim, height):
            # Create an ellipse patch at coordinates (i, j)
            ellipse = patches.Ellipse((i, j), width=width, height=height, angle=angle, color=color, fill=fill)
            # Add the ellipse to the provided axis
            ax.add_patch(ellipse)

    # Return the modified figure and axis
    return fig, ax