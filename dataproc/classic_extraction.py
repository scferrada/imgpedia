import os, sys, threading, cv2
from Queue import Queue, Empty
import numpy as np
from GrayHistogramComputer import GrayHistogramComputer
from EdgeHistogramComputer import EdgeHistogramComputer
from OrientedGradientsComputer import OrientedGradientsComputer
from ColorLayoutComputer import ColorLayoutComputer

'''
This script iterates through the images from <i>input</i> and computes three descriptors.
Results are numpy vectors stored in <i>output</i> folder.
Number of threads and descriptor parameters must be changed from the code.
The code asumes the data is stored as Wikimedia Commons images folders.
'''

if len(sys.argv)<3:
	print "usage: classic_extraction.py input output"
	exit(-1)
	
input_folder = sys.argv[1]
output_folder = sys.argv[2]
MAX_THREADS = 28

class ExtractorThread(threading.Thread):
	def __init__(self, folders, inpath, outpath):
		super(ExtractorThread, self).__init__()
		self.folders = folders
		self.inpath = inpath
		self.outpath = outpath
		self.computers = []
		self.computers.append(GrayHistogramComputer(4,4,16))
		self.computers.append(OrientedGradientsComputer(4,4,150))
		self.computers.append(ColorLayoutComputer())
	
	def run(self):
		while not self.folders.empty():
			current_folder = self.folders.get()
			print "working on %s" % current_folder
			path = os.path.join(self.inpath, current_folder)
			files = []
			for (dirpath, dirnames, filenames) in os.walk(path):
				files.extend(filenames)
				break
			if len(files) == 0:
				for line in open(current_folder[-2:]+".ls"):
					files.append(line.strip())
			valid_files = [x for x in files if x[x.rfind('.'):].lower() in [".png", ".jpg", ".jpeg"]]
			print "%d valid files for %s" % (len(valid_files), current_folder)
			count = 0
			for file in valid_files:
				desc_folder = os.path.join(self.outpath, current_folder, file[:200])
				if not os.path.exists(desc_folder):
					os.makedirs(desc_folder)
				else:
					continue
				img = cv2.imread(os.path.join(path, file))
				if img is not None:
					count += 1
					for computer in self.computers:
						desc = computer.compute(img)
						np.save(open(os.path.join(desc_folder, file[:200]+"."+computer.prefix) , 'w'), desc)
				else:
					os.rmdir(desc_folder)
			self.folders.task_done()
			print "Done with %s" % current_folder
			output_resume = open(os.path.join(self.outpath, current_folder[2:]+".txt"), "w")
			output_resume.write("%d out of %d descriptors calculated" % (count, len(valid_files)))
			output_resume.close()
		
folders = Queue()
digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
for i in digits:
	for j in digits:
		folders.put(os.path.join(i, i+j))
threads = []
print "launching threads"
for i in range(MAX_THREADS):
	t = ExtractorThread(folders, input_folder, output_folder)
	threads.append(t)
	t.start()
print "waiting for join"
for t in threads:
	t.join()
folders.join()