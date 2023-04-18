# Generated by Django 1.9.9 on 2016-09-13 15:32


from django.db import migrations, models


def disable_mgmt(apps, schema_editor):
    # Disable management module for existing assessments.
    apps.get_model("assessment", "Assessment").objects.all().update(enable_project_management=False)


class Migration(migrations.Migration):
    dependencies = [
        ("assessment", "0008_auto_20160802_1626"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessment",
            name="enable_project_management",
            field=models.BooleanField(
                default=True,
                help_text=b"Enable project management module for data extraction and risk of bias. If enabled, each study will have multiple tasks which can be assigned and tracked for completion.",
            ),
        ),
        migrations.RunPython(disable_mgmt, reverse_code=migrations.RunPython.noop),
    ]
