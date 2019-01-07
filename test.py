import numpy
import sys
import math
import json
# from matplotlib import pyplot
# from PIL import Image
# from PIL import ImageDraw

from grid_detection import grid
# from grid_detection import visualisation

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

# image = Image.open('detection.jpg')
# image = Image.open('/var/lace-server/detection_images/detection.jpg')

# image_array = load_image_into_numpy_array(image)

generated_grid = grid.create_grid_boxes_array(7)

# print(sys.getsizeof(generated_grid))
print(generated_grid)

boundingboxes_test = [
	[
		[0.6916143894195557, 0.7077077031135559],
		[0.8271324634552002, 0.7077077031135559],
		[0.8271324634552002, 0.9436697363853455],
		[0.6916143894195557, 0.9436697363853455]
	],
	[
		[0.2702397108078003, 0.7390063405036926],
		[0.4274061918258667, 0.7390063405036926],
		[0.4274061918258667, 0.9456049799919128],
		[0.2702397108078003, 0.9456049799919128]
	],
	[
		[0.6434462070465088, 0.7121392488479614],
		[0.7989441156387329, 0.7121392488479614],
		[0.7989441156387329, 0.9437928199768066],
		[0.6434462070465088, 0.9437928199768066]
	]
]

# test = [3.0, 0, 0, 1.0, 4.0, 1.0, 1.0, 0, 0]
# # output = [[3.0, 0] [0, 0]]
# output = []

# length = int(math.sqrt(len(test)))
# iterator = 0

# # for each_row in test:
# # 	temp = []
# # 	for each_item in range(iterator, )
# # 	iterator += length


# while iterator < len(test):
# 	temp = []
# 	for each in range(iterator, iterator + length):
# 		temp.append(test[each])
# 	output.append(temp)
# 	iterator += length

# print(output)

# print(sys.argv[1])

# density_grid = grid.create_density_grid(boundingboxes_test, '', 4, 25)
# sys.stdout.write(density_grid)

# visualisation.draw_grid_on_image_array(image_array, generated_grid)
# visualisation.draw_bounding_boxes_on_image_array(image_array, boundingboxes_test)
# visualisation.draw_density_graph_on_image(image_array, generated_grid, density_grid)
# pyplot.figure(figsize=(12, 8))
# pyplot.imsave('test' + '.jpg', image_array)

# def load_image_into_numpy_array(image):
# 	(im_width, im_height) = image.size
# 	return numpy.array(image.getdata()).reshape((im_height, im_width, 3)).astype(numpy.uint8)

# image = Image.open('object_detection/test_images/image1.jpg')
# image_array = load_image_into_numpy_array(image)

# def draw_grid_on_image_array(image,
# 							coordinates,
# 							color='black',
# 							thickness=4):
# 	for coord in coordinates:
# 		xcoord = {'start': 0, 'end': 1}
# 		ycoord = coord
# 		draw_grid_line_on_image(image, xcoord, ycoord)

# 	return image

# def draw_grid_line_on_image(image,
# 							xcoord,
# 							ycoord,
# 							color='black',
# 							thickness=4):
# 	image_pil = Image.fromarray(numpy.uint8(image)).convert('RGB')
# 	draw = ImageDraw.Draw(image_pil)
# 	image_width, image_height = image_pil.size

# 	min_coords = (xcoord['start'], ycoord * image_height)
# 	max_coords = (xcoord['end'] * image_width, ycoord * image_height)
# 	draw.line([min_coords, max_coords], width=thickness, fill=color)

# 	numpy.copyto(image, numpy.array(image_pil))

# def find_grid_and_bounding_box_overlap(boundingbox, gridbox):
# 	# Define the index for the upper bound
# 	upper_index = 3
# 	# Define the index for the lower bound
# 	lower_index = 1
# 	x = 0
# 	y = 1

# 	# Function for calculating the distance of overlap on an axis
# 	def distance(r1lower, r2lower, r1upper, r2upper):
# 		return min(r1upper, r2upper) - max(r1lower, r2lower)
	
# 	# Calculate the distance of overlap on the y-axis
# 	y_distance = distance(
# 							boundingbox[upper_index][y],
# 							gridbox[upper_index][y],
# 							boundingbox[lower_index][y],
# 							gridbox[lower_index][y])

# 	# Return false if there is no overlap
# 	if y_distance <= 0:
# 		return False
	
# 	# Calculate the distance of overlap on the x-axis
# 	x_distance = distance(
# 							boundingbox[upper_index][x],
# 							gridbox[upper_index][x],
# 							boundingbox[lower_index][x],
# 							gridbox[lower_index][x])

# 	# Return false if there is no overlap
# 	if x_distance <= 0:
# 		return False

# 	# Calculate the area of overlap
# 	overlap_area = y_distance * x_distance

# 	return overlap_area

## RUN TEST
# boundingbox = [[5, 8], [10, 8], [10, 6], [5, 6]]
# gridbox = [[4, 5], [7, 5], [7, 2], [4, 2]]
# overlap_area = find_grid_and_bounding_box_overlap(boundingbox, gridbox)
# print(overlap_area)
# coordinates = numpy.linspace(0, 1, 50)
# print(coordinates)

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
