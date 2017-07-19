import threading, os, sys
import numpy as np

'''
This script parses the results from flann_parallel_search.py.
Its output is a CSV of the form (img1, img2, distance), iff img2 is within
the 10-ANN of img1.
'''

if len(sys.argv) != 4:
	print "usage: python flann_parse_results.py dict_path result_path output_path"
	exit(-1)
	
dict_path = sys.argv[1]
result_path = sys.argv[2]
output_path = sys.argv[3]
folders = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

def clean(folder):
	print "cleaning " + folder
	dict_names = []
	for (path, dirs, files) in os.walk(os.path.join(dict_path, folder)):
		dict_names.extend([os.path.join(path,x) for x in files if x.endswith("_dict.txt")])
	dict_names.sort()
	counter = 0
	parsed_dict = {}
	
	#build parsed dict
	for dict_filename in dict_names:
		for line in open(dict_filename):
			line = line.strip()
			if line == "": continue
			parts = line.split(";;")
			parsed_dict[counter] = parts[1].strip()
			counter += 1
	outname = folder + "_parsed.txt"
	outfile = open(os.path.join(output_path, outname), "w")
	for key in parsed_dict:
		txt = "%d ;; %s\n" % (key, parsed_dict[key])
		outfile.write(txt)
	outfile.close()
	
def parse(folder_id, parsed_dicts):
	folder_dict = parsed_dicts[folder_id]
	parsed_results = {}
	for folder in folders:
		print "parsing search of %s in %s" % (folder_id, folder)
		results = np.load(os.path.join(result_path, folder_id +"_"+ folder + "result.txt"))
		print results.shape
		distances = np.load(os.path.join(result_path, folder_id +"_"+ folder + "distances.txt"))
		current_dict = parsed_dicts[folder]
		counter = 0
		for row in results:
			source_img = folder_dict[str(counter)]
			targets = []
			j = 0
			for col in row:
				target_img = current_dict[str(col)]
				distance = distances[counter][j]
				targets.append((target_img, distance))
				j += 1
			if source_img not in parsed_results:
				targets = [x for x in targets if x[1]>0]
				targets.append(('',float("inf")))
				parsed_results[source_img] = targets
			else:
				for target, distance in targets:
					max_dist = max([x[1] for x in parsed_results[source_img]])
					if distance < max_dist and distance > 0:
						max_index = [x[1] for x in parsed_results[source_img]].index(max_dist)
						parsed_results[source_img][max_index] = (target, distance)
			counter += 1
	print "writing output for %s" % folder_id
	outfile = open(os.path.join(output_path, folder_id+"results.txt"), "w")
	for key in parsed_results:
		for target, distance in parsed_results[key]:
			txt = ("%s ;; %s ;; %e\n") % (key, target, distance)
			outfile.write(txt)
	outfile.close()
	
clean_threads = []
for folder in folders:
	t = threading.Thread(target=clean, args=(folder, ))
	clean_threads.append(t)
	t.start()
for t in clean_threads:
	t.join()
	
print "generating dictionaries"
parsed_dicts = {}
for folder in folders:
	parsed_dicts[folder] = {}
	for line in open(os.path.join(output_path, folder + "_parsed.txt")):
		parts = line.split(";;")
		index = parts[0].strip()
		value = parts[1].strip()
		#print value
		#exit(-1)
		parsed_dicts[folder][index] = value

print "parsing..."
parse_threads = []
for folder in folders:
	t = threading.Thread(target=parse, args=(folder, parsed_dicts))
	parse_threads.append(t)
	t.start()
for t in parse_threads:
	t.join()