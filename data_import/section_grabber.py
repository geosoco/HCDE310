import httplib
import urllib
import urllib2
import simplejson
import csv
import sys


WS_BASE = "https://ws.admin.washington.edu"


# borrowed from online somewhere
# see line below for what to look for
# custom HTTPS opener, banner's oracle 10g server supports SSLv3 only
import httplib, ssl, urllib2, socket
class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
        except ssl.SSLError, e:
            print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)

class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)

# install opener
urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))



def pretty(obj):
    return simplejson.dumps(obj, sort_keys=True, indent=2)

# returns a json object containing a list of classes for the given year, quarter, and department; all fields must be passed
def get_classes(year, quarter, department):
    base_url = "https://ws.admin.washington.edu/student/v4/public/course.json?year="
    class_url = base_url + str(year) + "&quarter=" + quarter + "&future_terms=0&curriculum_abbreviation=" + urllib.quote(department) + "&course_number=&course_title_starts=&course_title_contains=&page_size=500"
    class_string = urllib2.urlopen(class_url).read()
    class_json = simplejson.loads(class_string)
    return class_json



def get_section(url):
    data = urllib2.urlopen(WS_BASE + url).read()
    return simplejson.loads(data)



def find_sections(params):
    url = WS_BASE + "/student/v4/public/section.json?" + urllib.urlencode(params)
    print url

    data = urllib2.urlopen(url).read()
    return simplejson.loads(data)

#
#
# start
#
#

filename = None
if sys.argv is not None and len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    quit()

fieldnames = ["CourseNumber", "CourseTitle", "CourseTitleLong", "CurriculumAbbreviation", "Href", "Quarter", "Year"]



print "reading %s ..."%(filename)
with open(filename, "rt") as data_file:
    csvreader = csv.DictReader(data_file, delimiter=",",  quotechar='"')
    params = {}
    for row in csvreader:
        params['year'] = row['Year']
        params['quarter'] = row['Quarter']
        #params['curriculum_abbreviation'] = row['CurriculumAbbreviation']
        params['curriculum_abbreviation'] = 'ENGL'
        params['page_size'] = '500'
        #params['course_number'] = row['CourseNumber']
        print row['Href']
        sect = get_section(row['Href'])
        print pretty(sect)
        print pretty(find_sections(params))
        quit()
        


quit()
