from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect as redirect

from views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    url(r'^$', lambda x: redirect('/index/')),
    url(r'^index/', index),
    url(r'^recosys/', include('recosys.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
