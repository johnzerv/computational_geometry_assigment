import numpy as np
import random
from numpy import linalg
import matplotlib.pyplot as plt
import helpers as helpers
from math import sqrt


def grahams_scan(points):
    # Need of at least three points 
    if len(points) < 3:
        return points
    
    # Firstly, sort the point by x-coordinate
    sorted_points = sorted(points)

    # Compute upper convex-hull
    upper_hull = [sorted_points[0], sorted_points[1]]
    
    # Start from the third element
    for i in range(2, len(sorted_points)):
        point_i = sorted_points[i]
        upper_hull.append(point_i)
        
        # While there are at least 3 points in the upper convex-hull and the three last don't define CW turn
        while (len(upper_hull) > 2  and (helpers.ccw(upper_hull[-3], upper_hull[-2], upper_hull[-1]) > 0)):
            # Just pop the second-to-last point
            upper_hull.pop(-2)

    # Similarly for the lower convex-hull
    lower_hull = [sorted_points[-1], sorted_points[-2]]

    for i in range(len(sorted_points)-3, 0, -1):
        point_i = sorted_points[i]
        lower_hull.append(point_i)

        while (len(lower_hull) > 2 and helpers.ccw(lower_hull[-3], lower_hull[-2], lower_hull[-1]) > 0):
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
            
            # If CW(r, u, t) > 0 => helpers.CCW(r, u ,t) < 0, skip current candidate and move on. Same for collinear points. (If we want to compute collinear points too, just remove the and-check)
            if helpers.ccw(current_vertex_r, candidate_u, point_t) < 0 or (helpers.ccw(current_vertex_r, candidate_u, point_t) == 0 and helpers.is_internal_point(current_vertex_r, candidate_u, point_t)):
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

def divide_and_conquer_helper(points):
    # Base Case
    if len(points) == 1:
        return points
    
    median = int(len(points)/2)    

    left_points = points[0:median]
    right_points = points[median:]

    left_hull = divide_and_conquer_helper(left_points)
    right_hull = divide_and_conquer_helper(right_points)

    return convex_hulls_merge(left_hull, right_hull)

def divide_and_conquer(points):
    # Need of at least three points
    if (len(points) < 3):
        return points
    
    return divide_and_conquer_helper(sorted(points))

def convex_hulls_merge(A_hull, B_hull):
    A = max(A_hull) # Rightmost point of left hull
    B = min(B_hull) # Leftmost point of right hull

    # Make copies for both of these points
    A_copy = A
    B_copy = B

    # Find the upper bridge
    while True:
        prev_A = A
        prev_B = B

        # Find the vertex that belongs to right convex hull and to the final upper bridge
        if B.cw_next:
            # Move B clockwise as long as it makes a left turn
            while helpers.ccw(A, B, B.cw_next) > 0:
                B = B.cw_next

        # Find the vertex that belongs to left convex hull and to the final upper bridge
        if A.ccw_next:
            # Move p counterclockwise as long as it makes a right turn
            while helpers.ccw(B, A, A.ccw_next) < 0:
                A = A.ccw_next

        if A == prev_A and B == prev_B:
            break

    # Similarly for the lower bridge
    while True:
        prev_A = A_copy
        prev_B = B_copy

        if B_copy.ccw_next:
            # Move q counterlockwise as long as it makes a right turn
            while helpers.ccw(A_copy, B_copy, B_copy.ccw_next) < 0:
                B_copy = B_copy.ccw_next

        if A_copy.cw_next:
            # Move p clockwise as long as it makes a left turn
            while helpers.ccw(B_copy, A_copy, A_copy.cw_next) > 0:
                A_copy = A_copy.cw_next

        if A_copy == prev_A and B_copy == prev_B:
            break

    # Remove all other intermediate points
    A.cw_next = B
    B.ccw_next = A

    A_copy.ccw_next = B_copy
    B_copy.cw_next = A_copy

    # Construct the final merged hall
    result = []
    start = A

    while True:
        result.append(A)
        A = A.ccw_next

        if A == start:
            break

    return result

# Method to get the quadrangle with the furthest vertexes
def find_furthest_quadrangle(points):
    leftmost_vertex = min(points, key=lambda point: point.x)
    lower_vertex = min(points, key=lambda point:point.y)
    rightmost_vertex = max(points, key=lambda point: point.x)
    upper_vertex = max(points, key=lambda point:point.y)

    return leftmost_vertex, lower_vertex, rightmost_vertex, upper_vertex

