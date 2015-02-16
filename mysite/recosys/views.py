from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse

from django.template import RequestContext, loader
# Create your views here.

from recosys.models import Movie

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.avg_rate = round(movie.avg_rate/2)
    return render_to_response('recosys/detail.html', {'movie': movie})
