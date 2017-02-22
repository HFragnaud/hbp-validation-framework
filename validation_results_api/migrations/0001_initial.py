# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScientificModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(help_text=b'short descriptive name', max_length=200)),
                ('description', models.TextField()),
                ('species', models.CharField(help_text=b'species', max_length=100, blank=True)),
                ('brain_region', models.CharField(help_text=b'brain region, if applicable', max_length=100, blank=True)),
                ('cell_type', models.CharField(help_text=b'cell type, for single-cell models', max_length=100, blank=True)),
                ('author', models.TextField(help_text=b'Author(s) of this model')),
                ('source', models.URLField(help_text=b'Version control repository containing the source code of the model')),
            ],
        ),
        migrations.CreateModel(
            name='ScientificModelInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(max_length=64)),
                ('parameters', models.TextField()),
                ('model', models.ForeignKey(to='validation_results_api.ScientificModel')),
            ],
        ),
        migrations.CreateModel(
            name='ValidationTestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(help_text=b'Timestamp of when the simulation was run', auto_created=True)),
                ('test_definition', models.URLField(help_text=b'URI of the validation test definition')),
                ('results_storage', models.URLField(help_text=b'Location of data files produced by the test run')),
                ('result', models.FloatField(help_text=b'A numerical measure of the difference between model and experiment')),
                ('passed', models.NullBooleanField(help_text=b'Whether the test passed or failed')),
                ('platform', models.TextField(help_text=b'Computer system on which the simulation was run')),
                ('model_instance', models.ForeignKey(to='validation_results_api.ScientificModelInstance')),
            ],
        ),
    ]
