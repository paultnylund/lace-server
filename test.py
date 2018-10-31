import numpy
import sys
from matplotlib import pyplot
from PIL import Image
from PIL import ImageDraw

def load_image_into_numpy_array(image):
	(im_width, im_height) = image.size
	return numpy.array(image.getdata()).reshape((im_height, im_width, 3)).astype(numpy.uint8)

def draw_grid_on_image_array(image,
							coordinates,
							color='black',
							thickness=4):
	for coord in coordinates:
		xcoord = {'start': 0, 'end': 1}
		ycoord = coord
		draw_grid_line_on_image(image, xcoord, ycoord)

	return image

def draw_grid_line_on_image(image,
							xcoord,
							ycoord,
							color='black',
							thickness=4):
	image_pil = Image.fromarray(numpy.uint8(image)).convert('RGB')
	draw = ImageDraw.Draw(image_pil)
	image_width, image_height = image_pil.size

	min_coords = (xcoord['start'], ycoord * image_height)
	max_coords = (xcoord['end'] * image_width, ycoord * image_height)
	draw.line([min_coords, max_coords], width=thickness, fill=color)

	numpy.copyto(image, numpy.array(image_pil))

def find_grid_and_bounding_box_overlap(boundingbox, gridbox):
	# Define the index for the upper bound
	upper_index = 3
	# Define the index for the lower bound
	lower_index = 1
	x = 0
	y = 1

	# Function for calculating the distance of overlap on an axis
	def distance(r1lower, r2lower, r1upper, r2upper):
		return min(r1upper, r2upper) - max(r1lower, r2lower)
	
	# Calculate the distance of overlap on the y-axis
	y_distance = distance(
							boundingbox[upper_index][y],
							gridbox[upper_index][y],
							boundingbox[lower_index][y],
							gridbox[lower_index][y])

	# Return false if there is no overlap
	if y_distance <= 0:
		return False
	
	# Calculate the distance of overlap on the x-axis
	x_distance = distance(
							boundingbox[upper_index][x],
							gridbox[upper_index][x],
							boundingbox[lower_index][x],
							gridbox[lower_index][x])

	# Return false if there is no overlap
	if x_distance <= 0:
		return False

	# Calculate the area of overlap
	overlap_area = y_distance * x_distance

	return overlap_area

## RUN TEST
# boundingbox = [[5, 8], [10, 8], [10, 6], [5, 6]]
# gridbox = [[4, 5], [7, 5], [7, 2], [4, 2]]
# overlap_area = find_grid_and_bounding_box_overlap(boundingbox, gridbox)
# print(overlap_area)
coordinates = numpy.linspace(0, 1, 50)
print(coordinates)
# image = Image.open('object_detection/test_images/image1.jpg')
# image_array = load_image_into_numpy_array(image)
# draw_grid_on_image_array(image_array, coordinates, 'black', 1)
# draw_grid_line_on_image(image_array, 0.5, 0.5)
# pyplot.figure(figsize=(12, 8))
# pyplot.imsave('test' + '.jpg', image_array)

# test = numpy.linspace(0, 1, length)
# final = numpy.zeros((50, 2))

# iterator = 0
# for each in test:
#     final[iterator] = [each, 1]
#     iterator += 1

# for each in final:
#     print(each[0])
#     print(each[1])
#     print('---------------------')

# print(test)
# print(final)
