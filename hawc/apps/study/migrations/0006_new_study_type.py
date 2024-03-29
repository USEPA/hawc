# Generated by Django 1.9.8 on 2016-07-25 16:16


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("study", "0005_auto_20160606_1424"),
    ]

    operations = [
        # create new fields
        migrations.AddField(
            model_name="study",
            name="bioassay",
            field=models.BooleanField(
                default=False,
                verbose_name="Animal bioassay",
                help_text=b"Study contains animal bioassay data",
            ),
        ),
        migrations.AddField(
            model_name="study",
            name="epi",
            field=models.BooleanField(
                default=False,
                verbose_name="Epidemiology",
                help_text=b"Study contains epidemiology data",
            ),
        ),
        migrations.AddField(
            model_name="study",
            name="epi_meta",
            field=models.BooleanField(
                default=False,
                verbose_name="Epidemiology meta-analysis",
                help_text=b"Study contains epidemiology meta-analysis/pooled analysis data",
            ),
        ),
        migrations.AddField(
            model_name="study",
            name="in_vitro",
            field=models.BooleanField(default=False, help_text=b"Study contains in-vitro data"),
        ),
        # make optional (for removal)
        migrations.AlterField(
            model_name="study",
            name="study_type",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, b"Animal Bioassay"),
                    (1, b"Epidemiology"),
                    (4, b"Epidemiology meta-analysis/pooled analysis"),
                    (2, b"In vitro"),
                    (3, b"Other"),
                ],
                help_text=b"Type of data captured in the selected study. This determines which fields are required for data-extraction.",
                null=True,
            ),
        ),
    ]
