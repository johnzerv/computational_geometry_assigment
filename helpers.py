import numpy as np
import random
from numpy import linalg
import matplotlib.pyplot as plt

# Class for representing 2D points
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Nearest points in a clockwise and counter-clockwise direction
        # These references are useful in order to implement the merge method
        # needed by divide and conquer method in linear time. Otherwise
        # each time a neighbor is needed, the elapsed time to find the 
        # clockwise or counter-clockwise nearest neighbor would be O(n)
        self.cw_next = None
        self.ccw_next = None

    # Overwrite __repr__ function in order to print a 2D-Point
    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    # Overwrite compare functions for sorting
    def __eq__(self, point_2D):
        return (self.x == point_2D.x and self.y == point_2D.y)

    def __lt__(self, point_2D):
        return (self.x < point_2D.x) \
            or (self.x == point_2D.x and self.y < point_2D.y)

    def __gt__(self, point_2D):
        return (self.x > point_2D.x) \
            or (self.x == point_2D.x and self.y > point_2D.y)
    # Getters    
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

# Orientation Predicate using determinant
'''
In order to compute the orientation predicate, we must compute the determinant : 
| 1 x0 y0 |
| 1 x1 y1 | = 1*(x1*y2 - y1 * x2) - x0 * (1*y2 - y1 * 1) + y0 * (1*x2 - x1 * 1) = x0 * (y1 - y2) + x1 * (y2 - y0) + x2 * (y0 - y1)  
| 1 x2 y2 |
                                                                                 
'''
def ccw(p0, p1, p2):
    return p0.x * (p1.y - p2.y) + p1.x * (p2.y-p0.y) + p2.x * (p0.y - p1.y)

# Method that generates a list of <N> random 2D points using uniform distribution
def generate_random_2D_points(N):
    random_2D_points = []

    for i in range(N):
        min, max, decimals = 0.0, 50.0, 2
        x = round(random.uniform(min, max), decimals)
        y = round(random.uniform(min, max), decimals)
        new_random_point = Point2D(x, y)
        random_2D_points.append(new_random_point)

    return random_2D_points

# Method to check if the second of the three arguments is internal point of the line segment <xz>
def is_internal_point(x, y, z):
    # Check if y is between x and z on the x-coordinate
    x_between = min(x.x, z.x) <= y.x <= max(x.x, z.x)
    
    # Check if y is between x and z on the y-coordinate
    y_between = min(x.y, z.y) <= y.y <= max(x.y, z.y)

    return x_between and y_between
    
