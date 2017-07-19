import os, sys, threading, Queue
import numpy as np

MAX_THREADS = 40

if len(sys.argv) != 4:
	print "usage: python flann_settings.py input_path output_path preffix"
	exit(1)
	
	
'''
This script reads the descriptors and builds FLANN data and dictionaries for post parsing.
It outputs a descriptor matrix for each image bucket.
'''
base_input_path = sys.argv[1]
base_output_path = sys.argv[2]
prefix = sys.argv[3]

folders = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
sub_folders = ["0","1","2", "3", "4","5","6","7","8","9","a","b","c","d","e","f"]

def read_folder(buffer):
	while not buffer.empty():
		folder, subfolder = buffer.get()
		first = True
		counter = 0
		path = os.path.join(base_input_path, folder, folder+subfolder)
		print "reading %s" % path
		dirs = []
		map = {}
		for (dirpath, dirnames, filenames) in os.walk(path):
			dirs.extend(dirnames)
			break
		dataset = None
		for dir in dirs:
			try:
				desc = np.load(os.path.join(path, dir, (dir + prefix)) )
			except IOError:
				continue
			counter += 1
			if first:
				dataset = desc.T
				first = False
			else:
				dataset = np.vstack((dataset, desc.T))
			map[counter - 1] = dir
		output_path = os.path.join(base_output_path, folder, folder+subfolder)
		if not os.path.exists(output_path):
			os.makedirs(output_path)
		np.save(open(os.path.join(output_path, folder+subfolder+".npy"), "w"), dataset)
		mapfile = open(os.path.join(output_path, folder+subfolder+"_dict.txt"), "w")
		for key in map:
			txt = "%d ;; %s\n" % (key, map[key])
			mapfile.write(txt)
		mapfile.close()
		buffer.task_done()

buffer = Queue.Queue()
for folder in folders:
	for subfolder in sub_folders:
		buffer.put((folder, subfolder))

threads = []		
for i in range(MAX_THREADS):
	t = threading.Thread(target=read_folder, args=(buffer,))
	threads.append(t)
	t.start()
for thread in threads:
	thread.join()
buffer.join()