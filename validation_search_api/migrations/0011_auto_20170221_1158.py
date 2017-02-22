# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('validation_search_api', '0010_validationtestcode_timestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='validationtestcode',
            options={'get_latest_by': 'timestamp', 'verbose_name_plural': 'validation test code'},
        ),
    ]
