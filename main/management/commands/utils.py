import simplejson
import django.db
from main.models import *


QUARTERS = {
	'autumn' : 'AU',
	'winter' : 'WI',
	'spring' : 'SP',
	'summer' : 'SU'
}


#
# parseTime
#
# input: 24-hour time value 
#
def parseTime(s):
	if s is not None and len(s) > 0:
		parts = s.split(':')
		return int((parts[0] + parts[1]))


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
	except model.DoesNotExist, e:
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

#
# Courses 
#
def GetCourse(curriculum, num):
	return dbSafeGet(Course, **{'idcurriculum': curriculum, 'number': num})

#
#
# Instructor
#
#
def AddInstructor(name):
	return dbSafeGetOrAdd(Instructor, **{'name': name})

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


#
#
# Section
#
#
def GetSection(course, year, quarter, section):
	return dbSafeGet(Section, **{'idcourse': course, 'year':year, 'quarter':quarter, 'section':section})



#
#
#
#
def cachedSafeGetOrAdd(dict, key, method, **kwargs):
	ret = None
	if key is not None and len(key) > 0:
		if key in dict:
			ret = dict[key]
		else:
			#print "%s not in dict, trying to grab"%key
			ret = method(**kwargs)
			if ret is not None:
				dict[key] = ret
	return ret





