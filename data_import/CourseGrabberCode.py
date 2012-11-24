import httplib
import urllib
import urllib2
import simplejson
import csv


GWS_HOST  = 'ws.admin.washington.edu'
GWS_PORT  = 443


url = 'https://ws.admin.washington.edu/student/v4/public/college.json?campus_short_name=seattle'

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



r = urllib2.urlopen(url).read()
r_json = simplejson.loads(r)

collegeabbr = {}

# creates a list of departments
for item in r_json["Colleges"]:
    string = item["CollegeAbbreviation"]
    collegeabbr[string] = []
    


years = [2010, 2011, 2012]
quarters = ["autumn", "winter", "spring", "summer"]


#generates a json dictionary of all of the classes specified in the above "years" and "quarters" arrays
for department in collegeabbr:
    print department
    for year in years:
        for quarter in quarters:
            classes = get_classes(year, quarter, department)
            for item in classes["Courses"]:
                collegeabbr[department].append(item)
    #break;

#Takes the dictionary of classes and export it to a .csv file
fieldnames = ["CourseNumber", "CourseTitle", "CourseTitleLong", "CurriculumAbbreviation", "Href", "Quarter", "Year"]
data_file = open("coursedata.csv", "wt")
csvwriter = csv.DictWriter(data_file, delimiter=",", fieldnames=fieldnames)

print "writing csv file..."
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for dept in collegeabbr:
    print dept
    for item in collegeabbr[dept]:
        #print pretty(item)
        csvwriter.writerow(item)
data_file.close()
