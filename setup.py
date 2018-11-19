##################################################
# Setup script for object_detection
##################################################
from setuptools import find_packages
from setuptools import setup

# Define the required packages
REQUIRED_PACKAGES = [
    'Pillow',
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