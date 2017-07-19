import numpy as np
import cv2, sys, os
from datetime import datetime
from OrientedGradientsComputer import OrientedGradientsComputer
from GrayHistogramComputer import GrayHistogramComputer
from DeCAF7Computer import DeCAF7Computer
from ColorLayoutComputer import ColorLayoutComputer

'''
This scripts computes the time it takes to compute the descriptors using a given set of images.
'''

if len(sys.argv)<3:
	print "Usage: python descriptor_benchmark.py image_path output_path"
	exit(-1)

image_path = sys.argv[1]
output_path = sys.argv[2]
CLDComputer = ColorLayoutComputer()
HOGComputer = OrientedGradientsComputer(2,2,100)
GHistComputer = GrayHistogramComputer(2,2,32)
DeCAFComputer = DeCAF7Computer()

images = os.listdir(image_path)
images = [x for x in images if (x.endswith(".jpg") or x.endswith(".JPG") or x.endswith(".png"))]
images_amount = len (images)
print "Computing descriptors for %d files" % images_amount

print "Computing CLD..."
start = datetime.now()
for image in images:
	img = cv2.imread(os.path.join(image_path, image))
	if img is None: continue
	decaf = CLDComputer.compute(img)
	if decaf is None: 
		print image
		continue
	np.save(open(os.path.join(output_path, image[:200]+".cld"), "w"), decaf)
end = datetime.now()
total_time = (end - start).total_seconds()
print "CLD finished in %d seconds. %.8f seconds per image" % (total_time, total_time/images_amount)
file = open("CLD results.txt", "w")
file.write("CLD finished in %d seconds. %.8f seconds per image" % (total_time, total_time/images_amount))
file.close()

print "Computing HOG..."
start = datetime.now()
for image in images:
	img = cv2.imread(os.path.join(image_path, image))
	if img is None: continue
	hog = HOGComputer.compute(img)
	np.save(open(os.path.join(output_path, image[:200]+".hog"), "w"), hog)
end = datetime.now()
total_time = (end - start).total_seconds()
print "HOG finished in %d seconds. %.8f seconds per image" % (total_time, total_time/images_amount)
print "Computing EHD..."
start = datetime.now()
for image in images:
	img = cv2.imread(os.path.join(image_path, image))
	if img is None: continue
	ehd = EHDComputer.compute(img)
	np.save(open(os.path.join(output_path, image[:200]+".ehd"), "w"), ehd)
end = datetime.now()
total_time = (end - start).total_seconds()
print "EHD finished in %d seconds. %.8f seconds per image" % (total_time, total_time/images_amount)
print "Computing Gray histogram..."
start = datetime.now()
for image in images:
	img = cv2.imread(os.path.join(image_path, image))
	if img is None: continue
	ghist = GHistComputer.compute(img)
	np.save(open(os.path.join(output_path, image[:200]+".ghist"), "w"), ghist)
end = datetime.now()
total_time = (end - start).total_seconds()
print "Gray histogram finished in %d seconds. %.8f seconds per image" % (total_time, total_time/images_amount)
print "Computing DeCAF7..."
start = datetime.now()
for image in images:
	img = cv2.imread(os.path.join(image_path, image))
	if img is None: continue
	decaf = DeCAFComputer.compute(img)
	np.save(open(os.path.join(output_path, image[:200]+".decaf"), "w"), decaf)
end = datetime.now()
total_time = (end - start).total_seconds()
print "DeCAF7 finished in %d seconds. %.8f seconds per image" % (total_time, total_time/images_amount)