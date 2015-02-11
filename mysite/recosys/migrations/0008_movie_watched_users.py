# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recosys', '0007_auto_20150211_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='watched_users',
            field=models.IntegerField(verbose_name='Watched', default=0),
            preserve_default=True,
        ),
    ]
