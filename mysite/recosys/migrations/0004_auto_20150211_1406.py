# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recosys', '0003_remove_movie_avg_rate2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='watched',
        ),
        migrations.AddField(
            model_name='movie',
            name='avg_rate2',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='rated',
            field=jsonfield.fields.JSONField(verbose_name='rated movies', null=True),
            preserve_default=True,
        ),
    ]
