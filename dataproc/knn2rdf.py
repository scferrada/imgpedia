import sys, os, threading, hashlib
from Queue import Queue
import numpy as np

'''
This script reads the CSV of the similarity relations and writes
RDF files containing Image Relations as described in the ontology
of IMGpedia.
'''

if len(sys.argv) != 3:
	print "usage: python knn2rdf.py knn_path output_path"
	exit(0)
	
knn_path = sys.argv[1]
output_path = sys.argv[2]
prefixes= '''@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix imo: <http://imgpedia.dcc.uchile.cl/ontology#> .
@prefix imr: <http://imgpedia.dcc.uchile.cl/resource/> .

'''
desc_types = ['cld','ehd','ghd','hog'] 
MAX_THREADS = 32

def createRDF(buffer):
	while not buffer.empty():
		file, desc = buffer.get()
		counter = 0
		current_outfile = None
		for line in open(file, 'r'):
			if counter % 100000 == 0:
				if current_outfile is not None:
					current_outfile.close()
				current_outfile = open(os.path.join(output_path, desc+file[file.rfind('/')+1:-4]+str(counter)), 'w')
				current_outfile.write(prefixes)
			parts = line.split(';;')
			source = parts[0].strip()
			target = parts[1].strip()
			distance = float(parts[2].strip())
			MD5key = hashlib.md5(source+target+str(distance)+desc).hexdigest()
			simtxt = "imr:%s.%s a imo:ImageRelation ;\n" % (MD5key, desc)
			simtxt += "\timo:sourceImage <http://imgpedia.dcc.uchile.cl/resource/%s> ;\n" % source
			simtxt += "\timo:targetImage <http://imgpedia.dcc.uchile.cl/resource/%s> ;\n" % target
			simtxt += "\timo:distance \"%e\"^^xsd:float ;\n" % distance
			simtxt += "\timo:usesDescriptorType imo:%s .\n\n" % desc.upper()
			simtxt += "<http://imgpedia.dcc.uchile.cl/resource/%s> imo:similar <http://imgpedia.dcc.uchile.cl/resource/%s> .\n\n" % (source, target)
			current_outfile.write(simtxt)
			counter += 1
		buffer.task_done()
			
buffer = Queue()
for type in desc_types:
	for (p,d,f) in os.walk(os.path.join(knn_path, type)):
		for file in [x for x in f if x.endswith('results.txt')]:
			buffer.put((os.path.join(p,file), type))
threads = []			
for i in range(MAX_THREADS):
	t = threading.Thread(target=createRDF, args=(buffer,))
	threads.append(t)
	t.start()
for t in threads:
	t.join()
buffer.join()