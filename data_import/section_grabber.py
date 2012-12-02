import httplib
import urllib
import urllib2
import simplejson
import csv
import sys
import student
import os



# Building
# RoomNumber
# DaysOfWeek - Text
# StartTime
# EndTime
# MeetingType
# DaysOfWeekToBeArranged
#


def set_meeting(s, num, bldg = '', room = '', days = '[     ]', start='', end = '', meetingtype='', tba = False, instructors = None):
    s['Building' + num] = bldg
    s['RoomNumber' + num] = room
    s['DaysOfWeek' + num] = days
    s['StartTime' + num] = start
    s['EndTime' + num] = end
    s['MeetingType' + num] = meetingtype
    s['DaysOfWeekToBeArranged' + num] = tba
    for i in range(5):
        istr = str(i+1)
        name = None
        regid = None
        if instructors is not None and i < len(instructors):
            name = instructors[i]['name']
            regid = instructors[i]['regid']
        s['Instructor' + num + "-" + istr] = name
        s['RegID' + num + "-" + istr] = regid



def prune_meeting(s, m, num):
    meeting_instructors = m.get('Instructors')
    instructors = []
    if meeting_instructors is not None:
        
        for i in meeting_instructors:
            person = i.get('Person')
            if person is not None:
                data = {}
                data['name'] = person.get('Name')
                data['regid'] = person.get('RegID')
                instructors.append(data)

        if len(meeting_instructors) > 5:
            print "Found multiple meeting_instructors for course:"
            print student.pretty(s)
            print student.pretty(m)

    set_meeting(s,num,
        bldg = m['Building'],
        room = m['RoomNumber'], 
        days = '[     ]' if 'DaysOfWeek' not in m else '[' + m['DaysOfWeek']['Text'] + ']',
        start = m['StartTime'],
        end = m['EndTime'],
        meetingtype = m['MeetingType'],
        tba = m['DaysOfWeekToBeArranged'],
        instructors = instructors
        );

def formatInstructors(instructors):
    ret = []
    #print instructors
    if instructors is None:
        return None
    for i in instructors:
        person = i.get('Person')
        if person is not None:
            ret.append(person.get("Name"))
    return ";".join(ret)


def prune_section(sect):
    s = {}
    s['CurriculumAbbreviation'] = sect['Course']['CurriculumAbbreviation']
    s['CourseNumber'] = sect['Course']['CourseNumber']
    s['Year'] = sect['Course']['Year']
    s['Quarter'] = sect['Course']['Quarter']
    s['SectionID'] = sect['SectionID']
    s['PrimarySection'] = sect['PrimarySection']['SectionID']
    s['SLN'] = sect['SLN']
    s['CurrentEnrollment'] = sect['CurrentEnrollment']
    s['LimitEstimateEnrollment'] = sect['LimitEstimateEnrollment']
    s['ClassWebsiteUrl'] = sect['ClassWebsiteUrl']

    i = sect['Meetings']
    s['Building'] = "|".join([m['Building'] for m in i])
    s['Room'] = "|".join([m['RoomNumber'] for m in i])
    s['DaysOfWeek'] = "|".join(['[     ]' if 'DaysOfWeek' not in m else '[' + m['DaysOfWeek']['Text'] + ']' for m in i])
    s['StartTime'] = "|".join([m['StartTime'] for m in i])
    s['EndTime'] = "|".join([m['EndTime'] for m in i])
    s['MeetingType'] = "|".join([m['MeetingType'] for m in i])
    
    #print student.pretty(m['Instructors'])

    s['Instructors'] = formatInstructors(m['Instructors'])
    #print s['Instructors']

    #for i in range(0, 3):
    #    if i < len(sect['Meetings']):
    #        prune_meeting(s,sect['Meetings'][i],str(i))
    #    else:
    #        set_meeting(s,str(i))

    return s



def writeCSV(filename, rows):
    with open(filename, "wt") as data_file:
        #print student.pretty(rows[0].keys())
        fieldnames = sorted(rows[0].keys())
        csvwriter = csv.DictWriter(data_file, delimiter=",", fieldnames=fieldnames)
        csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
        for item in rows:
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

year = '2013'
quarter = 'winter'
subdir = "./sectiondata"

filename = None
if sys.argv is not None and len(sys.argv) > 2:
    filename = sys.argv[1]
    subdir = sys.argv[2]
    if len(sys.argv) > 3:
        year = sys.argv[3]
    if len(sys.argv) > 4:
        quarter = sys.argv[4]
else:
    print "Usage: <curriculumfile.csv> <subdir> year quarter"
    quit()


if not os.path.exists(subdir):
    os.makedirs(subdir)

#sections = student.get_sections(year, quarter, 'HCDE')
#print pretty(sections)
#s = student.get_class_data(sections["Sections"][0]['Href'])

#s2 = prune_section(s)
#print student.pretty(s)
#print "---"
#print student.pretty(s2)

#quit()

print "reading %s ..."%(filename)
with open(filename, "rt") as data_file:
    csvreader = csv.DictReader(data_file, delimiter=",",  quotechar='"')
    params = {}
    for row in csvreader:
        #params['course_number'] = row['CourseNumber']
        #print row['Href']
        #sect = get_section(row['Href'])
        abbr = row['CurriculumAbbreviation']
        #abbr = 'HCDE'
        print abbr

        #sections = student.get_sections('2012', 'summer', abbr)
        #for sect in sections['Sections']:
        #    s = student.get_class_data(sect['Href'])
        #    print student.pretty(s)
        #quit()        

        filename = os.path.join(subdir, abbr + ".csv")
        if not os.path.exists(filename):
            sections = student.get_sections(year, quarter, abbr)
            #print student.pretty(sections)

            pruned_sections = []
            for sect in sections['Sections']:
                s = student.get_class_data(sect['Href'])
                #print student.pretty(s)
                if s is not None:
                    s = prune_section(s)
                    pruned_sections.append(s)
            
            if len(pruned_sections) > 0:
                writeCSV(filename, pruned_sections )
        




