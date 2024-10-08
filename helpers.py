import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import sqrt
import imageio
import os

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

# Method to check if three points are collinear
def is_collinear(p1, p2, p3):
    return (p3.y - p1.y) * (p2.x - p1.x) == (p2.y - p1.y) * (p3.x - p1.x)

# Method to generate a list of <N> non-collinear random 2D points using uniform distribution
def generate_non_collinear_random_2D_points(N):
    random_2D_points = []
    min_val, max_val, decimals = -50.0, 50.0, 2

    # Generate the first two points
    for _ in range(2):
        x = round(random.uniform(min_val, max_val), decimals)
        y = round(random.uniform(min_val, max_val), decimals)
        random_2D_points.append(Point2D(x, y))

    while len(random_2D_points) < N:
        x = round(random.uniform(min_val, max_val), decimals)
        y = round(random.uniform(min_val, max_val), decimals)
        new_point = Point2D(x, y)
        
        # Check collinearity with all pairs of existing points
        is_new_point_collinear = False
        for i in range(len(random_2D_points) - 1):
            for j in range(i + 1, len(random_2D_points)):
                if is_collinear(random_2D_points[i], random_2D_points[j], new_point):
                    is_new_point_collinear = True
                    break
            if is_new_point_collinear:
                break
        
        if not is_new_point_collinear:
            random_2D_points.append(new_point)

    return random_2D_points

# Method to check if the second of the three arguments is internal point of the line segment <xz>
def is_internal_point(x, y, z):
    # Check if y is between x and z on the x-coordinate
    x_between = min(x.x, z.x) <= y.x <= max(x.x, z.x)
    
    # Check if y is between x and z on the y-coordinate
    y_between = min(x.y, z.y) <= y.y <= max(x.y, z.y)

    return x_between and y_between

# Method to extract the right half plane that
# Exclude points that define the line
def right_half_plane(line_point1, line_point2, points):
    right_half_plane = []
    
    for point in points:
        # Compute orientation-predicate to find if the point is right from line (clockwise) 
        if ccw(line_point1, line_point2, point) < 0:
            right_half_plane.insert(0, point)
            
    return right_half_plane

# Computes the furthest point to the line defined by a couple 2D-points 
def furthest_point_to_line(points, line_point1, line_point2):
    x1 = line_point1.x
    y1 = line_point1.y

    x2 = line_point2.x
    y2 = line_point2.y

    max_distance = -1
    point_of_max_distance = None

    for point in points:
        x0 = point.x
        y0 = point.y

        # Line equation Ax + By + C = 0
        A = y1 - y2
        B = x2 - x1
        C = x1 * y2 - x2 * y1

        # Distance from point to line
        current_distance =  abs(A * x0 + B * y0 + C) / sqrt(A * A + B * B)

        if (current_distance > max_distance):
            max_distance = current_distance
            point_of_max_distance = point

    return point_of_max_distance

# Method to get the quadrangle with the furthest vertexes
def find_furthest_quadrangle(points):
    leftmost_vertex = min(points, key=lambda point: point.x)
    lower_vertex = min(points, key=lambda point:point.y)
    rightmost_vertex = max(points, key=lambda point: point.x)
    upper_vertex = max(points, key=lambda point:point.y)

    return leftmost_vertex, lower_vertex, rightmost_vertex, upper_vertex

# Method to plot 2D-Points and their convex hull
def plot_convex_hull(points, convex_hull_points, title, elapsed_time):
    # Plotting
    x_points = [point.x for point in points]
    y_points = [point.y for point in points]

    # Close the convex hull in order to plot the edges
    convex_hull_points.append(convex_hull_points[0])

    hull_x = [point.x for point in convex_hull_points]
    hull_y = [point.y for point in convex_hull_points]

    fig, axs = plt.subplots(2, 1, figsize=(8, 12))

    plot_title = "Convex Hull with " + title + " Algorithm"
    if (elapsed_time != None):
        plot_title += " and elapsed time " + str(elapsed_time)

    axs[0].scatter(x_points, y_points, color='blue', label='Points')
    axs[0].legend()
    axs[0].grid(True)

    axs[1].scatter(x_points, y_points, color='blue', label='Points')
    axs[1].scatter(hull_x, hull_y, color='red', label='Hull Vertexes')
    axs[1].plot(hull_x, hull_y, color='red', linewidth=2, label='Convex Hull')
    axs[1].legend()
    axs[1].grid(True)

    plt.title(plot_title)
    plt.tight_layout()  # Adjust subplot parameters to give specified padding
    plt.savefig(title + ".png")

