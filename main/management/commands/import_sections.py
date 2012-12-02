from django.core.management.base import BaseCommand, CommandError
import django.db
import csv
import sys
import os
from main.models import Curriculum, Course, Section, Rating, Instructor, Section, Meeting, Building, Room, SectionRelation, MeetingType
import pprint
import simplejson



quarters = {
	'autumn' : 'AU',
	'winter' : 'WI',
	'spring' : 'SP',
	'summer' : 'SU'
}


#
#
#
def pretty(obj):
	return simplejson.dumps(obj, sort_keys=True, indent=2)


#
def dbSafeGet(model, **kwargs):
	try: 
		o = model.objects.get(**kwargs)
		return o
	except o.DoesNotExist, e:
		return None

#
def dbSafeGetOrAdd(model, **kwargs):
	try: 
		o = model.objects.get(**kwargs)
		return o
	except model.DoesNotExist, e:
		try:
			o = model(**kwargs)
			o.save()
			return o
		except Exception, e:
			print "Exception in dbSafeGetOrAdd", e
			return None


#
# Curriculum
#
def GetCurriculum(abbr):
	return dbSafeGet(Curriculum, **{ 'abbreviation': abbr })
#	try:
#		d = Curriculum.objects.get(abbreviation = abbr)
#		return d
#	except Curriculum.DoesNotExist, e:
#		return None

#
# Courses 
#
def GetCourse(curriculum, num):
	return dbSafeGet(Course, **{'idcurriculum': curriculum, 'number': num})

#	try:
#		c = Course.objects.get(idcurriculum=curriculum, number=num)
#		return c
#	except Course.DoesNotExist, e:
#		return None

#
#
# Instructor
#
#
def AddInstructor(name):
	return dbSafeGetOrAdd(Instructor, **{'name': name})
#	try:
#		i = Instructor.objects.get(name = name)
#		return i
#	except Instructor.DoesNotExist, e:
#		try:
#			i = Instructor(name=name)
#			i.save()
#			return i
#		except:
#			return None


#
#
# Room
#
#

def AddRoom(name, idbuilding):
	return dbSafeGetOrAdd(Room, **{'name': name, 'idbuilding': idbuilding})

#
#
# Building
#
#

def AddBuilding(name):
	return dbSafeGetOrAdd(Building, **{'name': name})

#
#
# MeetingType
#
#
def AddMeetingType(name):
	return dbSafeGetOrAdd(MeetingType, **{'name': name})



#	try:
#		b = Building.objects.get(name = name)
#		return b
#	except Building.DoesNotExist, e:
#		try:
#			b = Building(name=name)
#			b.save()
#			return b
#		except Exception, e:
#			return None 

#
#
# Section
#
#
def GetSection(course, year, quarter, section):
	return dbSafeGet(Section, **{'idcourse': course, 'year':year, 'quarter':quarter, 'section':section})
#	try:
#		s = Section.objects.get(idcourse=course, year=year, quarter=quarter, section=section)
#		return s
#	except Course.DoesNotExist, e:
#		return None

#
def AddSection(course, year, quarter, section, instructor = None, enrolled = None, maxenrolled = None, sln = None, classurl = None ):
	try:
		s = Section(
			quarter=quarter, 
			section=section,
			idinstructor = instructor,
			idcourse = course,
			instructortitle = None,
			year = year,
			numenrolled = enrolled,
			maxenrollment = maxenrolled,
			classwebsite = classurl,
			sln = sln
			)
		s.save()
	except Exception,e:
		print "Failed to add section"
		return None



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
def buildMeeting(row, index):
	idx = str(index)
	ret = {}
	days = makeDaysFromStr(row['DaysOfWeek' + idx])
	starttime = row['StartTime' + idx]
	tba = row['DaysOfWeekToBeArranged' + idx].lower() == 'true'
	if len(starttime) == 0 and tba == False and days == 0:
		return None

	ret['building'] = row['Building' + idx]
	ret['days'] = days
	ret['daystba'] = tba
	ret['meetingtype'] = row['MeetingType' + idx]
	ret['starttime'] = starttime
	ret['endtime'] = row['EndTime' + idx]
	return ret


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


def cachedSafeGetOrAdd(dict, key, method, **kwargs):
	ret = None
	if key is not None:
		if key in dict:
			ret = dict[key]
		else:
			print "%s not in dict, trying to grab"%key
			ret = method(**kwargs)
			if ret is not None:
				dict[key] = ret
	return ret


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

						print "instructor added..."
						print instructor
						#if inst_name is not None:
						#	if inst_name is in self.instructors:
						#		instructor = self.instructors
						#	else:
						#		instructor = AddInstructor(inst_name)
						#		if instructor is not None:
						#			self.instructors[inst_name] = instructor

						# add section
						kwargs = {}
						kwargs['quarter'] = quarters[row['Quarter'].lower()]
						kwargs['year'] = row['Year']
						kwargs['section'] = row['SectionID'] if 'SectionID' in row else row['PrimarySection']
						kwargs['idinstructor'] = instructor
						kwargs['idcourse'] = c
						kwargs['numenrolled'] = row['CurrentEnrollment']
						kwargs['maxenrollment'] = row['LimitEstimateEnrollment']
						kwargs['sln'] = row['SLN']
						kwargs['classwebsite'] = row['ClassWebsiteUrl']
						section = dbSafeGetOrAdd(Section, **kwargs)

						print "section seems to have been added..."
						print section


						# meetings
						for m in mtgs:

							bldg_name = m['Building']
							bldg = cachedSafeGetOrAdd(self.buildings, bldg_name, AddBuilding, **{'name': bldg_name})

							if bldg is not None:
								room_name = m['Room']
								room = cachedSafeGetOrAdd(self.rooms, room_name, AddRoom, **{'name': room_name, 'idbuilding': bldg })

							mtg_type_name = m['Type']
							mtg_type = cachedSafeGetOrAdd(self.meetingtypes, mtg_type_name, AddMeetingType, **{'name': mtg_type_name})


							#add meeting



						#d0 = row['DaysOfWeek0']
						#d1 = row['DaysOfWeek1']
						#d2 = row['DaysOfWeek2']

						#if d0 is not None:
						#	self.daysofweek.add(d0)
						#if d1 is not None:
						#	self.daysofweek.add(d1)
						#if d2 is not None:
						#	self.daysofweek.add(d2)
						#time0 = formatTime(row,0)
						#time1 = formatTime(row,1)
						#time2 = formatTime(row,2)

						#if time0 is not None:
						#	self.times.add(time0)
						#if time1 is not None:
						#	self.times.add(time1)
						#if time2 is not None:
						#	self.times.add(time2)

		#print pretty(sorted(list(self.times)))
		#days = sorted(list(self.daysofweek))
		#for d in days:
		#	s = "%s : %d"%(d, makeDaysFromStr(d))
		#	print s
		



