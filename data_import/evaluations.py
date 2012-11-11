__author__ = 'soco'

import mechanize
import re
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from lxml import etree
import sys
import os


subdir = "./cec/"



def get_page(filename):
    f = open(filename,"r")
    soup = BeautifulSoup(f.read(),from_encoding="iso-8859-1")
    return soup



re_parser1 = re.compile(r"([\w& \.\(\)]+?)([A-Z ]{3,7})(\d{0,3})?\s*(\w+)?$")
re_parser2 = re.compile(r"([\w\-\'\(\) \*]+)\s{2,4}([\w\- ]+)\s{2,4}(\w\w\d\d)")


#re_parser = re.compile(r"([\w& \.\(\)]+) ([A-Z ]{2,6}) (\d+)\s+(\w+)?\s+([\w\-\'\(\) \*]+)\s{2,4}([\w\- ]+)\s{2,4}(\w\w\d\d)")

cnt = 0

for root, dirs, files in os.walk(subdir):
    print root
    for name in files:
        filename = os.path.join(root,name)
        #print "    ",  filename
        evalsoup = get_page(filename)

        str1 = evalsoup.find('h1').text.strip().replace(u"\u00A0", " ")
        str2 = evalsoup.find('h2').text.strip().replace(u"\u00A0", " ")
        #print str1
        #print str2
        m = re_parser1.search(str1)
        #print len(m.groups())
        #print m.groups()
        m2 = re_parser2.search(str2)
        if m == None or m2 == None:
            print "fail 0: \"%s\" \"%s\" -- None" %(str1, str2)
        elif len(m.groups()) != 4:
            print "fail 1: %s %s -- %s %s" %(str1, str2, m.groups(), m2.groups())
        if len(m2.groups()) != 3:
            print "fail 2: ", str1, str2

        left = m.group(1).strip() + "," + m.group(2).strip() + "," + ("" if m.group(3) == None else m.group(3).strip()) + "," + ("" if m.group(4) == None else m.group(4).strip())

        caption = evalsoup.find('caption').text.replace(u"\xa0", " ")
        #print caption
        details = re.match("\s*Form ([\d\w]+):\s*([\w\s\/-]+)\s{4,10}\"(\d+)\" surveyed\s*\"(\d+)\"\s+enrolled", caption)
        if details is not None:
            #line = line + "," + ",".join(m.groups())
            #print "<" + ",".join(details.groups()) + ">"
            survey = ",".join(map(lambda d: d.strip(),details.groups()))
        else:
            print filename
            survey = ",,,,"

        #print str1
        rows = evalsoup.find_all('tr')[1:]
        right = ",".join(map(lambda r: ",".join(map(lambda y: y.text.strip("% \r\n\t"), r.find_all('td')[1:])) , rows ))
        print str1 + "||" + left + "," + survey + "," +  ",".join(map(lambda g: g.strip() , m2.groups())) + "," + right






exit(0)

soup = get_page("https://www.washington.edu/cec/toc.html")



#print soup.prettify()

letters = map(lambda x: "https://www.washington.edu/cec/" + x['href'], soup.find_all(href=re.compile("-toc.html$")))
for letter in letters:
    br = None
    #toc = "https://www.washington.edu/cec/" + soup.find(href=re.compile("-toc.html$"))['href']
    soup = get_page(letter)

    #print soup.prettify()
    pages = soup.body.find_all('a', href=re.compile('^\w/[\w\d]+\.html'))
    re_parser = re.compile(r"([\w& \.\(\)]+) ([A-Z ]{2,6}) (\d+)\s+(\w+)?\s+([\w\-\'\(\) \*]+)\s{2,4}([\w\- ]+)\s{2,4}(\w\w\d\d)")
    count = 0
    toc_letter = re.match(r".+\/(\w+)-toc.html$", letter).groups()[0]
    f = file("cec-" + toc_letter  + ".csv", "w+")
    #print "found " + str(len(pages)) + " pages"
    for i in pages:
        count = count + 1
        #print "\t" + i['href']
        # replace all non-breaking spaces with spaces
        s = i.text.replace(u"\u00A0", " ")
        # do the regex
        m = re_parser.match(s)
        if m is None or m is NoneType or m.groups() is None or m.groups() is NoneType:
            print "error: " + s
            continue

        #if not m is None:
        #    print m.groups()

        evalpage = "https://www.washington.edu/cec/" + i['href']
        #print evalpage
        #print
        #print
        evalsoup = get_page(evalpage)

        #print evalsoup.prettify()

        left = ",".join(m.groups())

        rows = evalsoup.find_all('tr')[1:]
        right = ",".join(map(lambda r: ",".join(map(lambda y: y.text.strip(), r.find_all('td')[1:])) , rows ))

        line = left + "," + right
        caption = evalsoup.find('caption').text.replace(u"\xa0", " ")
        details = re.match("Form\s([\d\w]+):\s+([\w\s\/]+)\s{5,8}\"(\d+)\"\s+surveyed\s+\"(\d+)\"\s+enrolled", caption)
        if not details is None:
            line = line + "," + ",".join(m.groups())


        #print left + "," + right
        f.write( line + "\n")

        #if count > 10: break;

        #for row in rows[1:]:
        #    cells = row.find_all('td')
        #    print cells[1:7].join(',')


        #percents = evalsoup.find_all('td',text=re.compile('\d+\%'))
        #print len(percents)
        #for k in percents:
        #    print k.text

        #print evalsoup.body.find("")

        #break
        #else:
        #    print "--"
        #for g in match.groupdict():
        #    if not g is None:
        #        print g + ", "
        #print i.text.encode("utf-8") + " : " + i['href']
        #for ch in s:
        #    print hex(ord(ch)) + "'" + ch + "'"
    f.close()