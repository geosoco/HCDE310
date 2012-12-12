# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import *
from main.models import Curriculum, Course, Section, Rating, Instructor, Meeting
import simplejson as json
from django.db import connection
from django.core import serializers
from django.db.models import Q
#from main.filters import *


def index(request):
    return render(request, 'template.html', {"inner_page": 'index.html'})

def about(request):
	hcde = Curriculum.objects.get(abbreviation='HCDE')
	psych = Curriculum.objects.get(abbreviation='PSYCH')
	cecilia = Instructor.objects.get(name__iexact='Cecilia Aragon')
	sean = Instructor.objects.get(name__iexact='Munson,Sean A')
	susan = Instructor.objects.get(name__iexact='Susan Joslyn')
	hcde310 = Course.objects.get(number='310', idcurriculum__abbreviation__iexact='HCDE')
	return render(request, 'template.html', {
		"inner_page": 'about.html', 
		'HCDE': hcde, 
		'PSYCH': psych, 
		'Sean': sean, 
		'Susan': susan, 
		'Cecilia': cecilia, 
		'HCDE310': hcde310})

def test(request):
	return render(request, 'template.html', {'title': 'Super Fantastic', 'topic': 'Fun!', "inner_page": 'index.html'})


def instructor(request, id=1):
	i = get_object_or_404(Instructor, pk=long(id))
	c = Section.objects.filter(idinstructor=i)
	return render(request, 'template.html', {"courseinstances" : c, "instructor" : i, "inner_page": 'instructor.html'})


def department(request, id):
	d = get_object_or_404(Curriculum, pk=long(id))
	c = Course.objects.filter(idcurriculum=d)
	return render(request, 'template.html', {"courses" : c, "department" : d, "inner_page": 'department.html'})


def course(request, id):
	c = get_object_or_404(Course, pk=long(id))
	inst = Section.objects.filter(idcourse=c.id)
	return render(request, 'template.html', {"course" : c, "sections" : inst, "inner_page": 'course.html'})

def course_readable(request, curriculum, num):
	cur = get_object_or_404(Curriculum, abbreviation=curriculum)
	c = get_object_or_404(Course, idcurriculum=cur, number=num)
	inst = Section.objects.filter(idcourse=c.id)
	return render(request, 'template.html', {"course" : c, "sections" : inst, "inner_page": 'course.html'})


def section(request, curriculum, num, year, quarter, section):
    times = [730,830,930,1030,1130,1230,1330,1430,1530,1630,1730,1830]
	cur = get_object_or_404(Curriculum, abbreviation=curriculum)
	c = get_object_or_404(Course, idcurriculum=cur, number=num)
	s = get_object_or_404(Section, idcourse=c, year=year, quarter=quarter, section=section)
	return render(request, 'template.html', {"course" : c, "section" : s, "curriculum" : cur, "inner_page": 'section.html', 'times':times})

    
def curriculum(request, letter=None):
    letters = map(chr, range(65, 91))
    if letter is None: 
        return render(request, 'template.html', {'inner_page': 'azlist.html', 'objtype' : 'department', 'letters': letters, 'pageurl':'curriculum/'})
    else:
        curlist = Curriculum.objects.filter(abbreviation__startswith=letter)
        return render(request, 'template.html', {'inner_page': 'objlist.html', 'objtype' : 'department', 'objects': curlist, 'letters': letters, 'pageurl':'curriculum/'})

def courselist(request, letter=None):
    letters = map(chr, range(65, 91))
    if letter is None: 
        return render(request, 'template.html', { 'inner_page': 'azlist.html', 'objtype': 'course', 'letters': letters, 'pageurl':'courselist/'})
    else:
        courses = Course.objects.filter(name__startswith=letter)
        return render(request, 'template.html', {'inner_page': 'objlist.html', 'objtype': 'course', 'objects': courses, 'letters': letters, 'pageurl':'courselist/'})

def instructorlist(request, letter=None):
    letters = map(chr, range(65, 91))
    if letter is None: 
        return render(request, 'template.html', { 'inner_page': 'azlist.html', 'objtype': 'instructor', 'letters': letters, 'pageurl':'instructorlist/'})
    else:
        instructors = Instructor.objects.filter(name__startswith=letter)
        return render(request, 'template.html', {'inner_page': 'objlist.html', 'objtype': 'instructor', 'objects': instructors, 'letters': letters, 'pageurl':'instructorlist/'})

def sqldebug(request):
	return render(request, 'sqldebug.html', {'sql_queries': connection.queries})


def search(request):
	semi_filtered = Course.objects.select_related().all()
	qset = ()
	if('query' in request.REQUEST):
		query = request.REQUEST['query']
		qset = (
			Q(name__icontains=query) |
			Q(description__icontains=query) |
			Q(curriculum__abbreviation__icontains=query)
		)

	#if 'starttime' in request.REQUEST:
	#	st = request.REQUEST['starttime']
	#	semi_filtered = semi_filtered.filter(section__meeting__starttime__gte=st)

	#if 'endtime' in request.REQUEST:
	#	st = request.REQUEST['endtime']
	#	semi_filtered = semi_filtered.filter(section__meeting__endtime__gte=st)

 	if "ger" in request.REQUEST:
	    ger = int(request.REQUEST['ger'])
	    semi_filtered = semi_filtered.extra(where=["GenEdReqs & %s = %s"], params=(ger, ger))

	if "days" in request.REQUEST:
	    d = (~int(request.REQUEST['days'])) & 255
	    semi_filtered = semi_filtered.extra(where=["meeting.Day & %s = 0"], params=(d), tables=['section', 'meeting'])



	objs = semi_filtered.filter(qset)


	data = {}
	data['count'] = objs.count()
	data['items'] = []
	data['page'] = 0
	data['page_count'] = 0

	items = []
	for o in objs:
		item = {}
		item['curriculum'] = { 'id': o.curriculum.id , 'abbreviation': o.curriculum.abbreviation, 'name': o.curriculum.name }
		item['number'] = o.number
		item['GenEdReqs'] = o.genedreqs
		item['description'] = o.description
		item['name'] = o.name
		item['comment'] = o.comment
		item['mincredits'] = o.mincredits
		item['maxcredits'] = o.maxcredits
		sections = []
		for s in o.section_set.all():
			section = {}
			section['id'] = s.id
			section['section'] = s.section
			section['quarter'] = s.quarter
			section['year'] = s.year
			section['num_enrolled'] = s.numenrolled
			section['max_enrolled'] = s.maxenrollment
			section['sln'] = s.sln
			meetings = []
			for m in s.meeting_set.all():
				meeting = {}
				meeting['day'] = m.day
				meeting['starttime'] = m.starttime
				meeting['endtime'] = m.endtime
				meeting['type'] = m.meetingtype.name
				meeting['room'] = m.room.name
				meeting['building'] = m.room.building.abbreviation
				meetings.append(meeting)
			section['meetings'] = meetings
			sections.append(section)
		item['sections'] = sections
		items.append(item)

	data['items'] = items

	jsondata = json.dumps(data)

	#data = serializers.serialize("json", Meeting.objects.select_related().filter(qset), relations={
	#	'room' : {'relations': ('building',)}, 
	#	'section' : {
	#		'relations': { 
	#			'course' : {'relations': ('curriculum',) } 
	#		}
	#	}
	#})
	return HttpResponse(jsondata, mimetype='application/json; charset=utf-8')


