# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('validation_search_api', '0006_auto_20170207_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validationtestdefinition',
            name='data_type',
            field=models.CharField(help_text=b'type of comparison data (number, histogram, time series, etc.)', max_length=100),
        ),
        migrations.AlterField(
            model_name='validationtestdefinition',
            name='test_type',
            field=models.CharField(help_text=b'single cell activity, network structure, network activity, subcellular', max_length=100, choices=[(b'single cell', b'single cell activity'), (b'network structure', b'network structure'), (b'network activity', b'network activity'), (b'behaviour', b'behaviour'), (b'subcellular', b'subcellular')]),
        ),
    ]
