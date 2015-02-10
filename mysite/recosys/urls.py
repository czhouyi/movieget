from django.conf.urls import patterns, url

from recosys import views

urlpatterns = patterns('',\
                       url(r'^$',views.index, name='index'),\
                       url(r'^(?P<movie_id>\d+)/$', views.detail, name='detail'),
                      )
