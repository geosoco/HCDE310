from django.core.management.base import BaseCommand, CommandError
import django.db
import csv
from main.models import Curriculum, Course, Section, Rating, Instructor
import pprint
from decimal import *
from utils import *


RATING_MAPPINGS = {
	"NumSurveyed" : "NumSurveyed",
	"NumEnrolled" : "NumEnrolled",
	"Course" : "CourseWholeMedian",
	"Content" : "ContentMedian",
	"Contrib" : "ContribMedian",
	"Effectiveness" : "EffectivenessMedian",
	"Grading" : "GradingMedian",
	"Interest" : "InterestMedian",
	"Learned" : "LearnedMedian"
}



def AddCurricula(depts):
	for dept in depts.keys():
		d = GetCurriculum(dept)
		#print id
		if d is not None:
			depts[dept]['id'] = d.id
		else:
			depts[dept]['id'] = -1
		depts[dept]['obj'] = d
		


def AddInstructors(instructors):
	for instructor in instructors.keys():
		i = AddInstructor(instructor)
		if i is not None:
			instructors[instructor]['id'] = i.id
		else:
			instructors[instructor]['id'] = -1
		instructors[instructor]['obj'] = i



def AddCourses(deptid, courses):
	for course in courses.keys():
		#print "[%s]"%course
		#print courses[course]
		c = GetCourse(deptid, course)
		if c is not None:
			courses[course]['id'] = c.id
		else:
			courses[course]['id'] = -1
		courses[course]['obj'] = c


def AddRating(rating):
#	try:
		r = Rating(numsurveyed = rating["NumSurveyed"], numenrolled = rating["NumEnrolled"])
		r.coursewhole = Decimal(rating["Course"]) if len(rating["Course"]) > 0 else None
		r.coursecontent = Decimal(rating["Content"]) if len(rating["Content"]) > 0 else None
		r.instructoreffectiveness = Decimal(rating["Effectiveness"]) if len(rating["Effectiveness"]) > 0 else None
		r.instructorcontribution = Decimal(rating["Contrib"]) if len(rating["Contrib"]) > 0 else None
		r.instructorinterest = Decimal(rating["Interest"]) if len(rating["Interest"]) > 0 else None
		r.amountlearned = Decimal(rating["Learned"]) if len(rating["Learned"]) > 0 else None
		r.grading = Decimal(rating["Grading"]) if len(rating["Grading"]) > 0 else None

		#print r.coursewhole

		#print rating
		#print ",".join(rating.values())
		r.save()
		return r
#	except Exception, e:
#		print "exception in AddRating: ", e
#		return None

def AddSection(course_id, instructor_id, quarter, section, instructor_title, ratings):
	try:
		q = quarter[:2].upper()
		y = quarter[2:]
		#print course_id
		#print "%s %s"%(q, y)
		r = AddRating(ratings)
		i = Section(quarter = q, year = y, idinstructor = instructor_id, idcourse = course_id, idrating = r, instructortitle = instructor_title, section = section )
		i.save()
		return i.id
	except Exception, e:
		print "exception: ", e
		return None



class Command(BaseCommand):
	args = '<filename>'
	help = 'Closes the specified poll for voting.\nUsage: import_evals %s'

	headerDict = {}
	depts = {}
	courses = {}
	instructors = {}
	coursetypes = {}
	quarters = set()


	def handle(self, *args, **options):
		print "Version: %s"%django.get_version()
		if args is None or len(args) == 0:
			raise CommandError('must specify a csv file to import from')
		#print "opening %s"%args[0]
		self.stdout.write('opening: %s\n'%args[0])
		with open(args[0],'rU') as csvfile:
			csvreader = csv.DictReader(csvfile)

			#
			for row in csvreader:
				self.coursetypes[row['CourseType'].strip()] = row['CourseTypeName']

				instructor = row['Instructor'].strip()
				instructor_title = row['InstructorTitle'].strip()
				if instructor not in self.instructors:
					self.instructors[instructor] = { "courses": 0, "titles": set(), "id": -1}
				self.instructors[instructor]['courses'] = self.instructors[instructor]['courses'] + 1
				self.instructors[instructor]['titles'].add(instructor_title)

				dept = row['DeptAbbrev'].strip()
				dept_name = row['Dept'].strip()
				coursenum = row['CourseNum'].strip()
				if len(coursenum) == 0: 
					continue


				if dept not in self.depts:
					self.depts[dept] = { 'id': len(self.depts), 'name': dept_name, 'courses': {}}
				if coursenum not in self.depts[dept]:
					self.depts[dept]['courses'][coursenum] = { "id": len(self.depts[dept]['courses']) }

				quarter = row['Quarter'].strip()
				self.quarters.add(quarter)

				section = row['Section'].strip()
				instructor_title = row['InstructorTitle'].strip()

				#self.depts[dept]['courses'][coursenum]['instances'].append({ "id": -1, "rating": ratings, "quarter": quarter, "section": section, "instructortitle": instructor_title})

			# step through
			print "Adding Curricula (%d)"%len(self.depts)
			AddCurricula(self.depts)

			print "Adding Instructors (%d)"%len(self.instructors)
			AddInstructors(self.instructors)

			print "Adding Course"
			for dept in self.depts.keys():
				print "%s (%d)"%(dept,self.depts[dept]['id'])
				dept_obj = self.depts[dept]['obj']
				#print dept_obj
				AddCourses(dept_obj, self.depts[dept]['courses'])

			# now do the instances
			
			csvfile.seek(0)
			csvreader.next()
			for row in csvreader:
				instructor = row['Instructor'].strip()
				instructor_title = row['InstructorTitle'].strip()
				dept = row['DeptAbbrev'].strip()
				coursenum = row['CourseNum'].strip()
				quarter = row['Quarter'].strip()
				section = row['Section'].strip()

				if len(coursenum) == 0:
					continue

				ratings = {}
				for k,v in RATING_MAPPINGS.iteritems():
					ratings[k] = row[v]

				print "%s %s"%(dept,coursenum)

				i = self.instructors[instructor]['obj']
				d = self.depts[dept]['obj']
				c = self.depts[dept]['courses'][coursenum]['obj']

				if c is not None:
					inst = AddSection(c,i,quarter,section,instructor_title,ratings)
				else:
					self.stderr.write("no course found for %s %s\n"%(dept,coursenum))

				


