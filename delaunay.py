import numpy as np
from scipy.spatial import Delaunay, delaunay_plot_2d
import matplotlib.pyplot as plt
from helpers import create_gif_by_frames
import time

class IncrementalDelaunay:
    def __init__(self, points):
        self.points = points
        
        # Create first triangle
        self.tri = Delaunay(points[:3])
        self.simplices = self.tri.simplices.copy()
        
        # Add point to the Delaunay set of points and compute triangulation
        # for the updated set 
    def add_point(self, point):
        self.points = np.append(self.points, [point], axis=0)
        self.tri = Delaunay(self.points)
        self.simplices = self.tri.simplices.copy()

    def solve(self, new_points):
        for step, point in enumerate(new_points, start=1):
            self.add_point(point)
            frames.append(self.plot(step, init_points, new_points))

    # Method to plot the Delaunay Triangulation of a set of points
    # Returns the file name of the saved plot
    def plot(self, step, init_points, new_points):
        fig, ax = plt.subplots()

        x_points = [point[0] for point in init_points]
        y_points = [point[1] for point in init_points]

        ax.scatter(x_points, y_points, color='blue', label='Points')

        x_points = [point[0] for point in new_points]
        y_points = [point[1] for point in new_points]

        ax.scatter(x_points, y_points, color='blue', label='Points')

        fig = delaunay_plot_2d(delaunay, ax=ax)
        file_name = f"step_{step:03d}.png"
        plt.savefig(file_name)
        plt.close()

        return file_name
    
    


if __name__ == "__main__":

    # Initial set of points (first triangle)
    init_points = np.random.uniform(low=0.0, high=5000.0, size=(3, 2))

    # Initialize the incremental Delaunay triangulation
    delaunay = IncrementalDelaunay(init_points)

    # Frames in order to create a gif
    frames = []

    # Define the number of total points
    N = 50

    # Add points incrementally and for each time compute the Delaunay Triangulation
    # Plot the result too
    new_points = np.random.uniform(low=0.0, high=5000.0, size=(N, 2))

    # First triangle
    frames.append(delaunay.plot(0, init_points, new_points))

    delaunay.solve(new_points)

    create_gif_by_frames('delaunay.gif', frames)


    # Create Delaunay Triangulation using SciPy for different sizes
    sizes = [5, 20,  50, 100, 500]

    for size in sizes:
        points = np.random.uniform(low=0.0, high=5000.0, size=(size, 2))

        start = time.time()
        delaunay = Delaunay(points)
        end = time.time() - start

        fig = delaunay_plot_2d(delaunay)

        plt.title(f"Delaunay with Size : {size} and Elapsed Time : {end:.7f}")
        plt.savefig(f"delaunay_{size}.png")

    big_sizes = [1000, 5000, 20000, 50000, 100000, 500000]
    time_results = []

    for size in big_sizes:
        points = np.random.uniform(low=0.0, high=5000.0, size=(size, 2))

        start = time.time()
        delaunay = Delaunay(points)
        end = time.time() - start

        time_results.append(round(end, 5))

    print('Elapsed time for big sizes in [seconds]')
    for item in zip(big_sizes, time_results):
        print (item)


