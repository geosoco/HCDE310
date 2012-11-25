import httplib
import urllib
import urllib2
import simplejson
import csv
import student

college_url = 'https://ws.admin.washington.edu/student/v4/public/curriculum.json'





def get_json_data(url):
    data = urllib2.urlopen(url).read()
    return simplejson.loads(data)


def get_student_json_data(method, params):
    params_str = urllib.urlencode(params)
    return get_json_data("https://ws.admin.washington.edu/student/v4/public/" + method + ".json?" + params_str)


def get_curriculum_data(year, quarter):
    return get_student_json_data('curriculum', {'year': year, 'quarter': quarter })

# returns a json object containing a list of classes for the given year, quarter, and department; all fields must be passed
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


def get_class_data(url):
    return get_json_data("https://ws.admin.washington.edu" + url)




#
#
# start
#
#


years = range(2012,2013)
#quarters = ["autumn", "winter", "spring", "summer"]
quarters = ["autumn"]

curriculums = {}


for y in years:
    for q in quarters:
        c_data = get_curriculum_data(y,q)
        print pretty(c_data)
        quit()


r = urllib2.urlopen(college_url).read()
r_json = simplejson.loads(r)
print r_json

collegeabbr = {}

# creates a list of departments
for item in r_json["Colleges"]:
    string = item["CollegeAbbreviation"]
    collegeabbr[string] = {}
    




#generates a json dictionary of all of the classes specified in the above "years" and "quarters" arrays
for department in collegeabbr:
    print department
    for year in years:
        for quarter in quarters:
            classes = get_classes(year, quarter, department)
            for item in classes["Courses"]:
                num = item['CourseNumber']
                if num not in collegeabbr[department]:
                    extra_data = get_class_data(item['Href'])
                    item['CourseDescription'] = extra_data['CourseDescription']
                    item['CourseComment'] = extra_data['CourseComment']
                    item['FirstYear'] = extra_data['FirstEffectiveTerm']['Year']
                    item['FirstQuarter'] = extra_data['FirstEffectiveTerm']['Quarter']
                    item['LastYear'] = extra_data['LastEffectiveTerm']['Year']
                    item['LastQuarter'] = extra_data['LastEffectiveTerm']['Quarter']
                    item['MinTermCredit'] = extra_data['MinimumTermCredit']
                    item['MaxTermCredit'] = extra_data['MaximumTermCredit']
                    item['GE_EC'] = extra_data['GeneralEducationRequirements']['EnglishComposition']
                    item['GE_IS'] = extra_data['GeneralEducationRequirements']['IndividualsAndSocieties']
                    item['GE_NW'] = extra_data['GeneralEducationRequirements']['NaturalWorld']
                    item['GE_VLPA'] = extra_data['GeneralEducationRequirements']['VisualLiteraryAndPerformingArts']
                    item['GE_QSR'] = extra_data['GeneralEducationRequirements']['QuantitativeAndSymbolicReasoning']
                    item['GE_W'] = extra_data['GeneralEducationRequirements']['Writing']
                    collegeabbr[department][num] = item
    #break;


#Takes the dictionary of classes and export it to a .csv file
fieldnames = ["CurriculumAbbreviation", "CourseNumber", "CourseTitle", "CourseTitleLong", "CourseDescription", "CourseComment", "Href", 
    "Year", "Quarter", 'FirstYear', 'FirstQuarter', 'LastYear', 'LastQuarter', 'MinTermCredit', 'MaxTermCredit', 
    "GE_EC", "GE_IS", "GE_NW", "GE_VLPA", "GE_QSR", "GE_W" ]
data_file = open("coursedata.csv", "wt")
csvwriter = csv.DictWriter(data_file, delimiter=",", fieldnames=fieldnames)

print "writing csv file..."
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for dept in collegeabbr:
    print dept
    for key,item in collegeabbr[dept].items():
        #print pretty(item)
        csvwriter.writerow(item)
data_file.close()
