# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-27 20:54


import json

from django.db import migrations


def add_merge_option(apps, schema_editor):
    DataPivot = apps.get_model("summary", "DataPivot")
    for obj in DataPivot.objects.all():
        try:
            settings = json.loads(obj.settings)
        except ValueError:
            settings = False

        if settings:
            settings["plot_settings"]["merge_aggressive"] = False
            obj.settings = json.dumps(settings)

            # don't change last_updated timestamp
            DataPivot.objects.filter(id=obj.id).update(settings=obj.settings)


def remove_merge_option(apps, schema_editor):
    DataPivot = apps.get_model("summary", "DataPivot")
    for obj in DataPivot.objects.all():
        try:
            settings = json.loads(obj.settings)
        except ValueError:
            settings = False

            if settings:
                settings["plot_settings"].pop("merge_aggressive")
                obj.settings = json.dumps(settings)

            # don't change last_updated timestamp
            DataPivot.objects.filter(id=obj.id).update(settings=obj.settings)


class Migration(migrations.Migration):

    dependencies = [
        ("summary", "0008_auto_20160608_1109"),
    ]

    operations = [
        migrations.RunPython(add_merge_option, reverse_code=remove_merge_option),
    ]
