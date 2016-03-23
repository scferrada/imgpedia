# IMGpedia Descriptors
Reference implementations for visual descriptors used in the **IMGpedia project**. These are made publicly available
as an effort to bring the Image Analysis process closer to the Semantic Web community. Although these implementations can
be used by anyone under **GNU GPL** license

### About the descriptors

######Gray Histogram Descriptor:
Images are partitioned in a fixed amount of blocks.
Per each block a histogram of gray intensity is computed, typically intensity
takes 8 bit values. Finally, the descriptor is the concatenation of all histograms.
######Oriented Gradients Descriptor:
Image gradient is calculated via convolution
with Sobel kernels. A threshold is then applied to the gradient, and for those
pixels that exceed it, the orientation of the gradient is calculated. Finally, a
histogram of the orientations is computed and is used as the descriptor.
######Edge Histogram Descriptor:
For each 2 × 2 pixel block, the dominant edge orientation is computed (horizontal, vertical, both diagonals or none), where the
descriptor is a histogram of these orientations.
######DeCAF7:
Uses a Caffe neural network pre-trained with the Imagenet dataset.
To obtain the vector, each image is resized and ten overlapping patches are
extracted, each patch is given as input to the neural network and the last selfconvolutional layer of the model is extracted as a descriptor, so the final vector
is the average of the layers for all the patches

### Dependencies
In order to get the code working a few dependencies are needed:

- OpenCV
This is the main dependency for all descriptors. Our code works with version 2.4.11 or superior. For installation instructions,
please refer to the official documentation for OpenCV in [Linux](http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html), [Windows](http://docs.opencv.org/2.4/doc/tutorials/introduction/windows_install/windows_install.html).
Or [Install just python bindigs](http://docs.opencv.org/3.1.0/d5/de5/tutorial_py_setup_in_windows.html#gsc.tab=0 ) if you like.

- Caffe
This is only needed for the neural networks used to extract DeCAF7, so, if you will not use it, there is no need to install Caffe.
Otherwise, you can found installation instructions [here](http://caffe.berkeleyvision.org/installation.html)

And that's it, once you've installed OpenCV and Caffe, all algorithms should run in your preferred language

### Usage
Both python and java implementations are objects that inherits of superclass _DescriptorComputer_ which defines the abstract method _compute_ that is implemented following the algorithms for each descriptor
so, in order to compute the descriptor vector of an image you should do something like (in python, java syntax can be inferred):
```
computer = GrayHistogramComputer(2,2,32)
img = cv2.imread("image.jpg")
descriptor = computer.compute(img) #so descriptor is a vector of 2 x 2 x 32 dimensions
```
C++ implementation consist only on functions that can be imported and used with no object orientation.

Finally, any doubt you have with the process, e-mail me to: sferrada [at] dcc [dot] uchile [dot] cl