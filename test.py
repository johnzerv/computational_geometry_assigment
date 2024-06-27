# import helpers
# import matplotlib.pyplot as plt

# points = [helpers.helpers.Point2D(1, 7),
#         helpers.Point2D(0, 14),
#         helpers.Point2D(3, 21),
#         helpers.Point2D(-3.5,13),
#         helpers.Point2D(18, -3),
#         helpers.Point2D(-2, -10),
#         helpers.Point2D(-10, 5),
#         helpers.Point2D(5, 6),
#         helpers.Point2D(3, 4),
#         helpers.Point2D(15,15),
#         helpers.Point2D(9, 3),
#         helpers.Point2D(11, 8),
#         helpers.Point2D(15, -11),
#         helpers.Point2D(24, -8),
#         helpers.Point2D(6, 8),
#         helpers.Point2D(3, 12),
#         helpers.Point2D(-10, -7),
#         helpers.Point2D(-10, -8)]

# # Plotting
# x_points = [point.get_x() for point in points]
# y_points = [point.get_y() for point in points]

# A, B, C, D = helpers.find_furthest_quadrangle(points)
# quandr = [A, B, C, D, A]
# xx_points = [point.get_x() for point in quandr]
# yy_points = [point.get_y() for point in quandr]



# plt.plot(figsize=(8, 12))
# # plt.title("Convex Hull with " + title + " Algorithm")

# plt.scatter(x_points, y_points, color='blue', label='Points')
# plt.scatter(xx_points, yy_points, color='red', label='Quadrangle Points')
# plt.plot(xx_points, yy_points, color='red', linewidth=2)
# plt.legend()
# plt.grid(True)

# plt.show()

import matplotlib.pyplot as plt
import helpers
import kd_tree

# Function to plot 2D points
def plot_points(points):
    # Extract x and y coordinates from the points
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]

    # Create the plot
    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, color='blue', marker='o')

    # Add title and labels
    plt.title('2D Points Plot')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')

    # Display the plot
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    points = [helpers.Point2D(2, 8), helpers.Point2D(2, 4), helpers.Point2D(3.5, 3), helpers.Point2D(3, 5), helpers.Point2D(5, 7), helpers.Point2D(6, 4.5), helpers.Point2D(7, 8), helpers.Point2D(8, 7.5), helpers.Point2D(8.75, 2.5), helpers.Point2D(9.25, 3.5)]
    plot_points(points)

    kdtree = kd_tree.KDTree(points)

    kdtree.print()