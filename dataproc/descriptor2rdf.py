import sys, os, threading, Queue
import numpy as np

'''
This scripts converts the numpy vectors of the descriptors into RDF 
files according to the IMGpedia ontology
'''

if len(sys.argv) != 3:
	print "usage: python descriptor2rfd.py descriptor_path output_path"
	exit(-1)
	
descriptor_path = sys.argv[1]
output_path = sys.argv[2]

MAX_THREADS = 24
folders = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
images = "images"
descriptors = "descriptors"
prefixes_desc = "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n@prefix imo: <http://imgpedia.dcc.uchile.cl/ontology#> .\n@prefix imr: <http://imgpedia.dcc.uchile.cl/resource/> .\n"
prefixes_im = prefixes_desc + "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n@prefix dbcr: <http://commons.dbpedia.org/resource/File:>\n\n"
error_log = "rdf_errors.txt"
descriptor_map = {"CLD": "CLD", "GHD":"GHD", "HOG":"HOG"}

def writeRDF(buffer):
	while not buffer.empty():
		folder, subfolder = buffer.get()
		print "working on %s" % subfolder
		img_dirs = []
		for path, dirs, files in os.walk(os.path.join(descriptor_path,folder,subfolder)):
			img_dirs.extend(dirs)
			break
		for img_dir in img_dirs:
			out_images = os.path.join(output_path, images, folder, subfolder)
			out_descriptors = os.path.join(output_path, descriptors, folder, subfolder)
			if not os.path.exists(out_images):
				os.makedirs(out_images)
			if not os.path.exists(out_descriptors):
				os.makedirs(out_descriptors)
			#write rdf file for visual entity
			image_rdf = open(os.path.join(out_images, img_dir), "w")
			image_rdf.write(prefixes_im)
			txt = "imr:%s a imo:Image ;\n" % img_dir
			txt += "\timo:folder %s ;\n" % folder
			txt += "\timo:subfolder %s ;\n" % subfolder
			txt += "\towl:sameAs dbcr:%s ;\n" % img_dir
			image_rdf.write(txt)
			image_rdf.close()
			#write rdf files for each descriptor
			for path, dirs, files in os.walk(os.path.join(descriptor_path, folder, subfolder, img_dir)):
				if len(files) < 3:
					e = open(error_log, "a")
					txt = "File %s/%s/%s has only %d descriptors\n" % (folder, subfolder, img_dir, len(files))
					e.write(txt)
					e.close()
				for descriptor_file in files:
					descriptor = np.load(os.path.join(descriptor_path, folder, subfolder,img_dir,descriptor_file))
					descriptor_rdf = open(os.path.join(out_descriptors, descriptor_file), "w")
					descriptor_rdf.write(prefixes_desc)
					extension = descriptor_map[descriptor_file[-3:]]
					txt = "\nimr:%s a imo:%s ;\n" % (descriptor_file[:-3] + extension, extension)
					txt += "\timo:describes imr:%s ;\n" % (img_dir)
					txt += "\timo:value \"%s\" ." % (np.array2string(descriptor.T[0], separator=',', max_line_width=100000))
					descriptor_rdf.write(txt)
					descriptor_rdf.close()
				break
		buffer.task_done()
		print "subfolder %s done" % subfolder

buffer = Queue.Queue()
for folder in folders:
	for subfolder in folders:
		buffer.put((folder,  folder+subfolder)) 
print "launching threads"
threads = []
for i in range(MAX_THREADS):
	t = threading.Thread(target=writeRDF, args=(buffer,))
	threads.append(t)
	t.start()
buffer.join()
	
for t in threads:
	t.join()