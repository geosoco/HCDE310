from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tastypie.api import Api
from main.api import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


v1_api = Api(api_name='v1')
v1_api.register(CurriculumResource())
v1_api.register(CourseResource())
v1_api.register(InstructorResource())
v1_api.register(SectionResource())


urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^about/$', 'main.views.about'),
    url(r'^test/$', 'main.views.test'),
    url(r'^instructor/(?P<id>\d+)$', 'main.views.instructor'),
    url(r'^curriculum/(?P<id>\d+)$', 'main.views.department'),
    url(r'^course/(?P<id>\d+)$', 'main.views.course'),
    url(r'^course/(?P<curriculum>[\w\s]+)/(?P<num>\d{3})$', 'main.views.course_readable'),
    url(r'^section/(?P<curriculum>[\w\s]+)/(?P<num>\d{3})/(?P<year>\d{4})/(?P<quarter>\w{2})/(?P<section>\w*)$', 'main.views.section'),
    url(r'^curriculum/(?P<letter>\w)?$', 'main.views.curriculum'),
    url(r'^courselist/(?P<letter>\w)?$', 'main.views.courselist'),
    url(r'^instructorlist/(?P<letter>\w)?$', 'main.views.instructorlist'),

    #debug & test
    url(r'^sqldebug/$', 'main.views.sqldebug'),
    # Examples:
    # url(r'^$', 'HCDE310.views.home', name='home'),
    (r'^api/', include(v1_api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
