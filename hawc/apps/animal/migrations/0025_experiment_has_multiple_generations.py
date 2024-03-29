# Generated by Django 1.11.18 on 2019-11-26 21:46

from django.db import migrations, models


def set_multiple_generations(apps, schema_editor):
    Experiment = apps.get_model("animal", "Experiment")
    Experiment.objects.all().update(has_multiple_generations=False)
    Experiment.objects.filter(type__in=("Rp", "Dv")).update(has_multiple_generations=True)


class Migration(migrations.Migration):
    dependencies = [
        ("animal", "0024_change_choices"),
    ]

    operations = [
        migrations.AddField(
            model_name="experiment",
            name="has_multiple_generations",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(set_multiple_generations),
    ]
