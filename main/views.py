# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    return HttpResponse('test')