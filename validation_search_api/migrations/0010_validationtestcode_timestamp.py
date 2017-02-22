# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('validation_search_api', '0009_auto_20170221_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='validationtestcode',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 21, 8, 40, 30, 207438, tzinfo=utc), help_text=b'timestamp for this version of the code', auto_now_add=True),
            preserve_default=False,
        ),
    ]
