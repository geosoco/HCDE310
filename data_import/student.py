import httplib
import ssl
import urllib
import urllib2
import socket
import simplejson


# borrowed from online somewhere
# see line below for what to look for
# custom HTTPS opener, banner's oracle 10g server supports SSLv3 only
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



#
#
#
def get_json_data(url):
    data = urllib2.urlopen(url).read()
    return simplejson.loads(data)


#
#
#
def get_student_json_data(method, params):
    params_str = urllib.urlencode(params)
    return get_json_data("https://ws.admin.washington.edu/student/v4/public/" + method + ".json?" + params_str)


#
#
#
def get_curriculum_data(year, quarter):
    return get_student_json_data('curriculum', {'year': year, 'quarter': quarter })

#
# returns a json object containing a list of classes for the given year, quarter, and department; all fields must be passed
#
def get_classes(year, quarter, department):
    params['year'] = year
    params['quarter'] = quarter
    params['curriculum_abbreviation'] = urllib.quote(department)
    params['page_size'] = 500
    return get_student_json_data('course', params)

    #base_url = "https://ws.admin.washington.edu/student/v4/public/course.json?year="
    #class_url = base_url + str(year) + "&quarter=" + quarter + "&future_terms=0&curriculum_abbreviation=" + urllib.quote(department) + "&course_number=&course_title_starts=&course_title_contains=&page_size=500"
    #class_string = urllib2.urlopen(class_url).read()
    #class_json = simplejson.loads(class_string)
    #return class_json


#
#
#
def get_class_data(url):
    return get_json_data("https://ws.admin.washington.edu" + url)

