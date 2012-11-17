__author__ = 'soco'

import mechanize
import re
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from lxml import etree
import sys
import os
from optparse import OptionParser


subdir = "./cec/"

types = {}
forms = {}

def get_page(filename):
    f = open(filename,"r")
    soup = BeautifulSoup(f.read(),from_encoding="iso-8859-1")
    return soup



re_parser1 = re.compile(r"([\w& \.\(\)]+?)([A-Z ]{3,7})\s*(\d{1,3})?\s*(\w)*$")
re_parser2 = re.compile(r"([\w\-\'\(\) \*]+)\s{2,4}([\w\- ]+)\s{2,4}(\w\w\d\d)")


#re_parser = re.compile(r"([\w& \.\(\)]+) ([A-Z ]{2,6}) (\d+)\s+(\w+)?\s+([\w\-\'\(\) \*]+)\s{2,4}([\w\- ]+)\s{2,4}(\w\w\d\d)")

cnt = 0

# configurable argv
if sys.argv is not None:
    subdir = sys.argv[1]


for root, dirs, files in os.walk(subdir):
    #print root
    for name in files:
        filename = os.path.join(root,name)
        #print "    ",  filename
        evalsoup = get_page(filename)

        caption = evalsoup.find('caption').text.replace(u"\xa0", " ")
        #print caption
        details = re.match("\s*Form ([\d\w]+):\s*([\w\s\/-]+)\s{4,10}\"(\d+)\" surveyed\s*\"(\d+)\"\s+enrolled", caption)

        form = details.group(1).strip()
        form_name = details.group(2).strip()
        if form not in forms:
        	forms[form] = form_name

        rows = evalsoup.find_all('tr')[1:]
        for r in rows:
        	val = r.find_all('td')[0].text.strip()
        	if val not in types:
        		types[val] = set()
        	types[val].add(details.group(1).strip())
        	

for f in sorted(forms):
	print "%s: %s"%(f,forms[f])

#print sorted(types)
for t in types.keys():
	#l = t + " : " + ",".join(sorted(types[t]))
	print "%s : %s"%(t, ",".join(sorted(types[t])))

