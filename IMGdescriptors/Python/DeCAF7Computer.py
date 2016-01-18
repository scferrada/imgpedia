import numpy as np
import os, sys, getopt, cv2, random, string, shutil
sys.path.insert(0, os.path.join('caffe', 'python'))
import caffe

from DescriptorComputer import DescriptorComputer

class DeCAF7Computer(DescriptorComputer):

	def __init__(self, layer="fc7", oversample = True):
		self.caffe_root = "caffe"
		self.model_prototxt = os.path.join(self.caffe_root, 'deploy.prototxt')
		self.model_trained = os.path.join(self.caffe_root, "bvlc_reference_caffenet.caffemodel")
		self.mean_image = os.path.join(self.caffe_root, 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
		self.layer = layer
		caffe.set_mode_cpu()
		self.net = caffe.Classifier(self.model_prototxt, self.model_trained,
						   mean=np.load(self.mean_image).mean(1).mean(1),
						   channel_swap=(2,1,0),
						   raw_scale=255,
						   image_dims=(256, 256))
		self.size = (256,256)
		self.patch_size = 224
		self.prefix = "DeCAF7"
		self.oversample = oversample
	
	def compute_oversample(self, framepath):
		input_image = caffe.io.load_image(framepath)
		prediction = self.net.predict([input_image], oversample=False)
		return self.net.blobs[self.layer].data[0].reshape(1,-1)

	def compute(self, image):
		directory = ''.join(random.choice(string.lowercase) for _ in range(8))
		if not os.path.exists(directory):
			os.makedirs(directory)
		image = cv2.resize(image, self.size)
		patches = []
		patches.append(image)
		patches.append(image[:self.patch_size, :self.patch_size])
		patches.append(image[32:,32:])
		patches.append(image[32:, :self.patch_size])
		patches.append(image[:self.patch_size, 32:])
		patches.append(image[16:-16, 16:-16])
		patches.append(image[16:-16, 32:])
		patches.append(image[16:-16, :self.patch_size])
		patches.append(image[32:, 16:-16])
		patches.append(image[:self.patch_size, 16:-16])

		descriptor = np.zeros((1,4096))
		for i in range(len(patches)):
			filepath = os.path.join(directory, ("%d.jpg" % i))
			cv2.imwrite(filepath, patches[i])
			descriptor = descriptor + self.compute_oversample(filepath)
		shutil.rmtree(directory)
		return descriptor/len(patches)