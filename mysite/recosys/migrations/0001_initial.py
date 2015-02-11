# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('avg_rate', models.FloatField(default=0)),
                ('avg_rate2', models.FloatField(default=0)),
                ('date', models.DateTimeField(verbose_name='date released')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('n_movies', models.IntegerField(default=0)),
                ('watched', models.ManyToManyField(to='recosys.Movie')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
