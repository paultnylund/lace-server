#!/bin/zsh

sudo apt update

echo '>> Install Python and the TensorFlow package dependencies'
if [ dpkg -l | grep python-dev -eq 0 ] ; then
	echo '>> Installing missing python-dev package'
	sudo apt install python-dev
fi
if [ dpkg -l | grep python-pip ] ; then
	echo '>> Installing missing python-pip package'
	sudo apt install python-pip
fi

echo '>> Installing the TensorFlow pip package dependencies'
sudo pip install -U --user numpy six wheel mock
echo '>> Installing keras_applications package'
sudo pip install -U --user keras_applications==1.0.5 --no-deps
echo '>> Installing keras_applications package'
sudo pip install -U --user keras_preprocessing==1.0.3 --no-deps

echo '>> Install and configure Bazel'
echo '>> Installing bazel prerequisites'
sudo apt install pkg-config zip g++ zlib1g-dev unzip python

echo '>> Downloading bazel installer'
wget https://github.com/bazelbuild/bazel/releases/download/0.18.1/bazel-0.18.1-installer-linux-x86_64.sh

sudo chmod +x bazel*
sudo ./bazel* --user

echo "export PATH='$PATH:$HOME/bin'" >> ~/.zshrc
source ~/.zshrc

sudo apt install openjdk-8-jdk

echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list

curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -

sudo apt update && sudo apt install bazel

sudo apt install --only-upgrade bazel

git clone https://github.com/tensorflow/tensorflow.git

cd tensorflow

git checkout r1.12

bazel clean

./configure

sudo apt install libc-ares-dev

bazel build -c opt --define=grpc_no_ares=true --copt=-mavx2 --copt=-mavx512f --copt=-mfma //tensorflow/tools/pip_package:build_pip_package

./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg

pip install /tmp/tensorflow_pkg/tensorflow-*.whl