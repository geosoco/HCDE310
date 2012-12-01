from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^test/$', 'main.views.test'),
    url(r'^instructor/(?P<id>\d+)$', 'main.views.instructor'),
    url(r'^dept/(?P<id>\d+)$', 'main.views.department'),
    url(r'^course/(?P<id>\d+)$', 'main.views.course'),
    # Examples:
    # url(r'^$', 'HCDE310.views.home', name='home'),
    # url(r'^HCDE310/', include('HCDE310.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
