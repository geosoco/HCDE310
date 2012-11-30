import sys
import httplib
import urllib
import urllib2
import simplejson
import csv
import student
import os


fieldnames = ["CurriculumAbbreviation", "CourseNumber", "CourseTitle", "CourseTitleLong", "CourseDescription", "CourseComment", "Href", 
    "Year", "Quarter", 'FirstYear', 'FirstQuarter', 'LastYear', 'LastQuarter', 'MinTermCredit', 'MaxTermCredit', 
    "GE_EC", "GE_IS", "GE_NW", "GE_VLPA", "GE_QSR", "GE_W" ]


def writeCSV(filename, rows):
    with open(filename, "wt") as data_file:
        csvwriter = csv.DictWriter(data_file, delimiter=",", fieldnames=fieldnames)
        csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
        for key,item in rows:
            try:
                csvwriter.writerow(item)
            except UnicodeEncodeError, e:
                print student.pretty(item)
                continue
            except Exception, e:
                continue
        data_file.close()


#
#
# start
#
#

subdir = "./coursedata"
if sys.argv is not None and len(sys.argv) > 1:
    subdir = sys.argv[1]
if not os.path.exists(subdir):
    os.makedirs(subdir)



years = range(2010,2014)
quarters = ["autumn", "winter", "spring", "summer"]
#quarters = ["autumn"]

curricula = set()


# grab the curricula
print "Grabbing Curricula..."
for y in years:
    print "  ", y
    for q in quarters:
        c_data = student.get_curriculum_data(y,q)
        curricula = curricula | set([ c['CurriculumAbbreviation'] for c in c_data['Curricula']])


# set up initial collegeabbr data
collegeabbr = {}
for department in curricula:
    collegeabbr[department] = {}

#generates a json dictionary of all of the classes specified in the above "years" and "quarters" arrays
print "Grabbing courses..."

for department in curricula:
    print "  ", department
    filename = os.path.join(subdir, department + ".csv")
    if os.path.exists(filename):
        print "    skipped"
        continue
    for year in years:
        print '    ', year
        for quarter in quarters:
            classes = student.get_classes(year, quarter, department)
            if classes is None:
                continue;
            #print student.pretty(classes)

            for item in classes["Courses"]:
                #print student.pretty(item)
                num = item['CourseNumber']
                if num not in collegeabbr[department]:
                    #print item['Href']
                    try:
                        extra_data = student.get_class_data(item['Href'])
                        if extra_data is not None:
                            item['CourseDescription'] = extra_data['CourseDescription']
                            item['CourseComment'] = extra_data['CourseComment']
                            item['FirstYear'] = extra_data['FirstEffectiveTerm']['Year']
                            item['FirstQuarter'] = extra_data['FirstEffectiveTerm']['Quarter']
                            item['LastYear'] = extra_data['LastEffectiveTerm']['Year']
                            item['LastQuarter'] = extra_data['LastEffectiveTerm']['Quarter']
                            item['MinTermCredit'] = extra_data['MinimumTermCredit']
                            item['MaxTermCredit'] = extra_data['MaximumTermCredit']
                            if 'GeneralEducationRequirements' in extra_data:
                                item['GE_EC'] = extra_data['GeneralEducationRequirements']['EnglishComposition']
                                item['GE_IS'] = extra_data['GeneralEducationRequirements']['IndividualsAndSocieties']
                                item['GE_NW'] = extra_data['GeneralEducationRequirements']['NaturalWorld']
                                item['GE_VLPA'] = extra_data['GeneralEducationRequirements']['VisualLiteraryAndPerformingArts']
                                item['GE_QSR'] = extra_data['GeneralEducationRequirements']['QuantitativeAndSymbolicReasoning']
                                item['GE_W'] = extra_data['GeneralEducationRequirements']['Writing']
                            else:
                                item['GE_EC'] = false
                                item['GE_IS'] = false
                                item['GE_NW'] = false
                                item['GE_VLPA'] = false
                                item['GE_QSR'] = false
                                item['GE_W'] = false

                        collegeabbr[department][num] = item
                    except Exception, e:
                        print num
                        print student.pretty(collegeabbr[department])
                        continue



    #print filename
    writeCSV(filename, collegeabbr[department].items() )



#Takes the dictionary of classes and export it to a .csv file

#data_file = open("coursedata.csv", "wt")
#csvwriter = csv.DictWriter(data_file, delimiter=",", fieldnames=fieldnames)

#print "writing csv file..."
#csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
#for dept in collegeabbr:
    #print dept
#    for key,item in collegeabbr[dept].items():
        #print pretty(item)
#        csvwriter.writerow(item)
#data_file.close()
