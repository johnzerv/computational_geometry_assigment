def classify_points(line_point1, line_point2, points):
    (x1, y1), (x2, y2) = line_point1, line_point2
    right_half_plane = []
    
    for (x, y) in points:
        # Compute the value of the line equation for the point (x, y)
        value = (y2 - y1) * x - (x2 - x1) * y + (x2 * y1 - x1 * y2)
        
        if value >= 0:
            right_half_plane.append((x, y))
    
    return right_half_plane

# Example usage
line_point1 = (-2, -10)
line_point2 = (1, 7)
points = [
    (1,7), (0, 14), (3, 21), (-3 , 13), # These four points form a square
    (18, -3), (-2, -10), (-10, 5), (5,6),
    (3, 4)
]


right_half_plane = classify_points(line_point1, line_point2, points)

print("Points in the right half-plane:", right_half_plane)
