# Generated by Django 3.1.2 on 2020-10-15 14:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("invitro", "0010_endpoint_ordering"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ivendpointgroup",
            name="cytotoxicity_observed",
            field=models.BooleanField(
                choices=[(None, "not reported"), (False, "not observed"), (True, "observed")],
                default=None,
                null=True,
                blank=True,
            ),
        ),
        migrations.AlterField(
            model_name="ivendpointgroup",
            name="precipitation_observed",
            field=models.BooleanField(
                choices=[(None, "not reported"), (False, "not observed"), (True, "observed")],
                default=None,
                null=True,
                blank=True,
            ),
        ),
    ]
