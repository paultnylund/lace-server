def create_grid_boxes_from_image_array(image_array):
    '''
    '''

def find_grid_box_and_bounding_box_overlap(bounding_box, grid_box):
    '''Find area of overlap between a bounding box and grid box (rectangles)

    Args:
        bounding_box: A [[2]] matrix with coordinates for each vertex
        grid_box: A [[2]] matrix with coordinates for each vertex
    
    Returns:
        Returns False if the two boxes from args does not overlap,
        returns the area of overlap otherwise.
    '''

    # Define the index for the upper- and lower bound
    upper_index = 3
    lower_index = 1
    # Define the index for the x- and y-coordinates
    x = 0
    y = 1

    def find_edge_distance(r1_lower, r2_lower, r1_upper, r2_upper):
        '''Find the further most vertex, and calulate the distance of the overlapping edge

        Args:
            r1_lower: A [2] array of coordinates for rectangle 1 lower bound
            r2_lower: A [2] array of coordinates for rectangle 2 lower bound
            r1_upper: A [2] array of coordinates for rectangle 1 upper bound
            r2_upper: A [2] array of coordinates for rectangle 2 upper bound
        
        Returns:
            Returns a possitive value if there is overlap,
            returns a negative value or 0 otherwise
        '''
        return min(r1_upper, r2_upper) - max(r1_lower, r2_lower)
    
    # Find the distance of overlap on the y-axis
    y_distance = find_edge_distance(
        bounding_box[upper_index][y],
        grid_box[upper_index][y],
        bounding_box[lower_index][y],
        grid_box[lower_index][y]
    )

    # Return false if there is no overlap 
    if y_distance <= 0:
        return False
    
    # Find the distance of overalp on the x-axis
    x_distance = find_edge_distance(
        bounding_box[upper_index][x],
        grid_box[upper_index][x],
        bounding_box[lower_index][x],
        grid_box[lower_index][x]
    )

    # Return false if there is no overlap
    if x_distance <= 0:
        return False
    
    # Calculate the area of overlap
    overlap_area = y_distance * x_distance

    return overlap_area

