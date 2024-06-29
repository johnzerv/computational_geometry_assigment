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

    def to_list(self):
        if (self.left == None and self.right == None):
            return [self.point]
        
        return self.left.to_list() + self.right.to_list()

class KDTree:
    def __init__(self, points):
        self.leftmost_x = float('inf')
        self.rightmost_x = float('-inf')
        self.lower_y = float('inf')
        self.upper_y = float('-inf')

        self.root = self.create(None, 0, points)

    def create(self, node, depth, points):
        if len(points) == 1:
            node = KDTreeNode(points[0])
            
            # Update edge x,y coordinates before returning the node
            if (points[0].x < self.leftmost_x):
                self.leftmost_x = points[0].x
            if (points[0].x > self.rightmost_x):
                self.rightmost_x = points[0].x
            if (points[0].y < self.lower_y):
                self.lower_y = points[0].y
            if (points[0].y > self.upper_y):
                self.upper_y = points[0].y

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
    
    # Methods to find the region defined by left or right subtree of a node
    def find_region(self, node=None, prev_region=None, which_child=None, depth=0):
        if (depth == 0):
            return [self.leftmost_x, self.rightmost_x, self.lower_y, self.upper_y]
        
        leftmost, rightmost, lower, upper = prev_region
        
        if (which_child == 'left'):
            if (depth % 2 == 1):
                return [leftmost, node.point.x, lower, upper]
            
            else:
                return [leftmost, rightmost, lower, node.point.y]
            
        elif (which_child == 'right'):
            if (depth % 2 == 1):
                return [node.point.x, rightmost, lower, upper]
            
            else:
                return [leftmost, rightmost, node.point.y, upper]

    def print(self):
        if self is not None:
            self.root.print()



# Example usage
if __name__ == "__main__":
    points = [Point2D(2, 8), Point2D(2, 4), Point2D(3.5, 3), Point2D(3, 5), Point2D(5, 7), Point2D(6, 4.5), Point2D(7, 8), Point2D(8, 7.5), Point2D(8.75, 2.5), Point2D(9.25, 3.5)]
    plot_points(points, [])
    

    kdtree = KDTree(points)

    kdtree.print()

    print(kdtree.leftmost_x)
    print(kdtree.rightmost_x)
    print(kdtree.lower_y)
    print(kdtree.upper_y)

    rec = kdtree.find_region(kdtree.root.left, kdtree.find_region(kdtree.root, kdtree.find_region(), 'left', 1), 'left', 2)

    mypoints = kdtree.root.left.left.to_list()

    print(mypoints)


    plot_points(points, [rec])
