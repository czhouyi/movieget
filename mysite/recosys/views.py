from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from django.template import RequestContext, loader
# Create your views here.

from recosys.models import Movie
def index(request):
    latest_movie_list = Movie.objects.order_by('-date')[:5]
    #template = loader.get_template('recosys/index.html')
    #context = RequestContext(request, {'latest_movie_list':latest_movie_list,})
    #return HttpResponse(template.render(context))
    context = {'latest_movie_list':latest_movie_list}
    return render(request, 'recosys/index.html', context)
    

def detail(request, movie_id):
    #try: 
    #    movie = Movie.objects.get(pk=movie_id)
    #except Movie.DoesNotExist:
    #    raise Http404("Movie does not exist")
    movie = get_object_or_404(Movie, pk=movie_id) 
    return render(request, 'recosys/detail.html', {'id': movie.index})
