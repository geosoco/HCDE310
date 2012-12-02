from django.core.management.base import BaseCommand, CommandError
import django.db
import csv
import sys
import os
from main.models import Curriculum, Course, Section, Rating, Instructor, Section, Meeting, Building, Room, SectionRelation, MeetingType
import pprint
import simplejson

from utils import *



#
#
#
#
#


#
#
#
#
def formatTime(row, index):
	time1 = row['StartTime' + str(index)]
	time2 = row['EndTime' + str(index)]
	if time1 is not None and time2 is not None and len(time1) > 0 and len(time2) > 0:
		return "%s - %s"%(time1,time2)
	return None

#
#
#
#
def makeDaysFromStr(str):
	if str == '[to be arranged]':
		return 255
	ret = 0
	ret |= 1 if str[1] == 'M' else 0
	ret |= 2 if str[2] == 'T' else 0
	ret |= 4 if len(str) > 3 and str[3] == 'W' else 0
	ret |= 8 if len(str) > 4 and str[4] == 'T' else 0
	ret |= 16 if len(str) > 5 and str[5] == 'F' else 0
	ret |= 32 if len(str) > 6 and str[6] == 'S' else 0
	return ret
#def getBuilding(abbr):




#
#
#
#

def inflateMeeting(row):
	meetings = []
	mtg_buildings = row['Building'].split('|')
	mtg_daysofweek = row['DaysOfWeek'].split('|')
	mtg_types = row['MeetingType'].split('|')
	mtg_starts = row['StartTime'].split('|')
	mtg_ends = row['EndTime'].split('|')
	mtg_rooms = row['Room'].split('|')
	mtg_instructors = row['Instructors'].split('|')

	for i in range(len(mtg_buildings)):
		mtg = {}
		mtg['Building'] = mtg_buildings[i]
		mtg['Days'] = mtg_daysofweek[i]
		mtg['Type'] = mtg_types[i]
		mtg['Start'] = mtg_starts[i]
		mtg['End'] = mtg_ends[i]
		mtg['Room'] = mtg_rooms[i]
		mtg['Instructors'] = mtg_instructors[i].split(';') if len(mtg_instructors) > i else None
		meetings.append(mtg)

	return meetings





class Command(BaseCommand):
	args = '<directory>'
	help = 'Imports sections. \nUsage: import_section %s'

	depts = {}
	courses = {}
	instructors = {}
	coursetypes = {}
	buildings = {}
	rooms = {}
	quarters = set()
	times = set()
	daysofweek = set()
	meetingtypes = {}


	def handle(self, *args, **options):
		#print "Version: %s"%django.get_version()
		if args is None or len(args) == 0:
			raise CommandError('must specify directory')
		#print "opening %s"%args[0]
		subdir = args[0]

		c = Course()

		for root, dirs, files in os.walk(subdir):
			for name in files:
				filename = os.path.join(root,name)

				self.stdout.write('opening: %s\n'%filename)

				abbr = os.path.splitext(os.path.basename(filename))[0]
				self.stdout.write(abbr + '\n')

				curriculum = GetCurriculum(abbr)
				if curriculum is None:
					self.stderr.write('Couldn\'t find the curriculum' )
					continue

				with open(filename,'rU') as csvfile:
					csvreader = csv.DictReader(csvfile)
					#
					for row in csvreader:

						# lookup the course
						coursenum = int(row['CourseNumber'])
						c = GetCourse(curriculum, coursenum)
						if c is None:
							print "!!!! Couldn't find %s   %d"%(curriculum.abbreviation, coursenum)
							continue

						# meetings
						mtgs = inflateMeeting(row)

						# instructor
						inst_name = None
						for i in mtgs:
							if i['Instructors'] is not None and len(i['Instructors']) > 0:
								if len(i['Instructors'][0]) > 0:
									inst_name = i['Instructors'][0]

						instructor = cachedSafeGetOrAdd(self.instructors, inst_name, AddInstructor, **{'name': inst_name})

						# add section
						kwargs = {}
						kwargs['quarter'] = QUARTERS[row['Quarter'].lower()]

						kwargs['year'] = row['Year']
						kwargs['section'] = row['SectionID'] if 'SectionID' in row else row['PrimarySection']
						kwargs['idinstructor'] = instructor
						kwargs['idcourse'] = c
						kwargs['numenrolled'] = row['CurrentEnrollment']
						kwargs['maxenrollment'] = row['LimitEstimateEnrollment']
						kwargs['sln'] = row['SLN']
						kwargs['classwebsite'] = row['ClassWebsiteUrl']
						section = dbSafeGetOrAdd(Section, **kwargs)

						if section is None:
							print "Section not added", section
							continue

						#print "section seems to have been added..."
						#print section


						# meetings
						for m in mtgs:

							bldg_name = m['Building']
							bldg = cachedSafeGetOrAdd(self.buildings, bldg_name, AddBuilding, **{'name': bldg_name})

							room = None
							if bldg is not None:
								room_name = m['Room']
								room = cachedSafeGetOrAdd(self.rooms, room_name, AddRoom, **{'name': room_name, 'idbuilding': bldg })

							mtg_type_name = m['Type']
							mtg_type = cachedSafeGetOrAdd(self.meetingtypes, mtg_type_name, AddMeetingType, **{'name': mtg_type_name})

							mtg_start = parseTime(m['Start'])
							mtg_end = parseTime(m['End'])
							mtg_days = makeDaysFromStr(m['Days'])

							meeting = Meeting(day = mtg_days, starttime = mtg_start, endtime = mtg_end, idinstance = section, idroom = room, idmeetingtype = mtg_type)
							meeting.save()



