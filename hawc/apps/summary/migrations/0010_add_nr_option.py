# Generated by Django 1.9.8 on 2016-07-29 15:25


import json

from django.db import migrations


def add_merge_option(apps, schema_editor):
    Visual = apps.get_model("summary", "Visual")
    rob_types = [2, 3]
    for obj in Visual.objects.filter(visual_type__in=rob_types):
        try:
            settings = json.loads(obj.settings)
        except ValueError:
            settings = False

        if settings:
            settings["show_nr_legend"] = False
            obj.settings = json.dumps(settings)

            # don't change last_updated timestamp
            Visual.objects.filter(id=obj.id).update(settings=obj.settings)


def remove_merge_option(apps, schema_editor):
    Visual = apps.get_model("summary", "Visual")
    rob_types = [2, 3]
    for obj in Visual.objects.filter(visual_type__in=rob_types):
        try:
            settings = json.loads(obj.settings)
        except ValueError:
            settings = False

            if settings:
                settings.pop("show_nr_legend")
                obj.settings = json.dumps(settings)

                # don't change last_updated timestamp
                Visual.objects.filter(id=obj.id).update(settings=obj.settings)


class Migration(migrations.Migration):
    dependencies = [
        ("summary", "0009_add_data_pivot_merge_option"),
    ]

    operations = [
        migrations.RunPython(add_merge_option, reverse_code=remove_merge_option),
    ]
