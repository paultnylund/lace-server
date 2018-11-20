# Imports
import numpy
import os
import sys
import tarfile
import zipfile
import six.moves.urllib as urllib
import tensorflow as tf
from PIL import Image

from object_detection.utils import label_map_util

# Verify that the latest version of TensorFlow is installed
# if tf.__version__ != '1.4.0':
# 	raise ImportError('Please upgrade the TF installation to v1.4.0')

MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = 'ssd_mobilenet_v1_coco_2017_11_17.tar.gz'

# Initialise a TensorFlow computation graph
detection_graph = tf.Graph()

# List of the strings that is used to add correct label for each box
PATH_TO_LABELS = os.path.join('/var/lace-sercer/object_detection/data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def download_and_unpack_model():
	'''Download and unpack the object detection model'''
	print('Downloading model')
	DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
	
	try:
		# Donload the model
		opener = urllib.request.URLopener()
		opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
		print('Extracting model')
		# Extract all the files in the archive
		tar_file = tarfile.open(MODEL_FILE)
		for file in tar_file.getmembers():
			file_name = os.path.basename(file.name)
			if 'frozen_inference_graph.pb' in file_name:
				tar_file.extract(file, os.getcwd())
		print('Cleaning up tar.gz files')
		# Clean up the tar archive
		os.remove(MODEL_FILE)
		# Load the inference model into memory
		load_frozen_inference_graph_in_memory()
	except:
		print('Failed to download and unpack the specified file!')
		print(sys.exc_info()[0])

def load_frozen_inference_graph_in_memory():
	'''If exists, load the frozen inference graph into memory, else download and unpack it
	'''
	try:
		PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
		with detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')
	except:
		print('Failed to unpack the specified file!')
		sys.stdout.write(PATH_TO_CKPT)
		print('; No such file or directory')
		print(sys.exc_info()[0])
		download_and_unpack_model()

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
	
	np_image = numpy.array(image.getdata())
	np_image = np_image[...,:3]
	# print(len(image.shape))

	# Return a numpy array representation of the image as uint8
	return np_image.reshape((image_height, image_width, 3)).astype(numpy.uint8)
	# return numpy.array(image.getdata()).reshape((image_height, image_width, 3)).astype(numpy.uint8)

# Load the frozen inference graph into memory
load_frozen_inference_graph_in_memory()

with detection_graph.as_default():
	with tf.Session(graph=detection_graph) as sess:
		# sess.run(tf.global_variables_initializer())
		# Definite input and output Tensors for detection_graph
		image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
		# Each score represent the level of confidence for each object
		detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
		# The classification of the detected object
		detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
		num_detections = detection_graph.get_tensor_by_name('num_detections:0')

def run_object_detection_on_image(image, threshold=0.5):
	# Load the image into a numpy array
	numpy_image_array = load_image_into_numpy_array(image)
	# Wxpand the dimensions of the numpy array to fit that needed for object detection
	numpy_image_array_expanded = numpy.expand_dims(numpy_image_array, axis=0)

	# Actual detection.
	(boxes, scores, classes, num) = sess.run(
		[detection_boxes, detection_scores, detection_classes, num_detections],
		feed_dict={image_tensor: numpy_image_array_expanded}
	)

	classes = numpy.squeeze(classes).astype(numpy.int32)
	scores = numpy.squeeze(scores)
	boxes = numpy.squeeze(boxes).tolist()

	bounding_boxes = []
	bounding_classes = []
	# If the detection score is above the threshold, add the bounding box and class
	for c in range(0, len(classes)):
		if scores[c] > threshold:
			box = [
				[boxes[c][1], boxes[c][0]],
				[boxes[c][3], boxes[c][0]],
				[boxes[c][3], boxes[c][2]],
				[boxes[c][1], boxes[c][2]]
			]
			bounding_boxes.append(box)
			bounding_classes.append(category_index[classes[c]]['name'])
	
	# Initialise a dictionary for return
	detection_result = {}
	detection_result['bounding_boxes'] = bounding_boxes
	detection_result['classes'] = bounding_classes
	# TODO: This should be done dynamically some how
	detection_result['node_distance'] = 4

	# Return the detection result dictionary
	return detection_result