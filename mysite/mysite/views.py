from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse

from django.template import RequestContext, loader

from recosys.models import Movie
# Create your views here.

def index(request):
    latest_movie_list = Movie.objects.order_by('-date')[:5]
    context = {'latest_movie_list' : latest_movie_list}
    return render_to_response('index.html', context)