# Method to extract the right half plane that
# Exclude points that define the line
def right_half_plane(line_point1, line_point2, points):
    right_half_plane = []
    
    for point in points:
        # Compute orientation-predicate to find if the point is right from line (clockwise) 
        if helpers.ccw(line_point1, line_point2, point) < 0:
            right_half_plane.insert(0, point)
            
    return right_half_plane

# Computes the furthest point to the line defined by a couple 2D-points 
def furthest_point_to_line(points, line_point1, line_point2):
    x1 = line_point1.get_x()
    y1 = line_point1.get_y()

    x2 = line_point2.get_x()
    y2 = line_point2.get_y()

    max_distance = -1
    point_of_max_distance = None

    for point in points:
        x0 = point.get_x()
        y0 = point.get_y()

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

# Recursive method to compute extra convex-hull vertexes from the quadrangle with the furthest vertexes
def quick_hull_helper(A, B, points):
    # Firstly compute the right half plane defined by the line of 2D-points A,B
    right_h_plane = right_half_plane(A, B, points)

    if (right_h_plane == []):
        return []

    # Compute the new convex-hull vertex which is the furthest point to the line defined by A,B
    C = furthest_point_to_line(right_h_plane, A, B)

    # Compute extra vertexes for the two new lines defined by AC and CB and add it to new vertex C
    return quick_hull_helper(A, C, points) + [C] + quick_hull_helper(C, B, points)

def quick_hull(points):
    # Need of at three points
    if (len(points) < 3):
        return points
    
    # Compute the four edge vertexes
    leftmost, lower, rightmost, upper = find_furthest_quadrangle(points)

    # Return computed vertexes and extra vertexes for each space defined by the half planes of the above 2D-points
    return [leftmost] + quick_hull_helper(leftmost, lower, points) + [lower] +\
           quick_hull_helper(lower, rightmost, points) + [rightmost] + quick_hull_helper(rightmost, upper, points) +\
           [upper] + quick_hull_helper(upper, leftmost, points)

# Method to plot 2D-Points and their convex hull
def plot_convex_hull(points, convex_hull_points):
    # Plotting
    x_points = [point.get_x() for point in points]
    y_points = [point.get_y() for point in points]

    # Close the convex hull in order to plot the edges
    convex_hull_points.append(convex_hull_points[0])

    hull_x = [point.get_x() for point in convex_hull_points]
    hull_y = [point.get_y() for point in convex_hull_points]

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



if __name__ == "__main__":
    points = [helpers.Point2D(1, 7),
            helpers.Point2D(0, 14),
            helpers.Point2D(3, 21),
            helpers.Point2D(-3.5,13),
            helpers.Point2D(18, -3),
            helpers.Point2D(-2, -10),
            helpers.Point2D(-10, 5),
            helpers.Point2D(5, 6),
            helpers.Point2D(3, 4),
            helpers.Point2D(15,15),
            helpers.Point2D(9, 3),
            helpers.Point2D(11, 8),
            helpers.Point2D(15, -11),
            helpers.Point2D(24, -8),
            helpers.Point2D(6, 8),
            helpers.Point2D(3, 12)]
    
    # is_internal_point(helpers.Point2D(), helpers.Point2D(), helpers.Point2D())

    grahams_scan_hull = grahams_scan(points)
    gift_wrapping_hull = gift_wrapping(points)
    divide_and_conquer_hull = divide_and_conquer(points)
    quickhull_hull = quick_hull(points)
    plot_convex_hull(points, grahams_scan_hull)
    plot_convex_hull(points, gift_wrapping_hull)
    plot_convex_hull(points, divide_and_conquer_hull)
    plot_convex_hull(points, quickhull_hull)


    # new_hull = [helpers.Point2D(-2, -10), helpers.Point2D(1, 7)]
    # new_hull_x = [point.get_x() for point in new_hull]
    # new_hull_y = [point.get_y() for point in new_hull]

    # fig, axs = plt.subplots(2, 1, figsize=(8, 12))
    # axs[0].scatter(x_points, y_points, color='blue', label='Points')
    # axs[0].legend()
    # axs[0].grid(True)

    # axs[1].scatter(x_points, y_points, color='blue', label='Hull')
    # axs[1].plot(new_hull_x, new_hull_y, color='red', linewidth=2, label='Convex Hull')
    # axs[1].legend()
    # axs[1].grid(True)

    # plt.tight_layout()  # Adjust subplot parameters to give specified padding
    # plt.show()

    # print(hull)
