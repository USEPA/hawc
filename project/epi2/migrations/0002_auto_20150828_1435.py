# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import migrations
from django.core.management import call_command


def load_fixture(apps, schema_editor):
    # Fixtures adapted from:
    # https://www.fsd1.org/powerschool/Documents/PDFs/Federal_Race_Ethnicity_Guidelines.pdf
    # https://www.iso.org/obp/ui/
    fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
    call_command('loaddata', os.path.join(fixture_dir, 'ethnicity.json'), app_label='epi2')
    call_command('loaddata', os.path.join(fixture_dir, 'countries.json'), app_label='epi2')
    call_command('loaddata', os.path.join(fixture_dir, 'resultmetric.json'), app_label='epi2')


def unload_fixture(apps, schema_editor):
    apps.get_model("epi2", "Ethnicity").objects.all().delete()
    apps.get_model("epi2", "Country").objects.all().delete()
    apps.get_model("epi2", "ResultMetric").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('epi2', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
