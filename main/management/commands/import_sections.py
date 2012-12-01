from django.core.management.base import BaseCommand, CommandError
import django.db
import csv
import sys
import os
from main.models import Curriculum, Course, Section, Rating, Instructor, Section, Meeting, Building, SectionRelation
import pprint
import simplejson


def pretty(obj):
	return simplejson.dumps(obj, sort_keys=True, indent=2)


def GetCurriculum(abbr):
	try:
		d = Curriculum.objects.get(abbreviation = abbr)
		return d
	except Curriculum.DoesNotExist, e:
		return None

def AddCourse(dept, number, name, comment = "", descr = "", genedreqs = 0, firstyear = None, firstquarter = None, lastyear = None, lastquarter = None, mincredits = None, maxcredits = None):
	try:
		c = Course.objects.get(iddepartment = dept, number = long(number))
		return c
	except Course.DoesNotExist, e:
		try:
			c = Course(name=name, number=long(number), iddepartment=dept, comment = comment, description = descr)
			c.genedreqs = genedreqs
			c.firstyear = firstyear
			c.firstquarter = firstquarter
			c.lastyear = lastyear
			c.lastquarter = lastquarter
			c.mincredits = mincredits
			c.maxcredits = maxcredits
			c.save()
			return c
		except Exception, e:
			print "exception!"
			print e
			return None
	except Exception, e:
		print "AddCourse - exception: ", e



quarters = {
	'autumn' : 'AU',
	'winter' : 'WI',
	'spring' : 'SP',
	'summer' : 'SU'
}

def formatTime(row, index):
	time1 = row['StartTime' + str(index)]
	time2 = row['EndTime' + str(index)]
	if time1 is not None and time2 is not None and len(time1) > 0 and len(time2) > 0:
		return "%s - %s"%(time1,time2)
	return None


class Command(BaseCommand):
	args = '<directory>'
	help = 'Imports sections. \nUsage: import_section %s'

	depts = {}
	courses = {}
	instructors = {}
	coursetypes = {}
	quarters = set()
	times = set()


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



