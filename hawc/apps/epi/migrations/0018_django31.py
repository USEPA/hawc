# Generated by Django 3.1.2 on 2020-10-15 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("epi", "0017_endpoint_ordering"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="isControl",
            field=models.BooleanField(
                blank=True,
                choices=[(True, "Yes"), (False, "No"), (None, "N/A")],
                default=None,
                help_text="Should this group be interpreted as a null/control group, if applicable",
                null=True,
                verbose_name="Control?",
            ),
        ),
    ]
