from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    url(r'^recosys/', include('recosys.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
