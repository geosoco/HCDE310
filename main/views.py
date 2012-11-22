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
	return HttpResponse('department')


def course(request, id):
	return HttpResponse('course')

