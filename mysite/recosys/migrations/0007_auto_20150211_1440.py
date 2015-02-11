# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recosys', '0006_auto_20150211_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='n_movies',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movie',
            name='index',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='index',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='rated',
            field=jsonfield.fields.JSONField(blank=True, verbose_name='rated movies'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='watched',
            field=models.ManyToManyField(to='recosys.Movie', blank=True),
            preserve_default=True,
        ),
    ]
