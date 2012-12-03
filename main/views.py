# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import *
from main.models import Curriculum, Course, Section, Rating, Instructor
import simplejson as json


def index(request):
    return render(request, 'index.html')


def test(request):
	return render(request, 'test.html', {'title': 'Super Fantastic', 'topic': 'Fun!'})


def instructor(request, id=1):
	i = get_object_or_404(Instructor, pk=long(id))
	c = Section.objects.filter(idinstructor=i)
	return render(request, 'instructor.html', {"instructor" : i, "courseinstances" : c})


def department(request, id):
	d = get_object_or_404(Curriculum, pk=long(id))
	c = Course.objects.filter(idcurriculum=d)
	return render(request, 'department.html', {"department" : d, "courses" : c})


def course(request, id):
	c = get_object_or_404(Course, pk=long(id))
	inst = Section.objects.filter(idcourse=c.id)
	return render(request, 'course.html', {"course" : c, "sections" : inst})

def course_readable(request, curriculum, num):
	cur = get_object_or_404(Curriculum, abbreviation=curriculum)
	c = get_object_or_404(Course, idcurriculum=cur, number=num)
	inst = Section.objects.filter(idcourse=c.id)
	return render(request, 'course.html', {"course" : c, "sections" : inst})	


def section(request, curriculum, num, year, quarter, section):
	cur = get_object_or_404(Curriculum, abbreviation=curriculum)
	c = get_object_or_404(Course, idcurriculum=cur, number=num)
	s = get_object_or_404(Section, idcourse=c, year=year, quarter=quarter, section=section)
	return render(request, 'section.html', {"section" : s, "course" : c, "curriculum" : cur})