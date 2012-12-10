# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import *
from main.models import Curriculum, Course, Section, Rating, Instructor
import simplejson as json
from django.db import connection
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
	cur = get_object_or_404(Curriculum, abbreviation=curriculum)
	c = get_object_or_404(Course, idcurriculum=cur, number=num)
	s = get_object_or_404(Section, idcourse=c, year=year, quarter=quarter, section=section)
	return render(request, 'template.html', {"course" : c, "section" : s, "curriculum" : cur, "inner_page": 'course.html'})
    
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
