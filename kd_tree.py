from helpers import Point2D, median_point, separate_to_subsets, plot_points

class KDTreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.point = key

    # Pretty print for KD-Trees
    def print(self, indent="", last=True):
        if self.right:
            self.right.print(indent + ("│   " if last else "    "), False)
        
        print(indent + ("└── " if last else "┌── ") + str(self.point))
        
        if self.left:
            self.left.print(indent + ("    " if last else "│   "), True)

class KDTree:
    def __init__(self, points):
        self.root = self.create(None, 0, points)

    def create(self, node, depth, points):
        if len(points) == 1:
            node = KDTreeNode(points[0])

            return node
        
        # If depth is even, use a horizontal line to separate the points
        if depth % 2 == 0:
            med_point = median_point(points, by='x')

            min_subset, max_subset = separate_to_subsets(points, med_point, by='x')
                    
        # Else if depth is odd, use a vertical line to separate the points
        else:
            med_point = median_point(points, by='y')

            min_subset, max_subset = separate_to_subsets(points, med_point, by='y')

        node = KDTreeNode(med_point)
        node.left = self.create(node.left, depth+1, min_subset)
        node.right = self.create(node.right, depth+1, max_subset)

        return node
    
    def print(self):
        if self is not None:
            self.root.print()




# Example usage
if __name__ == "__main__":
    points = [Point2D(2, 8), Point2D(2, 4), Point2D(3.5, 3), Point2D(3, 5), Point2D(5, 7), Point2D(6, 4.5), Point2D(7, 8), Point2D(8, 7.5), Point2D(8.75, 2.5), Point2D(9.25, 3.5)]
    plot_points(points)

    kdtree = KDTree(points)

    kdtree.print()
