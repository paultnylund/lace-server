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
    (image_width, image_height) = image.size
    return numpy.array(image.getdata()).reshape((image_width, image_width, 3)).astype(numpy.uint8)

def draw_grid_line_on_image(image, xcoord, ycoord, color='black', thickness=4):
    '''
    '''
    image_pil = Image.fromarray(numpy.uint8(image)).convert('RGB')
    draw = ImageDraw.Draw(image_pil)
    image_width, image_height = image_pil.size

    min_coords = (xcoord['start'], ycoord * image_height)

def draw_grid_on_image_array(image, coordinates, color='black', thickness=4):
    '''
    '''
    for coord in coordinates:
        xcoord = {'start': 0, 'end': 1}
        ycoord = coord
        