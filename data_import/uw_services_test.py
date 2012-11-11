__author__ = 'soco'

import os
import sys
import requests

import httplib
import urllib3
import simplejson as json


GWS_HOST  = 'ws.admin.washington.edu'
GWS_PORT  = 443

KEY_FILE  = '/path/to/key_file.key'
CERT_FILE = '/path/to/cert_file.cert'

url = 'https://ws.admin.washington.edu/student/v4/public/course/2009,winter,MUSAP,218.json'


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

if __name__ == "__main__":
    r = urllib2.urlopen('https://ws.admin.washington.edu/student/v4/public/college.json?campus_short_name=seattle')
    #print(JSON.stringify( r.read()))

    s= r.read()

    print json.dumps(json.loads(s), sort_keys=True, indent=4 * ' ')

exit(0)


my_config = {
    'verbose': sys.stdout,
    'prefetch': False,
    'safe_mode': False,
    'max_retries': 5,
    'max_redirects': 30,
    'encode_uri': False
}

my_headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #'Accept-Charset':'ISO-8859-1,utf-8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'en-US,en',
    'Cache-Control': 'max-age=0',
    'Connection':'keep-alive',
    'Host': GWS_HOST,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20100101 Firefox/16.0',
    #'X-UW-Act-as': 'soco',
    'If-None-Match': 'W1CEvHmwv+bWeZJxoawwrw==',

}

def print_url(args):
    print args
    print args.url
    print args.config
    print args.headers
    #print keys(args)
    #print args['url']

r = requests.get(url, config=my_config, verify=False, prefetch=False, headers=my_headers, hooks=dict(pre_request=print_url))
if not r is None:
    print 'error'
else:
    print 'success'


exit(0)





opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Graasca/5.0'), ('Accept', 'application/json'), ('Content-Type', 'application/json; charset=UTF-8')]
f = opener.open(url)
print f.read(100)
exit(0)


f = urllib2.urlopen(url)
print f.read(100)
exit(0)


connection = httplib.HTTPSConnection(GWS_HOST, GWS_PORT)
connection.set_debuglevel(100)


# do stuff
print "Getting"
connection.request("GET", "/student/v4/public/course/2009,winter,MUSAP,218.json")
r1 = conn.getresponse()
print r1.status, r1.reason
data1 = r1.read()
print data1

connection.close()

exit(0)
