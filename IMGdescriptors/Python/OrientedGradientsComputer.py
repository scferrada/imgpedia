import cv2
import numpy as np
from DescriptorComputer import DescriptorComputer

class OrientedGradientsComputer(DescriptorComputer):
	
	def __init__(self, rows, cols, threshold):
		self.rows = rows
		self.cols = cols
		self.threshold = threshold
		self.ykernel = np.matrix([[-1,-2,-1], [0,0,0], [1,2,1]])
		self.xkernel = np.matrix([[-1,0,1], [-2,0,2], [-1,0,1]])
		self.bins = 18
		self.range = [0, 2*np.pi]
		self.channel = [0]
		self.prefix = "HOG"
		
	def compute(self, frame):
		#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		dx = cv2.filter2D(frame, cv2.CV_32F, self.xkernel)
		dy = cv2.filter2D(frame, cv2.CV_32F, self.ykernel)
		orientations = np.zeros_like(dx)
		magnitudes = np.zeros_like(dx)
		cv2.cartToPolar(dx,dy, magnitudes,orientations)
		descriptor = []
		frameH, frameW = frame.shape
		mask_threshold = magnitudes <= self.threshold
		for row in range(self.rows):
			for col in range(self.cols):
				mask = np.zeros_like(frame)
				mask[((frameH/self.rows)*row):((frameH/self.rows)*(row+1)),(frameW/self.cols)*col:((frameW/self.cols)*(col+1))] = 1
				mask[mask_threshold] = 0
				a_, b_ = mask.shape
				hist = cv2.calcHist([orientations], self.channel, mask, [self.bins], self.range)
				hist = cv2.normalize(hist, None)
				descriptor.append(hist)
		return np.concatenate([x for x in descriptor])
