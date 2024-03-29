# Generated by Django 3.2.15 on 2022-10-20 20:24

from django.db import migrations, models
from django.db.models import F


def update_bmd_version(apps, schema_editor, version: str):
    # update BMD version for all assessments modeling completed
    AssessmentSettings = apps.get_model("bmd", "AssessmentSettings")
    Session = apps.get_model("bmd", "Session")
    qs = (
        Session.objects.annotate(assessment_id=F("endpoint__assessment_id"))
        .values_list("assessment_id", flat=True)
        .order_by("assessment_id")
        .distinct("assessment_id")
    )
    AssessmentSettings.objects.exclude(assessment_id__in=qs).update(version=version)


def update_forwards(apps, schema_editor):
    update_bmd_version(apps, schema_editor, "BMDS330")


def update_backwards(apps, schema_editor):
    update_bmd_version(apps, schema_editor, "BMDS270")


class Migration(migrations.Migration):
    dependencies = [
        ("bmd", "0007_selected_units"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assessmentsettings",
            name="version",
            field=models.CharField(
                choices=[
                    ("BMDS2601", "BMDS 2.6.0.1"),
                    ("BMDS270", "BMDS 2.7"),
                    ("BMDS330", "BMDS 3.3 (2022.10)"),
                ],
                default="BMDS330",
                max_length=10,
                help_text="Select the BMDS version to be used for dose-response modeling. Version 2 is no longer supported for execution; but results will be available for any version after execution is complete.",
            ),
        ),
        migrations.AlterField(
            model_name="session",
            name="version",
            field=models.CharField(
                choices=[
                    ("BMDS2601", "BMDS 2.6.0.1"),
                    ("BMDS270", "BMDS 2.7"),
                    ("BMDS330", "BMDS 3.3 (2022.10)"),
                ],
                max_length=10,
            ),
        ),
        migrations.RunPython(update_forwards, reverse_code=update_backwards),
    ]
