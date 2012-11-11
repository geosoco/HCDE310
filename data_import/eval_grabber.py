__author__ = 'soco'

import mechanize
import re
from bs4 import BeautifulSoup
import sys
import urlparse
import os

from types import *


url_base = "https://www.washington.edu/cec/"
subdir = "./cec/"
br = None

def get_page(url):
    global br
    if br is None:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        #br.set_debug_redirects(True)
        #br.set_debug_responses(True)
        #br.set_debug_http(True)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.10 Safari/537.11')]
    br.open(url)

    form_redirects_finished = False
    counter = 0

    while form_redirects_finished == False and counter < 10:
        #print "Counter: " + str(counter) + "(" + str(form_redirects_finished) + ")"
        #print
        counter = counter + 1
        # printing options
        if not br.forms():
            form_redirects_finished = True
            #print "-"
        else:
            has_redirect_form = False
            for form in br.forms():
                #print form.name
                if not form:
                    form_redirects_finished = True
                elif form.name == "relay":
                    br.select_form(name="relay")
                    br.submit()
                    has_redirect_form = True
                    break
                elif form.name == "query":
                    br.select_form(name="query")
                    br.form.find_control("user").value = sys.argv[1]
                    br.form.find_control("pass").value = sys.argv[2]
                    br.submit()
                    has_redirect_form = True
                    break
            form_redirects_finished = not has_redirect_form

    #print 'done'
    #print
    #print br.response().get_data()
    soup = BeautifulSoup(br.response().get_data(),from_encoding="iso-8859-1")
    return soup



soup = get_page("https://www.washington.edu/cec/toc.html")

letters = map(lambda x: re.match(r"(\w+)\-toc.html$",x['href']).group(1), soup.find_all(href=re.compile("-toc.html$")))
for letter in letters:
    br = None
    letter_url = url_base + letter + "-toc.html"
    print letter + ":" + letter_url

    soup2 = get_page(letter_url)

    path = subdir + letter + "/"
    if not os.path.exists(path):
        os.makedirs(path)

    pages = soup2.body.find_all('a', href=re.compile('^\w/[\w\d]+\.html'))
    for i in pages:
        review_page = get_page(url_base + i['href'])
        print i['href']
        filename = subdir + re.match(r"(\w+\/[\w\d]+\.html)$",i['href']).group(0)
        print filename
        with open(filename,"w") as f:
            f.write(review_page.prettify("iso-8859-1"))
            f.close()

