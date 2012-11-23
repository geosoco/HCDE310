import httplib
import urllib
import urllib2
import simplejson
import csv


GWS_HOST  = 'ws.admin.washington.edu'
GWS_PORT  = 443

KEY_FILE  = '/path/to/key_file.key'
CERT_FILE = '/path/to/cert_file.cert'

url = 'https://ws.admin.washington.edu/student/v4/public/college.json?campus_short_name=seattle'

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


#generates a json dictionary of all of the classes specficied in the above "years" and "quarters" arrays
for department in collegeabbr:
    for year in years:
        for quarter in quarters:
            classes = get_classes(year, quarter, department)
            for item in classes["Courses"]:
                collegeabbr[department].append(item)
    

#[Does not work] - Intended to take the dictionary of classes and export it to a .csv file
fieldnames = ["Course Number", "Course Title", "Course Title Long", "Curriculum Abbreviation", "Href", "Quarter", "Year"]
data_file = open("coursedata.csv", "wb")
csvwriter = csv.DictWriter(data_file, delimiter=",", fieldnames=fieldnames)
csvwriter.writerow(dict(fn,fn) for fn in fieldnames)
for row in collegeabbr:
    csvwriter.writerow(row)
data_file.close()