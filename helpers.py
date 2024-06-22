import numpy as np
import random
from numpy import linalg
import matplotlib.pyplot as plt

# Class for representing 2D points
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

def grahams_scan(points):
    # Firstly, sort the point by x-coordinate
    sorted_points = sorted(points)

    # Compute upper convex-hull
    upper_hull = [sorted_points[0], sorted_points[1]]
    
    # Start from the third element
    for i in range(2, len(sorted_points)):
        point_i = sorted_points[i]
        upper_hull.append(point_i)
        
        # While there are at least 3 points in the upper convex-hull and the three last don't define CW turn
        while (len(upper_hull) > 2  and (ccw(upper_hull[-3], upper_hull[-2], upper_hull[-1]) > 0)):
            # Just pop the second-to-last point
            upper_hull.pop(-2)

    # Similarly for the lower convex-hull
    lower_hull = [sorted_points[-1], sorted_points[-2]]

    for i in range(len(sorted_points)-3, 0, -1):
        point_i = sorted_points[i]
        lower_hull.append(point_i)

        while (len(lower_hull) > 2 and ccw(lower_hull[-3], lower_hull[-2], lower_hull[-1]) > 0):
            lower_hull.pop(-2)

    # Remove the first and the last point from the lower convex-hull in order to don't count duplicates with upper
    lower_hull.pop(0)
    lower_hull.pop(-1)

    # The entire convex hull is the concatenation of upper and lower
    entire_hull = upper_hull + lower_hull

    return entire_hull

def gift_wrapping(points):
    # Need of at least three points 
    if len(points) < 3:
        return points
    

    S = points.copy()

    # Keep the origin-vertex which is the leftmost 
    leftmost_vertex = min(S)

    # Current vertex - <r>
    current_vertex_r = leftmost_vertex

    # The result vertex-chain
    vertex_chain = [leftmost_vertex]

    while True:
        # Pick a candidate <u> from set S
        candidate_u = S[0]

        # For each point <t> in S\{u}
        for point_t in S:
            if point_t == candidate_u:
                continue
            
            # If CW(r, u, t) > 0 => CCW(r, u ,t) < 0, skip current candidate and move on. Same for collinear points. (If we want to compute collinear points too, just remove the and-check)
            if ccw(current_vertex_r, candidate_u, point_t) < 0 or (ccw(current_vertex_r, candidate_u, point_t) == 0 and is_internal_point(current_vertex_r, candidate_u, point_t)):
                candidate_u = point_t
        

        # Check if we have returned to the leftmost point
        if candidate_u == leftmost_vertex:
            break
        # If not, update lastest vertex <r>, the output set vertex_chain and remove the vertex founded
        else:
            current_vertex_r = candidate_u
            vertex_chain.append(current_vertex_r)
            S.remove(current_vertex_r)


    return vertex_chain  

if __name__ == "__main__":
    points = [Point2D(1, 7),
            Point2D(2, 14),
            Point2D(3, 21),
            Point2D(-3.5,13),
            Point2D(18, -3),
            Point2D(-2, -10),
            Point2D(-10, 5),
            Point2D(5, 6),
            Point2D(3, 4),
            Point2D(9, 3),
            Point2D(11, 8),
            Point2D(15, -11),
            Point2D(24, -8),
            Point2D(6, 8),
            Point2D(3, 12)]
    
    # is_internal_point(Point2D(), Point2D(), Point2D())

    # grahams_scan(points)
    # print(gift_wrapping(points))
    hull = gift_wrapping(points)


    # Plotting
    x_points = [point.get_x() for point in points]
    y_points = [point.get_y() for point in points]

    # Close the convex hull in order to plot the edges
    hull.append(hull[0])

    hull_x = [point.get_x() for point in hull]
    hull_y = [point.get_y() for point in hull]

    fig, axs = plt.subplots(2, 1, figsize=(8, 12))

    axs[0].scatter(x_points, y_points, color='blue', label='Points')
    axs[0].legend()
    axs[0].grid(True)

    axs[1].scatter(x_points, y_points, color='blue', label='Points')
    axs[1].plot(hull_x, hull_y, color='red', linewidth=2, label='Convex Hull')
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()  # Adjust subplot parameters to give specified padding
    plt.show()

    # new_hull = [Point2D(-10,5), Point2D(-2,-10), Point2D(15,-11), Point2D(24,-8), Point2D(3,21), Point2D(-3.5,13)]
    # new_hull_x = [point.get_x() for point in new_hull]
    # new_hull_y = [point.get_y() for point in new_hull]

    # fig, axs = plt.subplots(2, 1, figsize=(8, 12))
    # axs[0].scatter(x_points, y_points, color='blue', label='Points')
    # axs[0].legend()
    # axs[0].grid(True)

    # axs[1].scatter(new_hull_x, new_hull_y, color='red', label='Hull')
    # axs[1].legend()
    # axs[1].grid(True)

    # plt.tight_layout()  # Adjust subplot parameters to give specified padding
    # plt.show()

    
