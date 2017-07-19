import os, sys, threading, Queue
from PIL import Image

'''
This scripts generates RDF files containing the Visual Entities,
according to the ontology of IMGpedia.
'''

if len(sys.args) !=3:
	print "usage: python imagesize2rdf.py image_path rdf_path"
	exit(-1)
	
image_path = sys.argv[1]
rdf_path = sys.argv[2]

folders = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
MAX_THREADS = 24

def writeRDF(buffer):
	while not buffer.empty()
		folder, subfolder = buffer.get()
		print "working with %s" % subfolder
		image_filenames = []
		for path, dirs, files in os.walk(os.path,join(image_path, folder, subfolder)):
			image_filenames.extend(files)
			break
		if len(image_filenames) == 0:
			lsfile = open(subfolder+".ls")
			for line in lsfile:
				dirs.append(line.strip())
		for image in image_filenames:
			im = Image.open(os.path.join(image_path, folder, subfolder, image))
			width, height = im.size
			image_rdf = open(os.path.join(rdf_path, folder, subfolder, image), "a")
			txt = "\timo:height %d ;\n" % height
			txt += "\timo:width %d ;\n" %width
			image_rdf.write(txt)
			image_rdf.close()
		buffer.task_done()
	
buffer = Queue.Queue()
for folder in folders:
	for subfolder in folders:
		buffer.put((folder, folder + subfolder))
		
threads = []
for i in range(MAX_THREADS):
	t = threading.Thread(target=writeRDF, args=(buffer,))
	threads.append(t)
	t.start()
for t in threads:
	t.join()
buffer.join()