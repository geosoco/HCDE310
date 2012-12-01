from django.core.management.base import BaseCommand, CommandError
import django.db
import csv
import sys
import os
from main.models import Curriculum, Course, Section, Rating, Instructor
import pprint


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



class Command(BaseCommand):
	args = '<directory>'
	help = 'Imports courses. \nUsage: import_courses %s'

	depts = {}
	courses = {}
	instructors = {}
	coursetypes = {}
	quarters = set()


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
						#print row
						genedreqs = c.convertGenEdReqsToInt(row['GE_NW'], row['GE_VLPA'], row['GE_IS'], row['GE_W'], row['GE_EC'], row['GE_QSR'])

						mincr = float(row['MinTermCredit'])
						maxcr = float(row['MaxTermCredit']) 
						maxcr = mincr if maxcr < maxcr else maxcr

						AddCourse(curriculum , 
							int(row['CourseNumber']), 
							row['CourseTitleLong'], 
							row['CourseComment'], 
							row['CourseDescription'],
							genedreqs, 
							int(row['FirstYear']),
							quarters.get(row['FirstQuarter']),
							int(row['LastYear']),
							quarters.get(row['LastQuarter']),
							mincr,
							maxcr
							 )





