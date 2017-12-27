import os, sys

'''
This script takes the CSV resulting from the join between the images of
Wikimedia Commons and the Wikipedia articles and produces RDF files containing
the relation appears in described in the ontology of IMGpedia.
'''

if len(sys.argv) != 3:
	print "usage: python semanticlinks.py input_file output_file"
	exit(1)
	
input_file = sys.argv[1]
output_file = sys.argv[2]

prefixes = "@prefix imo: <http://imgpedia.dcc.uchile.cl/ontology#>\n\n"

imgpedia_pattern = "<http://imgpedia.dcc.uchile.cl/resource/%s>"
dbpedia_pattern = "<http://dbpedia.org/resource/%s>"
wikipedia_pattern = "<http://en.wikipedia.org/wiki/%s>"
counter= 0

with open(input_file, "r") as csv:
	with open(output_file, "w") as links:
		links.write(prefixes)
		for line in csv:
			parts = line.split("\t")
			if parts[0][parts[0].rfind('.'):].lower() not in [".png", ".jpg", ".jpeg"]:
				continue
			counter += 1
			resource = parts[1].strip()[:-3]
			txt = "%s imo:appearsIn %s ;\n" % ((imgpedia_pattern % parts[0]),(wikipedia_pattern % resource))
			txt += "\timo:associatedWith %s .\n" % (dbpedia_pattern % resource)
			links.write(txt)
			if counter%100000 == 0:
				print "%d images written" % counter
