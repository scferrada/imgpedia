# IMGpedia
[![License: ODbL](https://img.shields.io/badge/License-ODbL-brightgreen.svg)](https://opendatacommons.org/licenses/odbl/)

[**IMGpedia**](http://imgpedia.dcc.uchile.cl) is a Linked Dataset that incorporates visual information of the images from the Wikimedia Commons dataset: it brings together descriptors of the visual content of 15 million images, 450 million visual-similarity relations between those images, links to image metadata from DBpedia Commons, and links to the DBpedia resources associated with individual images. It allows people to perform _visuo-semantic_ queries over the images.

For exploring the data, you can follow these links:

  - [SPARQL Endpoint](http://imgpedia.dcc.uchile.cl/sparql)
  - [IMGpedia RDF Dumps](http://imgpedia.dcc.uchile.cl/dumps)
  - [VoID Statistics](http://imgpedia.dcc.uchile.cl/dumps/20170506/void.nt)
  - [Figshare](https://doi.org/10.6084/m9.figshare.4991099.v2)
  - [w3id Persistent Identifier](http://w3id.org/imgpedia)
  - [GitHub Issue Tracker](https://github.com/scferrada/imgpedia/issues)

## IMGpedia Descriptors
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

Reference implementations for the visual descriptors used in the **IMGpedia project**<sup>1</sup> written in Python, Java and C++. These are made publicly available
as an effort to bring the Image Analysis process closer to the Semantic Web community. However, these implementations can
be used by anyone under **GNU GPL** license

### About the descriptors

- Gray Histogram Descriptor:
We transform the image from color to grayscale and divide it into a fixed number of blocks. 
A histogram of 8-bit gray intensities is then calculated for each block. 
The concatenation of all histograms is used to generate a description vector.
- Histogram of Oriented Gradients:
We extract edges of the grayscale image by computing its gradient (using Sobel kernels), applying a threshold, and computing the orientation of the gradient. 
Finally, a histogram of the orientations is made and used as a description vector.
- Color Layout Descriptor:
We divide the image into blocks and for each block we compute the mean (YCbCr) color. Afterwards the Discrete Cosine Transform is computed for each color channel. 
Finally the concatenation of the transforms is used as the descriptor vector, with 192 dimensions.
- Edge Histogram Descriptor:
For each 2 x 2 pixel block, the dominant edge orientation is computed (horizontal, vertical, both diagonals or none), where the
descriptor is a histogram of these orientations. *This implementation is no longer used in the IMGpedia project*.
- DeCAF7:
Uses a Caffe neural network pre-trained with the Imagenet dataset.
To obtain the vector, each image is resized and ten overlapping patches are
extracted, each patch is given as input to the neural network and the last selfconvolutional layer of the model is extracted as a descriptor, so the final vector
is the average of the layers for all the patches

### Dependencies
In order to get the code to work a few dependencies are needed:

- **OpenCV:**
This is the main dependency for all descriptors. Our code works with version 2.4.11 or superior. For installation instructions,
please refer to the official documentation for OpenCV in [Linux](http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html), [Windows](http://docs.opencv.org/2.4/doc/tutorials/introduction/windows_install/windows_install.html).
Or [Install just python bindigs](http://docs.opencv.org/3.1.0/d5/de5/tutorial_py_setup_in_windows.html#gsc.tab=0 ) if you like.

- **Caffe:**
This is only needed for the neural networks used to extract DeCAF7, so, if you will not use it, there is no need to install Caffe.
Otherwise, you can find installation instructions [here](http://caffe.berkeleyvision.org/installation.html)

And that's it, once you've installed OpenCV and Caffe, all algorithms should run in your favourite language.

### Usage
Both python and java implementations are objects that inherit from superclass _DescriptorComputer_ which defines the abstract method _compute_ that is implemented according to the algorithms of each descriptor
so, in order to compute the descriptor vector of an image you should do something like (in Python, Java syntax can be inferred):
```
computer = GrayHistogramComputer(2,2,32)
img = cv2.imread("image.jpg")
descriptor = computer.compute(img) #so descriptor is a vector of 2 x 2 x 32 dimensions
```
C++ implementation consist only on functions that can be imported and used with no object orientation.

Finally, any doubt you have with the process, send me an e-mail to: sferrada [at] dcc [dot] uchile [dot] cl or open up an Issue.

<sup>1</sup> Read more about the **IMGpedia project** [here](https://pdfs.semanticscholar.org/a183/cad3b935f95b7792375e110f3eeee6ad2938.pdf). 
If you want to visit our SPARQL Endpoint and try some queries visit [this link](http://imgpedia.dcc.uchile.cl/sparql), the available vocabulary can be found [here](http://imgpedia.dc.uchile.cl/ontology).