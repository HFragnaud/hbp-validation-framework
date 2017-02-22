# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('validation_results_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validationtestresult',
            name='results_storage',
            field=models.TextField(help_text=b'Location of data files produced by the test run'),
        ),
    ]
