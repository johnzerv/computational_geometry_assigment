# import helpers
# import matplotlib.pyplot as plt

# points = [helpers.Point2D(1, 7),
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

from scipy.optimize import linprog

'''
Problem : maximize{-3x1 + 12x2} ---> Objective Function

Constraints :  x1 - 2x2 >=1
              2x1 - 3x2 >= 6
              -x1 + 3x2 <= 0
              -x1 + 6x2 <= 12
              4x1 - 9x2 <= 27
               x1, x2   >= 0

In order to solve this problem with SciPy library and linprog method
we need to transfrom it into a minimization problem, because linprog 
solves only minimization problems. We know that: max{f(x)} = -min{-f(x)}
So, the problems comes to:

Problem : minimize{-(-3x1 + 12x2)} = min{3x1 - 12x2} ---> Objective Function

Constraints :  -x1 + 2x2 <= -1
              -2x1 + 3x2 <= -6
              -x1  + 3x2 <=  0
              -x1 + 6x2 <=  12
              4x1 - 9x2 <=  27
               x1, x2   >=  0
'''

# Coefficients for the objective function
c = [3, -12]

# Coefficients for the inequality constraints
A = [
    [-1, 2],
    [-2, 3],
    [-1, 3],
    [-1, 6],
    [4, -9]
]

# Right-hand side values for the inequality constraints
b = [-1,
     -6,
      0,
     12,
     27]

# Variable's bounds
x1_bounds = (0, None)
x2_bounds = (0, None)

# Solve the linear programming problem
res = linprog(c, A_ub=A, b_ub=b, bounds=[x1_bounds, x2_bounds])

# Check if the optimization was successful and print the results
if res.success:
    print("Optimal solution:", res.x)
    print("Optimal value:", -res.fun)  # Convert back to maximization value
else:
    print("Optimization failed:", res.message)
