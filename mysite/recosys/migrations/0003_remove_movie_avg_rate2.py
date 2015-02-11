# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recosys', '0002_remove_user_n_movies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='avg_rate2',
        ),
    ]
