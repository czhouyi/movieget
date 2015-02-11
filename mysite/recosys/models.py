from django.db import models
from django.utils import timezone
from jsonfield import JSONField

# Create your models here.
class MovieManager(models.Manager):
    def create_movie(self, index, name, avg_rate):
        movie = self.create(index=index, name=name, \
                            avg_rate=avg_rate,avg_rate2=0,date=timezone.now())
        return movie

class Movie(models.Model):
    index = models.CharField(max_length=200, unique=True)
    name  = models.CharField(max_length=200)
    avg_rate = models.FloatField(default=0)
    avg_rate2 = models.FloatField(default=0)
    date = models.DateTimeField('date released')
    watched_users = models.IntegerField("Watched",default=0)
    objects = MovieManager()
    def __str__(self):
        return self.name

class UserManager(models.Manager):
    def create_user(self, index, name):
        user = self.create(index=index, name=name)
        return user

#import collections
#class MyModel(models.Model):
#      json = JSONField(load_kwargs={'object_pairs_hook':
#                                    collections.OrderedDict})

class User(models.Model):
    index = models.CharField(max_length=200, unique=True)
    name  = models.CharField(max_length=200, blank=True)
    rated = JSONField("rated movies", blank=True, default={});
    watched = models.ManyToManyField(Movie, blank=True)
    n_movies = models.IntegerField(default=0)
    objects = UserManager()
    def __str__(self):
        return self.name
