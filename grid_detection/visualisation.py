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

def draw_box_on_image(image, box_coords, color='red', thickness=2):
    '''Draw single grid box on image
    '''
    # Create an PIL Image from the numpy array image
    image_pil = Image.fromarray(numpy.uint8(image)).convert('RGB')

    # Create an object that can be used to draw in the given image
    draw = ImageDraw.Draw(image_pil)

    # Get the width and height of the image
    image_width, image_height = image_pil.size

    # Set the oposite vertecies of the grid box to the non-normalised coordinates
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
        draw_box_on_image(image, grid_box)

def draw_bounding_boxes_on_image_array(image, bounding_boxes, color='blue', thickness=2):
    for bounding_box in bounding_boxes:
        draw_box_on_image(image, bounding_box, color)

def draw_density_graph_on_image_array(image, density_graph):
    image_pil = Image.fromarray(numpy.uint8(image)).convert('RGB')

    draw = ImageDraw.Draw(image_pil)

    image_width, image_height = image_pil.size

    
