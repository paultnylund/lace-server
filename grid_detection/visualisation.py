import numpy
import sys
from matplotlib import pyplot
from PIL import Image, ImageDraw

def load_image_into_numpy_array(image):
    '''Loads image into a numpy array

    This helper function is used to load an image into a numpy array
    which can then be used for further processing.

    Args:
        image: a PIL.Image object.

    Returns:
        A uint8 numpy array representation of the image
    '''
    # Get the with and height of the image
    (image_width, image_height) = image.size

    # Return a numpy array representation of the image as uint8
    return numpy.array(image.getdata()).reshape((image_height, image_width, 3)).astype(numpy.uint8)

def draw_box_on_image(image, box_coords, color, thickness=2):
    '''Draw single grid box on image
    '''
    # Create an PIL Image from the numpy array image
    image_pil = Image.fromarray(numpy.uint8(image)).convert('RGB')

    # Create an object that can be used to draw in the given image
    draw = ImageDraw.Draw(image_pil)

    # Get the width and height of the image
    image_width, image_height = image_pil.size

    # Set the oposite vertecies of the box coords to the non-normalised coordinates
    min_coords = (box_coords[0][0] * image_width, box_coords[0][1] * image_height)
    max_coords = (box_coords[2][0] * image_width, box_coords[2][1] * image_height)

    # Draw the grid box
    draw.rectangle([min_coords, max_coords], width=thickness, outline=color)

    # Copy the values from the drawn image into the original image array
    numpy.copyto(image, numpy.array(image_pil))

def draw_grid_on_image_array(image, grid_boxes, color='red', thickness=2):
    '''Draw the grid on image
    '''
    for grid_box in grid_boxes:
        draw_box_on_image(image, grid_box, color)

def draw_bounding_boxes_on_image_array(image, bounding_boxes, color='blue', thickness=2):
    for bounding_box in bounding_boxes:
        draw_box_on_image(image, bounding_box, color)

def draw_density_graph_on_image(image, grid_graph, density_graph):
    # Create an PIL Image from the numpy array image
    image_pil = Image.fromarray(numpy.uint8(image)).convert('RGB')

    # Create an object that can be used to draw in the given image
    draw = ImageDraw.Draw(image_pil, 'RGBA')

    # Get the width and height of the image
    image_width, image_height = image_pil.size

    # Define colors based for the different 
    free_density_color = (255, 255, 155, 80)
    light_density_color = (100, 206, 143, 80)
    medium_density_color = (255, 203, 70, 80)
    high_density_color = (247, 104, 104, 80)
    null_density_color = (0, 0, 0, 80)

    print(grid_graph)
    print('===============================================')
    print('===============================================')
    print('===============================================')
    # for row_index in range(0, len(density_graph)):
    for row_index in range(0, len(grid_graph)):
        # Set the opposite vertecies of the box coors to the non-normalised coordinates
        # min_coords = (coords[0][0] * image_width, coords[0][1] * image_height)
        # max_coords = (coords[2][0] * image_width, coords[2][1] * image_height)
        # min_coords = (int(grid_graph[row_index][0][0] * image_width), int(grid_graph[row_index][0][1] * image_height))
        # max_coords = (int(grid_graph[row_index][2][0] * image_width), int(grid_graph[row_index][2][1] * image_height))
        # print(grid_graph[row_index])
        # print(min_coords)
        # print(max_coords)
        # for density_index in range(0, 4):
            # print(grid_graph[row_index])
            # print('-----------------------------------')
            # min_coords = (grid_graph[row_index][0][0], grid_graph[row_index][0][1])
            # max_coords = (grid_graph[row_index][density_index])
        # print('===============================================')
        print(grid_graph[row_index])
        for density_index in range(0, 4):
            # print(grid_graph[row_index][0])
            min_coords = (int(grid_graph[row_index][0][0] * image_width), int(grid_graph[row_index][0][1] * image_height))
            max_coords = (int(grid_graph[row_index][2][0] * image_width), int(grid_graph[row_index][2][1] * image_height))
            # print(min_coords)
            # print(max_coords)
            print('-----------------------------------')
            if density_graph[row_index][density_index] == 0:
                draw.rectangle([min_coords, max_coords], fill=free_density_color)
            elif density_graph[row_index][density_index] == 1:
                draw.rectangle([min_coords, max_coords], fill=light_density_color)
            elif density_graph[row_index][density_index] == 2:
                draw.rectangle([min_coords, max_coords], fill=medium_density_color)
            elif density_graph[row_index][density_index] == 3:
                draw.rectangle([min_coords, max_coords], fill=high_density_color)
            else:
                draw.rectangle([min_coords, max_coords], fill=null_density_color)
        print('===============================================')

    # Copy the values from the drawn image into the original image array
    numpy.copyto(image, numpy.array(image_pil))
