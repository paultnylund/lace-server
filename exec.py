import sys

import detect
from PIL import Image
from grid_detection import grid

# import object detection
# import grid tools

# Take the input image
# image = sys.argv[0]
image_path = 'object_detection/test_images/image1_old.jpg'
image = Image.open(image_path)

# Run object detection on the image which returns the bounding boxes
detection_results = detect.run_object_detection_on_image(image)
bounding_boxes = detection_results['bounding_boxes']
classes = detection_results['classes']
distance = detection_results['node_distance']

# Run grid tools on with the bounding boxes which returns density graph
density_grid = grid.create_density_grid(bounding_boxes, classes, distance)

# Flush the density graph to stdout
sys.stdout.write(density_grid)
