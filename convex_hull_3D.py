import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Generate 85 random points in 3D using uniform distribution, range ---> (-25.00, 25.00)
points = np.random.uniform(low=-25.00, high=25.00, size=(85, 3))

# Compute the convex hull
hull = ConvexHull(points)

# Create a figure with two subplots
fig = plt.figure(figsize=(12, 6))

# First subplot: Only points
ax1 = fig.add_subplot(121, projection='3d')

# Scatter the points
ax1.scatter(points[:,0], points[:,1], points[:,2], 'o')

# Labels and Title
ax1.set_xlabel('X', fontsize=12, fontweight='bold')
ax1.set_ylabel('Y', fontsize=12, fontweight='bold')
ax1.set_zlabel('Z', fontsize=12, fontweight='bold')
ax1.set_title('3D Points Only', fontsize=14, fontweight='bold')

# Second subplot: Convex hull with points
ax2 = fig.add_subplot(122, projection='3d')

# Scatter the points
ax2.scatter(points[:,0], points[:,1], points[:,2], 'o')\

# Add faces of convex hull
for simplex in hull.simplices:
    tri = Poly3DCollection([points[simplex]], alpha=0.5, edgecolor='k')
    ax2.add_collection3d(tri)

# Labels and Title
ax2.set_xlabel('X', fontsize=12, fontweight='bold')
ax2.set_ylabel('Y', fontsize=12, fontweight='bold')
ax2.set_zlabel('Z', fontsize=12, fontweight='bold')
ax2.set_title('3D Convex Hull with Points', fontsize=14, fontweight='bold')

plt.savefig('QuickHull_3D_85.png')
plt.show()