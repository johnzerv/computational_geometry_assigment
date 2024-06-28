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

# from shapely.geometry import Polygon
# import matplotlib.pyplot as plt

# # Define the coordinates of the vertices of the two areas
# coords_A = [(0, 0), (4, 0), (4, 4), (0, 4)]
# coords_B = [(1, 1), (1, 2), (2, 2), (2, 1)]

# # Create Polygon objects for the areas
# polygon_A = Polygon(coords_A)
# polygon_B = Polygon(coords_B)

# # Calculate the intersection of the two areas
# intersection = polygon_A.intersection(polygon_B)


# # Print the intersection
# print("Intersection area:", intersection.area)
# print("Intersection coordinates:", list(intersection.exterior.coords) if not intersection.is_empty else "No intersection")

# # Plot the areas and their intersection
# fig, ax = plt.subplots()

# # Plot polygon A
# x_A, y_A = polygon_A.exterior.xy
# ax.fill(x_A, y_A, alpha=0.5, fc='blue', label='Area A')

# # Plot polygon B
# x_B, y_B = polygon_B.exterior.xy
# ax.fill(x_B, y_B, alpha=0.5, fc='green', label='Area B')

# # Plot the intersection if it exists
# if not intersection.is_empty:
#     x_inter, y_inter = intersection.exterior.xy
#     ax.fill(x_inter, y_inter, alpha=0.5, fc='red', label='Intersection')

# # Set plot title and labels
# ax.set_title("Intersection of Two Areas")
# ax.set_xlabel("X coordinate")
# ax.set_ylabel("Y coordinate")
# ax.legend()
# ax.grid(True)

# # Show the plot
# plt.show()
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create a new figure and axis
fig, ax = plt.subplots()

# Define the coordinates for the rectangles
# Rectangle 1: with leftmost x=1, rightmost x=3, lower y=1, upper y=4
left1 = 1
right1 = 3
lower1 = 1
upper1 = 4

# Rectangle 2: with leftmost x=4, rightmost x=7, lower y=2, upper y=3
left2 = 4
right2 = 7
lower2 = 2
upper2 = 3

# Calculate width and height for each rectangle
width1 = right1 - left1
height1 = upper1 - lower1

width2 = right2 - left2
height2 = upper2 - lower2

# Create Rectangle patches
rectangle1 = patches.Rectangle((left1, lower1), width1, height1,
                               fill=True, color='blue', alpha=0.5, edgecolor='black')
rectangle2 = patches.Rectangle((left2, lower2), width2, height2,
                               fill=True, color='green', alpha=0.5, edgecolor='black')

# Add the rectangles to the plot
ax.add_patch(rectangle1)
ax.add_patch(rectangle2)

# Set limits to see the rectangles clearly
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)

# Add labels and title
ax.set_title('Plot with Rectangles')
ax.set_xlabel('x')
ax.set_ylabel('y')

# Show the plot
plt.show()


# 1) Χρειάζεται μια συνάρτηση για να υπολογίζουμε αν ένα σημείο είναι μέσα σε μια έκταση τεσσάρων κορυφών.
# 2) Χρειάζεται μια συνάρτηση που να υπολογίζει την έκταση που ορίζει ενα KD-Υποδέντρο
# 3) Η τελευταία συνάρτηση θα υπολογίζει α. αν όλα τα σημεία της έκτασης του υποδέντρου βρίσκονται 
# μέσα στην έκταση R, β. αν όχι, αν βρίσκεται τουλ. ένα έτσι ώστε να διερευνηθεί περαιτέρω το υποδέντρο 
