# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recosys', '0004_auto_20150211_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watched',
            field=models.ManyToManyField(to='recosys.Movie'),
            preserve_default=True,
        ),
    ]
