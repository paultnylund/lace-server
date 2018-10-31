from Stack import Stack
import numpy

array = numpy.array([0, 0.5, 1])
reverse_array = numpy.flipud(array).tolist()
stack = Stack(reverse_array)

row = 0
column = 0

# WORKS FOR ONE BOX
def test():
    if stack.isEmpty():
        return False

    current_value = stack.pop()
    peek_value = stack.peek()
    grid_box_coordinates = []
    row = 0
    column = 0

    while column < 1:
        grid_box_coordinates = [
            [current_value, row],
            [peek_value, row],
            [peek_value, row + peek_value],
            [current_value, row + peek_value]
        ]

        column = column + peek_value
    
    return grid_box_coordinates

def create_single_grid_box(row, column):
    if stack.isEmpty():
        return False
    
    current_value = stack.pop()
    peek_value = stack.peek()
    grid_box_coordinates = []

    while column < 1:
        grid_box_coordinates = [
            [current_value, row],
            [peek_value, row],
            [peek_value, row + peek_value],
            [current_value, row + peek_value]
        ]

        column = column + peek_value

    return grid_box_coordinates


# for each in stack.size():
#     print(create_single_grid_box(row, column))

def create_grid_boxes_array():
    '''
    '''
    # Split up the normalised coordinates in 50 intervals for grid edges
    normalised_coordinates = numpy.linspace(0, 1, 50)

    # Reverse the numpy array and turn it into a python list
    reversed_stack_array = numpy.flipud(normalised_coordinates).tolist()

    # Create a stack with the normalised coordinates 
    stack = Stack(reversed_stack_array)

    row = 0
    column = 0

    # If the stack is empty, return the 
    if stack.isEmpty():
        return False
    
    for each in range(0, stack.size()):
        print(create_single_grid_box(row, column))
        row = stack.peek()
    
create_grid_boxes_array()

def find_grid_box_and_bounding_box_overlap(bounding_box, grid_box):
    '''Find area of overlap between a bounding box and grid box (rectangle, square)

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

