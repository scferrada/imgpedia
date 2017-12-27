# -- coding: utf-8 -- 

import urllib as url
import urllib2 as url2
import json, argparse, shelve, re, time
from httplib import BadStatusLine

parser = argparse.ArgumentParser(description='Reads all appearsIn relations and finds')
parser.add_argument('ttl', type=str, help='Path to the ttl file')

args = parser.parse_args()

wiki_api = 'https://en.wikipedia.org/w/api.php'

vals = {
	"action":"query",
	"prop":"pageprops",
	"ppprop":"wikibase_item",
	"redirects":1,
	"format" : "json"
}

header = {'Content-Type': 'application/json', 'User-Agent': 'sferrada@dcc.uchile.cl'}
articles = shelve.open('articles.db')
pattern = re.compile('wikipedia.org/wiki/(.*)>')
count = 0

fails = shelve.open('fails.db')

for line in open(args.ttl):
	if 'appearsIn' in line:
		try:
			article = pattern.search(line).group(1).replace("\\'", "'")
			if articles.has_key(article) or fails.has_key(article):
				continue
			#print article
			#exit(1)
			vals["titles"]= article#url2.quote(article)
			params = url.urlencode(vals)
			request = url2.Request(wiki_api, params, header)
			response = url2.urlopen(request)	
			data = json.load(response)
			if "query" not in data:
				time.sleep(1)
				fails[article] = 1
				continue
			if "pages" not in data["query"]:
				time.sleep(1)
				fails[article] = 1
				continue
			pages = data["query"]["pages"]
			identifiers = []
			for page in pages:
				try:
					identifiers.append(pages[page]["pageprops"]["wikibase_item"])
				except KeyError as e:
					print "key not found for article %s" % article
					#print e
			if len(identifiers) == 0:
				time.sleep(1)
				fails[article] = 1
				continue
			articles[article] = identifiers
			count += 1
			if count% 1000 == 0:
				print "%d articles obtained" % count
			time.sleep(1)
		except url2.URLError, e:
			print 'Got an error code:', e
		except BadStatusLine, f:
			print 'Got a bad status response:', f
		