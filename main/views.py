# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import *
from main.models import Departments, Courses, Instances, Ratings, Instructors
import simplejson as json


def index(request):
    return HttpResponse('test')


def test(request):
	return render_to_response('test.html', {'title': 'Super Fantastic', 'topic': 'Fun!'})


def instructor(request, id=1):
	i = get_object_or_404(Instructors, pk=long(id))
	c = Instances.objects.filter(idinstructor=i)
	return render_to_response('instructor.html', {"instructor" : i, "courseinstances" : c})


def department(request, id):
	d = get_object_or_404(Departments, pk=long(id))
	c = Courses.objects.filter(iddepartment=d)
	return render_to_response('department.html', {"department" : d, "courses" : c})


def course(request, id):
	c = get_object_or_404(Courses, pk=long(id))
	inst = Instances.objects.filter(idcourse=c)
	return render_to_response('course.html', {"course" : c, "instances" : inst})

