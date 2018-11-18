##################################################
# Setup script for object_detection
##################################################
from setuptools import find_packages
from setuptools import setup

# Define the required packages
REQUIRED_PACKAGES = [
    'Pillow',
    'tensorflow',
    'six',
    'absl-py',
]

# Run the setup initialiser and install the packages
setup(
    name='lace_object_detection',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    packages=[p for p in find_packages()],
    description='lace : TensorFlow Object Detection',
)

# Download the Object Detection directory
import six.moves.urllib as urllib
from zipfile import ZipFile
import os
import re
import shutil

print('Downloading the TensorFlow API from GitHub...')

# Set the url for the repository
REPOSITORY_ZIP_URL = 'https://github.com/tensorflow/models/archive/master.zip'

try:
    # Copy the network object denoted by the URL to the local file
    filename, headers = urllib.request.urlretrieve(REPOSITORY_ZIP_URL)
    
    # Set the target path for our files
    target_path = os.path.join(os.getcwd(), 'object_detection/')
    temp_path = filename + '_dir'

    # 
    with ZipFile(filename, 'r') as zip_file:
        files = zip_file.namelist()
        fiels_to_extract = [f for f in files if f.startswith(('models-master/research/object_detection/'))]
        zip_file.extractall(temp_path, fiels_to_extract)
        print('Copying TensorFlow Object API files to %s' % target_path)
        shutil.move(os.path.join(temp_path, 'models-master/research/object_detection/'), target_path)
        os.removedirs(os.path.join(temp_path, 'models-master/research/'))

except:
    print('Problem downloading the TensorFlow Object API.\n'
    'Try running `git clone https://github.com/tensorflow/models.git`.\n'
    'Then `cp /research/object_detection to /object_detection` instead')

# Compile Protobufs
import subprocess
print('Compiling protobufs')
try:
    subprocess.Popen('protoc object_detection/protos/*.proto --python_out=.', shell=True)
except:
    print('Error compiling protobufs')

# Clean up temporary files left behind by urlretrieve() calls
urllib.request.urlcleanup()
