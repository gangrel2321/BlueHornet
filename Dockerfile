FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninterative
RUN apt-get update && apt-get install -y tzdata \
	vim \
	cmake \
	curl \
	g++ \
	git \ 
	wget \
	unzip \
	python3 \
	python3-pip
	

# Download and unpack opencv
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip 
RUN unzip opencv.zip

RUN mkdir -p build
RUN cd build

# Configure
RUN cmake ../opencv-4.x

# Build
RUN cmake -f Makefile --build .
RUN make install

# Python Dependencies
RUN python3 -m pip install --upgrade pip 
RUN python3 -m pip install \
	Pillow \
	numpy \
	pandas \
	argparse \
	pybind11 \
	GitPython 
RUN cd .. 
