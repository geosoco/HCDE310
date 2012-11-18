# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import *

def index(request):
    return HttpResponse('test')


def test(request):
	return render_to_response('test.html', {'title': 'Super Fantastic', 'topic': 'Fun!'})