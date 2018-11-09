# Imports
import numpy
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot
from PIL import Image
from PIL import ImageDraw

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils

# Verify that the latest version of TensorFlow is installed
if tf.__version__ != '1.4.0':
	raise ImportError('Please upgrade the TF installation to v1.4.0')
	

####################################################
# Model Preparation
####################################################

# What model to download
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box
PATH_TO_LABELS = os.path.join('object_detection/data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

# Download Model
# opener = urllib.request.URLopener()
# opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
# tar_file = tarfile.open(MODEL_FILE)
# for file in tar_file.getmembers():
# 	file_name = os.path.basename(file.name)
# 	if 'frozen_inference_graph.pb' in file_name:
# 		tar_file.extract(file, os.getcwd())

# Load a (frozen) TensorFlow model in memory
detection_graph = tf.Graph()
with detection_graph.as_default():
	od_graph_def = tf.GraphDef()
	with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
		serialized_graph = fid.read()
		od_graph_def.ParseFromString(serialized_graph)
		tf.import_graph_def(od_graph_def, name='')

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Helper code
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
	
	print(image.size)

	# Return a numpy array representation of the image as uint8
	return numpy.array(image.getdata()).reshape((image_height, image_width, 3)).astype(numpy.uint8)

####################################################
# Detection
####################################################

PATH_TO_TEST_IMAGES_DIR = 'object_detection/test_images/'
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}_old.jpg'.format(i)) for i in range(1, 2) ]

# Sizes in 
IMAGE_SIZE = (12, 8)

with detection_graph.as_default():
	with tf.Session(graph=detection_graph) as sess:
		sess.run(tf.global_variables_initializer())
		img = 1
		for image_path in TEST_IMAGE_PATHS:
			image = Image.open(image_path)
			# the array based representation of the image will be used later in order to prepare the
			# result image with boxes and labels on it.
			image_np = load_image_into_numpy_array(image)
			# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
			image_np_expanded = numpy.expand_dims(image_np, axis=0)
			image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
			# Each box represents a part of the image where a particular object was detected.
			boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
			# Each score represent how level of confidence for each of the objects.
			# Score is shown on the result image, together with the class label.
			scores = detection_graph.get_tensor_by_name('detection_scores:0')
			classes = detection_graph.get_tensor_by_name('detection_classes:0')
			num_detections = detection_graph.get_tensor_by_name('num_detections:0')
			# Actual detection.
			(boxes, scores, classes, num_detections) = sess.run(
				[boxes, scores, classes, num_detections],
				feed_dict={image_tensor: image_np_expanded}
			)
			########################
			# TEST
			########################
			# Print the outputs
			classes = numpy.squeeze(classes).astype(numpy.int32)
			scores = numpy.squeeze(scores)
			boxes = numpy.squeeze(boxes)
			threshold = 0.5
			obj_above_thresh = sum(n > threshold for n in scores)
			print('detected %s objects in %s above as %s score' % (obj_above_thresh, image_path, threshold))
			for c in range(0, len(classes)):
				if scores[c] > threshold:
					class_name = category_index[classes[c]]['name']
					print(' object %s is a %s - score: %s, location: %s' % (c, class_name, scores[c], boxes[c]))
			# TODO: Remove on deploy
			# draw_grid_on_image_array(image_np)
			# pyplot.figure(figsize=IMAGE_SIZE)
			# pyplot.imsave(str(img) + '.jpg', image_np)
			# Visualization of the results of a detection.
			visualization_utils.visualize_boxes_and_labels_on_image_array(
				image_np,
				numpy.squeeze(boxes),
				numpy.squeeze(classes).astype(numpy.int32),
				numpy.squeeze(scores),
				category_index,
				min_score_thresh=.5,
				use_normalized_coordinates=True,
				line_thickness=2,
			)
			pyplot.figure(figsize=IMAGE_SIZE)
			pyplot.imsave(str(img) + '.jpg', image_np)
			# img += 1

# # Put the object in JSON
# class Object(object):
# 	def __init__(self):
# 		self.name='TensorFlow Object API Service 0.0.1'
# 	def toJSON(self):
# 		return json.dumps(self.__dict__)

# def get_objects(image, threshold=0.1):
# 	image_np = load_image_into_numpy_array(image)
# 	# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
#     image_np_expanded = np.expand_dims(image_np, axis=0)
#     # Actual detection.
#     (boxes, scores, classes, num) = sess.run(
#         [detection_boxes, detection_scores, detection_classes, num_detections],
#         feed_dict={image_tensor: image_np_expanded})
 
#     classes = np.squeeze(classes).astype(np.int32)
#     scores = np.squeeze(scores)
#     boxes = np.squeeze(boxes)obj_above_thresh = sum(n > threshold for n in scores)
 
#     obj_above_thresh = sum(n > threshold for n in scores)
#     print("detected %s objects in image above a %s score" % (obj_above_thresh, threshold))

# 	output = []
 
#     #Add some metadata to the output
#     item = Object()
#     item.numObjects = obj_above_thresh
#     item.threshold = threshold
#     output.append(item)
 
#     for c in range(0, len(classes)):
#         class_name = category_index[classes[c]]['name']
#         if scores[c] >= threshold:      # only return confidences equal or greater than the threshold
#             print(" object %s - score: %s, coordinates: %s" % (class_name, scores[c], boxes[c]))
 
#             item = Object()
#             item.name = 'Object'
#             item.class_name = class_name
#             item.score = float(scores[c])
#             item.y = float(boxes[c][0])
#             item.x = float(boxes[c][1])
#             item.height = float(boxes[c][2])
#             item.width = float(boxes[c][3])
 
#             output.append(item)
 
#     outputJson = json.dumps([ob.__dict__ for ob in output])
#     return outputJson
