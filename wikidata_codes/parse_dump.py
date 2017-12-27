import argparse, re, gzip

parser = argparse.ArgumentParser(description='Parses RDF files and outputs RDF for IMGpedia')

parser.add_argument('input_gzip', type=str, help='The GZip file with the data from Wikimedia')
parser.add_argument('input_ttl', type=str, help='The ttl file with the data from IMGpedia associations')
parser.add_argument('output_file', type=str, help='The file name for the output')

args = parser.parse_args()

datafile = gzip.open(args.input_gzip, 'rb')

label = '<http://www.w3.org/2000/01/rdf-schema#label>'
description = '<http://schema.org/description>'
name = '<http://schema.org/name>'
preflabel = '<http://www.w3.org/2004/02/skos/core#prefLabel>'
altlabel = '<http://www.w3.org/2004/02/skos/core#altLabel>'
wikidata = '<http://www.wikidata.org/entity/(.+?)>'
dbpedia = '<http://dbpedia.org/resource/%s>'
text = '"(.+?)"'
pattern = '%s <http://imgpedia.dcc.uchile.cl/ontology#associatedWith> %s.\n'

pairs = {}

for line in datafile:
	line = line.decode('unicode_escape')
	if label in line:
		parts = line.split(label)
	elif description in line:
		parts = line.split(description)
	elif name in line:
		parts = line.split(name)
	elif preflabel in line:
		parts = line.split(preflabel)
	elif altlabel in line:
		parts = line.split(altlabel)
	else:
		print(line)
		continue
	if len(parts) != 2:
		print(parts)
		continue
	try:
		entity = re.search(wikidata, parts[0]).group(0)
		wikiname = re.search(text, parts[1]).group(1)#.decode('utf-8')
		dbname = dbpedia % wikiname
		dbname = dbname.replace(' ','_').lower()
		pairs[dbname] = entity
		
	except AttributeError:
		print("entity not found in %s" % parts[0])
		continue

associatedWith = 'imo:associatedWith'	
appearsIn = 'imo:appearsIn'	
		
with open(args.output_file, 'w') as outfile:
	current_img = None
	for line in open(args.input_ttl):
		if appearsIn in line:
			current_img = line.split(appearsIn)[0].strip()
			continue
		if associatedWith in line:
			dbname = line.split(associatedWith)[1][:-2].strip().lower()
			if not dbname in pairs:
				print("%s not in pairs" % dbname)
				continue
			outfile.write(pattern % (current_img, pairs[dbname]))		