from django.core.management.base import BaseCommand, CommandError
import django.db
import csv
from main.models import Departments, Courses, Instances, Ratings, Instructors



def AddDept(name, abbrev):
	#print "Adding %s (%s)"%(abbrev,name)
	try:
		d = Departments.objects.get(abbreviation = abbrev)
		#print d.id
		return d
	except Departments.DoesNotExist, e:
		try:
			d = Departments(name=name,abbreviation=abbrev)
			d.save()
			return d
		except:
			return None

def AddDepartments(depts):
	for dept in depts.keys():
		d = AddDept(depts[dept]['name'], dept)
		#print id
		if d is not None:
			depts[dept]['id'] = d.id
		else:
			depts[dept]['id'] = -1
		depts[dept]['obj'] = d
		
def AddInstructor(name):
	try:
		i = Instructors.objects.get(name = name)
		return i
	except Instructors.DoesNotExist, e:
		try:
			i = Instructors(name=name)
			i.save()
			return i
		except:
			return None

def AddInstructors(instructors):
	for instructor in instructors.keys():
		i = AddInstructor(instructor)
		if i is not None:
			instructors[instructor]['id'] = i.id
		else:
			instructors[instructor]['id'] = -1
		instructors[instructor]['obj'] = i


def AddCourse(dept, number, name, comment = "", descr = ""):
	try:
		c = Courses.objects.get(iddepartment = dept, number = int(number))
		return c
	except Courses.DoesNotExist, e:
		try:
			c = Courses(name=name, number=long(number), iddepartment=dept, comment = comment, description = descr)
			c.save()
			return c
		except Exception, e:
			print "exception!"
			print e
			return None

def AddCourses(deptid, courses):
	for course in courses.keys():
		#print "[%s]"%course
		#print courses[course]
		c = AddCourse(deptid, course, "", "", "")
		if c is not None:
			courses[course]['id'] = c.id
		else:
			courses[course]['id'] = -1
		courses[course]['obj'] = c


def AddRating(rating):
	try:
		r = Ratings(numsurveyed = rating["NumSurveyed"], numenrolled = rating["NumEnrolled"])
		r.coursewhole = rating["Course"]
		r.coursecontent = rating["Content"]
		r.instructoreffectiveness = rating["Effectiveness"]
		r.instructorcontribution = rating["Contrib"]
		r.instructorinterest = rating["Interest"]
		r.amountlearned = rating["Learned"]
		r.grading = rating["Grading"]
		r.save()
		return r
	except:
		return None

def AddInstance(course_id, instructor_id, quarter, section, instructor_title, ratings):
	try:
		i = Instances(quarter = quarter, idinstructor = instructor_id, idcourse = course_id, instructortitle = instructor_title, section = section )
		r = AddRating(ratings)
		i.idratings = r
		i.save()
		return i.id
	except:
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
			raise CommandError('csv  "%s" does not exist' % poll_id)
		#print "opening %s"%args[0]
		self.stdout.write('opening: %s\n'%args[0])
		with open(args[0],'rU') as csvfile:
			csvreader = csv.reader(csvfile)
			header = csvreader.next()

			# build header dictionary
			# key: name; value: index
			i = 0
			for col in header:
				colname = col.strip()
				self.headerDict[colname] = i
				i = i + 1

			#
			for row in csvreader:
				self.coursetypes[row[self.headerDict['CourseType']].strip()] = row[self.headerDict['CourseTypeName']]

				instructor = row[self.headerDict['Instructor']].strip()
				instructor_title = row[self.headerDict['InstructorTitle']].strip()
				if instructor not in self.instructors:
					self.instructors[instructor] = { "courses": 0, "titles": set(), "id": -1}
				self.instructors[instructor]['courses'] = self.instructors[instructor]['courses'] + 1
				self.instructors[instructor]['titles'].add(instructor_title)

				dept = row[self.headerDict['DeptAbbrev']].strip()
				dept_name = row[self.headerDict['Dept']].strip()
				coursenum = row[self.headerDict['CourseNum']].strip()
				if len(coursenum) == 0: 
					continue


				if dept not in self.depts:
					self.depts[dept] = { 'id': len(self.depts), 'name': dept_name, 'courses': {}}
				if coursenum not in self.depts[dept]:
					self.depts[dept]['courses'][coursenum] = { "id": len(self.depts[dept]['courses']) }

				quarter = row[self.headerDict['Quarter']].strip()
				self.quarters.add(quarter)

				section = row[self.headerDict['Section']].strip()
				instructor_title = row[self.headerDict['InstructorTitle']].strip()

				#self.depts[dept]['courses'][coursenum]['instances'].append({ "id": -1, "rating": ratings, "quarter": quarter, "section": section, "instructortitle": instructor_title})

			# step through
			print "Adding Departments (%d)"%len(self.depts)
			AddDepartments(self.depts)

			print "Adding Instructors (%d)"%len(self.instructors)
			AddInstructors(self.instructors)

			print "Adding Courses"
			for dept in self.depts.keys():
				print "%s (%d)"%(dept,self.depts[dept]['id'])
				dept_obj = self.depts[dept]['obj']
				#print dept_obj
				AddCourses(dept_obj, self.depts[dept]['courses'])

			# now do the instances
			csvfile.seek(0)
			csvreader = csv.reader(csvfile)
			header = csvreader.next()
			for row in csvreader:
				instructor = row[self.headerDict['Instructor']].strip()
				instructor_title = row[self.headerDict['InstructorTitle']].strip()
				dept = row[self.headerDict['DeptAbbrev']].strip()
				coursenum = row[self.headerDict['CourseNum']].strip()
				quarter = row[self.headerDict['Quarter']].strip()
				section = row[self.headerDict['Section']].strip()

				rating_mappings = {
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

				ratings = {}
				for rm in rating_mappings.keys():
					col = rating_mappings[rm]
					ratings[rm] = row[self.headerDict[col]]

				print "%s %d"%(dept,coursenum)
				i = self.instructors[instructor]['obj']
				d = self.depts[dept]['obj']
				c = self.depts[dept]['courses'][coursenum]['obj']

				inst = AddInstance(c,i,quarter,section,instructor_title,ratings)

				

		#print self.coursetypes.keys()

		#for ct in self.coursetypes.keys():
		#	name = self.coursetypes[ct]
		#	print "%s:%s"%(ct,name)


		#for i in self.instructors.keys():
		#	print "\n%s taught %d courses"%(i,self.instructors[i]['courses'])
		#	for course in self.instructors[i]['titles']:
		#		print "\t%s"%(course)

		#for dept in sorted(self.depts.keys()):
		#	print "\n%s"%(dept)
		#	for num in sorted(self.depts[dept]['courses']):
		#		print "\t%3s - %d"%(num,self.depts[dept]['courses'][num])

		#print "\n\n"
		#for q in self.quarters:
		#	print q

		
			#for course in self.depts[dept]['courses'].keys():
				#print "    %s"%(course)
				#print "        %s"%(self.depts[dept]['courses'][course]['ratings'])





