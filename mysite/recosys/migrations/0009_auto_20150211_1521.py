# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recosys', '0008_movie_watched_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rated',
            field=jsonfield.fields.JSONField(default={}, verbose_name='rated movies', blank=True),
            preserve_default=True,
        ),
    ]
