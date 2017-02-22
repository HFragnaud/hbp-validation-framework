# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('validation_search_api', '0004_validationtestdefinition_species'),
    ]

    operations = [
        migrations.AddField(
            model_name='validationtestdefinition',
            name='age',
            field=models.CharField(help_text=b"age of animal, e.g. '6 weeks'", max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='validationtestdefinition',
            name='publication',
            field=models.CharField(help_text=b'Publication in which the validation data set was reported', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='validationtestdefinition',
            name='test_type',
            field=models.CharField(help_text=b'single cell activity, network structure, network activity, subcellular', max_length=100),
        ),
    ]