# Method for ploting algorithm steps of finding convex hull and saving these frames
def plot_a_frame(points, hull_points, step_name, file_name):
    plt.figure(figsize=(8, 8))
    plt.scatter([point.x for point in points], [point.y for point in points], label='Points')

    if hull_points:
        hull_points.append(hull_points[0])  # To form a closed loop
        plt.plot([point.x for point in hull_points], [point.y for point in hull_points], 'r-', label='Hull')

    plt.title(step_name)
    plt.legend()
    plt.savefig(file_name)
    plt.close()

# Method for creating gif from a set of algorithm steps using imageio library
def create_gif_by_steps(points, steps, output_gif):
    frames = []

    for i, (hull_points, step_name) in enumerate(steps):
        file_name = f"step_{i:03d}.png"
        plot_a_frame(points, hull_points, step_name, file_name)
        frames.append(file_name)
    
    with imageio.get_writer(output_gif, mode='I', duration=0.5) as writer:
        for frame in frames:
            image = imageio.imread(frame)
            writer.append_data(image)
    
    # Clean up frames
    for frame in frames:
        os.remove(frame)

def create_gif_by_frames(output_gif, frames):
    with imageio.get_writer(output_gif, mode='I', duration=0.5) as writer:
        for frame in frames:
            image = imageio.imread(frame)
            writer.append_data(image)
    
    # # Clean up frames
    for frame in frames:
        os.remove(frame)

def median_point(points, by='x'):
    size = len(points)

    if (by == 'x'):
        sorted_points = sorted(points, key=lambda point: point.x)
    elif (by == 'y'):
        sorted_points = sorted(points, key=lambda point:point.y)

    if size % 2 == 1:
        return sorted_points[size // 2] # ceil(size/2)
    else:
        return sorted_points[size // 2 - 1]
    
def separate_to_subsets(points, median, by='x'):
    min_subset = []
    max_subset = []

    if (by == 'x'):
        for point in points:
            if (point.x <= median.x):
                min_subset.append(point)
            else:
                max_subset.append(point)

    elif (by == 'y'):
        for point in points:
            if (point.y <= median.y):
                min_subset.append(point)
            else:
                max_subset.append(point)

    return min_subset, max_subset

# Function to plot 2D points
def plot_points(points, rectangles, rec_color='gray'):
    # Extract x and y coordinates from the points
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]

    # Create the plot
    _, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x_coords, y_coords, color='blue', marker='o')

    # Add rectangles to the plot
    for rect in rectangles:
        left, right, lower, upper = rect
        width = right - left
        height = upper - lower
        rectangle = patches.Rectangle((left, lower), width, height,
                                      fill=True, color=rec_color, alpha=0.5)
        ax.add_patch(rectangle)

    # Add title and labels
    ax.set_title('Points with Rectangles')
    ax.set_xlabel('X-coordinate')
    ax.set_ylabel('Y-coordinate')

    # Display the plot
    plt.grid(True)
    plt.show()

# Method to check if a point is inside a specific rectangle region
def is_point_in_rectangle(point, rec):
    left, right, lower, upper = rec

    if (point.x >= left and point.x <= right and point.y >= lower and point.y <= upper):
        return True
    
    return False

# Method to check if given two rectangles, the first is subrectangle of second
def is_sub_rectangle(rec, target_rec):
    left1, right1, lower1, upper1 = rec
    left2, right2, lower2, upper2 = target_rec

    if (left1 >= left2 and right1 <= right2 and lower1 >= lower2 and upper1 <= upper2):
        return True
    
    return False

# Method to check if the intersection of two rectangles is empty or not
def is_rectangles_intersection_non_empty(rec, target_rec):
    left1, right1, lower1, upper1 = rec
    left2, right2, lower2, upper2 = target_rec

    # Check if one rectangle is to the left of the other
    if right1 < left2 or right2 < left1:
        return False
    
    # Check if one rectangle is above the other
    if upper1 < lower2 or upper2 < lower1:
        return False
    
    return True
