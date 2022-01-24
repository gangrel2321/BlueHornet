FROM ubuntu:16.04

RUN apt-get update -y 
RUN apt-get install -y \
	vim \
	cmake \
	curl \
	g++ \
	git \ 
	wget \
	unzip \
	python3 \
	python3-pip \
	python3-setuptools
	

# Download and unpack opencv
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip 
RUN unzip opencv.zip

RUN mkdir -p build && cd build

# Configure
RUN cmake ../opencv-4.x

# Build
RUN cmake --build .

# Python Dependencies 
RUN python3 -m pip install --upgrade pip 
RUN python3 -m pip install \
	pillow \
	numpy \
	pandas \
	argparse \
	GitPython \ 
	pybind11 
