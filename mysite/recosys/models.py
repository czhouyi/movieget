from django.db import models

# Create your models here.
class Movie(models.Model):
    index = models.CharField(max_length=200)
    name  = models.CharField(max_length=200)
    avg_rate = models.IntegerField(default=0)
    date = models.DateTimeField('date released')

    def __str__(self):
        return self.name

class User(models.Model):
    index = models.CharField(max_length=200)
    name  = models.CharField(max_length=200)
    movie = models.ForeignKey(Movie) 

    def __str__(self):
        return self.name
