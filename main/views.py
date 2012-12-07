# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import *
from main.models import Curriculum, Course, Section, Rating, Instructor
import simplejson as json


def index(request):
    return render(request, 'template.html', {"inner_page": 'index.html'})



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
    
def curriculum(request, id):
	return render(request, 'template.html', {"inner_page": 'curriculum.html'})
