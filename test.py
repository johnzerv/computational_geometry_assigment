import helpers
import matplotlib.pyplot as plt

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
        helpers.Point2D(3, 12),
        helpers.Point2D(-10, -7),
        helpers.Point2D(-10, -8)]

# Plotting
x_points = [point.get_x() for point in points]
y_points = [point.get_y() for point in points]

A, B, C, D = helpers.find_furthest_quadrangle(points)
quandr = [A, B, C, D, A]
xx_points = [point.get_x() for point in quandr]
yy_points = [point.get_y() for point in quandr]



plt.plot(figsize=(8, 12))
# plt.title("Convex Hull with " + title + " Algorithm")

plt.scatter(x_points, y_points, color='blue', label='Points')
plt.scatter(xx_points, yy_points, color='red', label='Quadrangle Points')
plt.plot(xx_points, yy_points, color='red', linewidth=2)
plt.legend()
plt.grid(True)

plt.show()

