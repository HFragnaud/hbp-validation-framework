# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('validation_search_api', '0008_auto_20170207_0911'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidationTestCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('repository', models.CharField(help_text=b'location of the code that defines the test', max_length=200)),
                ('version', models.CharField(help_text=b'version of the code that defines the test', max_length=128)),
                ('path', models.CharField(help_text=b'path to test class within Python code', max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='validationtestdefinition',
            name='code_location',
        ),
        migrations.AddField(
            model_name='validationtestcode',
            name='test_definition',
            field=models.ForeignKey(related_name='code', to='validation_search_api.ValidationTestDefinition', help_text=b'Validation test implemented by this code'),
        ),
    ]
