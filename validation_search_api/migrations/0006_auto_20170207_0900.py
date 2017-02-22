# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('validation_search_api', '0005_auto_20170203_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validationtestdefinition',
            name='data_modality',
            field=models.CharField(help_text=b'recording modality for comparison data (ephys, fMRI, 2-photon, etc)', max_length=100, choices=[(b'ephys', b'electrophysiology'), (b'fMRI', b'fMRI'), (b'2-photon', b'2-photon imaging')]),
        ),
        migrations.AlterField(
            model_name='validationtestdefinition',
            name='data_type',
            field=models.CharField(help_text=b'type of comparison data (number, histogram, time series, etc.)', max_length=100, choices=[(b'single cell', b'single cell activity'), (b'network structure', b'network structure'), (b'network activity', b'network activity'), (b'behaviour', b'behaviour'), (b'subcellular', b'subcellular')]),
        ),
    ]
