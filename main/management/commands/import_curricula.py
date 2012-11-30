from django.core.management.base import BaseCommand, CommandError
import django.db
import csv
from main.models import Departments, Courses, Instances, Ratings, Instructors
import pprint


def AddDept(name, abbrev, url, firstyear, lastyear ):
	#print "Adding %s (%s)"%(abbrev,name)
	try:
		d = Departments.objects.get(abbreviation = abbrev)
		#print d.id
		return d
	except Departments.DoesNotExist, e:
		try:
			d = Departments(name=name,abbreviation=abbrev, url=url, firstyear=firstyear, lastyear=lastyear)
			d.save()
			return d
		except:
			return None



class Command(BaseCommand):
	args = '<filename>'
	help = 'Imports curricula. \nUsage: import_curricula %s'

	depts = {}
	courses = {}
	instructors = {}
	coursetypes = {}
	quarters = set()


	def handle(self, *args, **options):
		#print "Version: %s"%django.get_version()
		if args is None or len(args) == 0:
			raise CommandError('must specify csv file')
		#print "opening %s"%args[0]
		self.stdout.write('opening: %s\n'%args[0])
		with open(args[0],'rU') as csvfile:
			csvreader = csv.DictReader(csvfile)

			#
			for row in csvreader:
				#print row
				AddDept(row['CurriculumFullName'] ,row['CurriculumAbbreviation'], row['Href'], int(row['Year']), int(row['LastYear']) )


