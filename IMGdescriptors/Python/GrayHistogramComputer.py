import cv2
import numpy as np
from DescriptorComputer import DescriptorComputer

class GrayHistogramComputer(DescriptorComputer):
	
	def __init__(self, rows, cols,	bins):
		self.rows = rows
		self.cols = cols
		self.bins = bins
		self.range = [0, 256]
		self.channel = [0]
		self.prefix = "GHD"
	
	def compute(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frameH, frameW = frame.shape
		descriptor = []
		for row in range(self.rows):
			for col in range(self.cols):
				mask = np.zeros_like(frame)
				mask[((frameH/self.rows)*row):((frameH/self.rows)*(row+1)),(frameW/self.cols)*col:((frameW/self.cols)*(col+1))] = 1
				hist = cv2.calcHist([frame], self.channel, mask, [self.bins], self.range)
				hist = cv2.normalize(hist, None)
				descriptor.append(hist)
		return np.concatenate([x for x in descriptor])
