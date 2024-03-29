#!/bin/bash

# Get packages required for OpenCV
sudo apt-get update
sudo apt-get -y install supervisor
sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev
sudo apt-get -y install qt4-dev-tools
sudo apt-get -y install libatlas-base-dev

# Get packages required for TensorFlow
# Using the tflite_runtime packages available at https://www.tensorflow.org/lite/guide/python
# Will change to just 'pip3 install tensorflow' once newer versions of TF are added to piwheels

#pip3 install tensorflow

#version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

# https://github.com/iCorv/tflite-runtime - find correct runtime for OS and python version
# pip3 install https://github.com/iCorv/tflite-runtime/raw/master/tflite_runtime-2.4.0-py3-none-any.whl
