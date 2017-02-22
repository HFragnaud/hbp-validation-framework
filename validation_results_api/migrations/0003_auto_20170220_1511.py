# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('validation_results_api', '0002_auto_20170220_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validationtestresult',
            name='timestamp',
            field=models.DateTimeField(help_text=b'Timestamp of when the simulation was run', auto_now_add=True),
        ),
    ]
