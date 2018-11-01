from Stack import Stack
import numpy
from enum import Enum

class Density(Enum):
    FREE = 0
    LIGHT = 1
    MEDIUM = 2
    HEAVY = 3
    NULL = 4

# def load_image_into_numpy_array(image):
#     '''Loads image into a numpy array

#     This helper function is used to load an image into a numpy array
#     which can then be used for further processing.

#     Args:
#         image: a PIL.Image object.

#     Returns:
#         A uint8 numpy array representation of the image
#     '''
#     # Get the with and height of the image
#     (image_width, image_height) = image.size

#     # Return a numpy array representation of the image as uint8
#     return numpy.array(image.getdata()).reshape((image_height, image_width, 3)).astype(numpy.uint8)

def create_single_grid_box(stack, row, column):
    '''Create a [4*[4]] python list with the grid box coordinates

    Args:
        stack: The Stack Object with the coordinates intervals
        row: The mutable row iterator
        column The mutable colunn iterator
    
    Returns:
        Returns a [4*[4]] tuple with the grid box coordinates
    '''
    # Return false if the stack is empty
    if stack.isEmpty():
        return False
    
    # Pop the first value of the stack
    current_value = stack.pop()

    # Get the next peek value
    peek_value = stack.peek()

    # Initialise the list tuple for grid box verticies
    grid_box_coordinates = []

    # Fill out the coordinates for the grid box vertecies
    grid_box_coordinates = [
        [current_value, row[0]],
        [peek_value, row[0]],
        [peek_value, (row[0] + peek_value) - current_value],
        [current_value, (row[0] + peek_value) - current_value]
    ]

    # Add the next value in the stack to the column iterator
    column[0] = peek_value

    # Return the coordinates list for the grid box
    return grid_box_coordinates

def create_grid_boxes_array(size=5):
    '''Create a [size*[size]] python list with entire grid

    Args:
        size: (int) The size of the grid - number of grids will be (size - 1)^2
    
    Returns:
        Returns a [size*[size]] tuple with the grid
    '''
    # Initialise a list for the grid
    grid_boxes = []

    # Split up the normalised coordinates in 50 intervals for grid edges
    normalised_coordinates = numpy.linspace(0, 1, size)

    # Reverse the numpy array and turn it into a python list
    reversed_stack_array = numpy.flipud(normalised_coordinates).tolist()

    # Create a stack with the normalised coordinates 
    stack = Stack(reversed_stack_array)

    # Initialise mutable iterators
    row = [0.0]
    column = [0.0]

    # If the stack is empty, return the 
    if stack.isEmpty():
        return False
    while row[0] < 1.0:
        while column[0] < 1.0:
            grid_boxes.append(create_single_grid_box(stack, row, column))
        # Reset the stack to the original input
        reversed_stack_array = numpy.flipud(normalised_coordinates).tolist()
        stack.reset(reversed_stack_array)
        # Reset the column iterator
        column[0] = 0.0
        # Add the next peak to the row iterator
        row[0] = row[0] + stack.next_peek()
    
    # Return the grid list
    return grid_boxes

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
    upper_index = 1
    lower_index = 3
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
        bounding_box[lower_index][x],
        grid_box[lower_index][x],
        bounding_box[upper_index][x],
        grid_box[upper_index][x]
    )

    # Return false if there is no overlap
    if x_distance <= 0:
        return False
    
    # Calculate the area of overlap
    overlap_area = y_distance * x_distance

    return overlap_area

def calculate_overlay_areas(grid_boxes, bounding_boxes):
    # Instasiate the overlay areas graph
    overlay_areas_graph = []

    # Calculate overlay area of all grid boxes and store in new array (loop)
    for grid_box in grid_boxes:
        for bounding_box in bounding_boxes:
            overlay_area = find_grid_box_and_bounding_box_overlap(bounding_box, grid_box)
            # If the is no overlay area append a zero, else append overlay area
            if overlay_area == False:
                overlay_areas_graph.append(0.0)
            else:
                overlay_areas_graph.append(overlay_area)

    # Return new array with overlay areas
    return overlay_areas_graph

def map_overlap_area_to_density(overlay_graph):
    '''
    '''
    density_graph = []
    # Find the largest area in overlay array
    max_area = overlay_graph[numpy.argmax(overlay_graph)]
    min_area = overlay_graph[numpy.argmin(overlay_graph)]

    def linear_transform_ranges(value):
        transformed_value = ((value - min_area) / (max_area - min_area)) * (Density.HEAVY.value - Density.LIGHT.value) + Density.LIGHT.value
        return transformed_value

    # Map all overlay areas into density range
    for area in overlay_graph:
        if area == 0.0:
            density_graph.append(Density.FREE.value)
        else:
            density_graph.append(linear_transform_ranges(area))

    # Return density values in new density array
    return density_graph

def convert_density_array_to_json_object(density_graph):
    # Convert density array to json object
    test = 1

    # Return the new density graph

def create_density_grid(bounding_boxes):
    '''
    '''
    # Define density range [0:4] - 4 being imposible to move as inanimate object is present
    # This comes from the Density enum class

    # The initial generated grid with (n - 1)^2 grid boxes
    grid_boxes = create_grid_boxes_array(3)

    # Calculate overlay area of all grid boxes and store in new array
    overlay_graph = calculate_overlay_areas(grid_boxes, bounding_boxes)
    print(overlay_graph)

    # Find the largest area in overlay array
    # Map all overlay areas into density range
    density_graph = map_overlap_area_to_density(overlay_graph)
    print(density_graph)

    # Convert density array to json object
    density_graph_json = convert_density_array_to_json_object(density_graph)

    # Return json density array to NodeJS
    return density_graph_json
    