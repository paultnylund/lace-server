import sys
import cStringIO
import re
from PIL import Image

from grid_detection import grid
import detect

# import object detection
# import grid tools

# Take the input image
image_path = '/var/lace-server/detection_images/detection.jpg'
# image_data = re.sub('^data:image/.+;base64,', '', data).decode('base64')
# image_path = 'object_detection/test_images/image1_old.jpg'
# image = Image.open(BytesIO(base64.b64decode(data)))
# image = Image.open(cStringIO.StringIO(image_data))
image = Image.open(image_path)
# print(image)

# Run object detection on the image which returns the bounding boxes
detection_results = detect.run_object_detection_on_image(image)
bounding_boxes = detection_results['bounding_boxes']
classes = detection_results['classes']
distance = detection_results['node_distance']

# Run grid tools on with the bounding boxes which returns density graph
density_grid = grid.create_density_grid(bounding_boxes, classes, distance, 21)
# print(bounding_boxes)
# Flush the density graph to stdout
sys.stdout.write(density_grid)
