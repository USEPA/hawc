# Generated by Django 1.11.4 on 2018-03-02 20:00

from django.db import migrations, models

from ...common.models import CustomURLField


class Migration(migrations.Migration):
    dependencies = [
        ("lit", "0009_auto_20151130_1456"),
    ]

    operations = [
        migrations.AlterField(
            model_name="identifiers",
            name="database",
            field=models.IntegerField(
                choices=[
                    (0, "External link"),
                    (1, "PubMed"),
                    (2, "HERO"),
                    (3, "RIS (EndNote/Reference Manager)"),
                    (4, "DOI"),
                    (5, "Web of Science"),
                    (6, "Scopus"),
                    (7, "Embase"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="reference",
            name="block_id",
            field=models.DateTimeField(
                blank=True,
                help_text="Used internally for determining when reference was originally added",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="reference",
            name="full_text_url",
            field=CustomURLField(
                blank=True,
                help_text="Link to full-text publication (may require increased access privileges, only reviewers and team-members)",
            ),
        ),
        migrations.AlterField(
            model_name="search",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="A more detailed description of the literature search or import strategy.",
            ),
        ),
        migrations.AlterField(
            model_name="search",
            name="import_file",
            field=models.FileField(blank=True, upload_to="lit-search-import"),
        ),
        migrations.AlterField(
            model_name="search",
            name="search_string",
            field=models.TextField(
                blank=True,
                help_text="The search-text used to query an online database. Use colors to separate search-terms (optional).",
            ),
        ),
        migrations.AlterField(
            model_name="search",
            name="search_type",
            field=models.CharField(choices=[("s", "Search"), ("i", "Import")], max_length=1),
        ),
        migrations.AlterField(
            model_name="search",
            name="slug",
            field=models.SlugField(
                help_text="The URL (web address) used to describe this object (no spaces or special-characters).",
                verbose_name="URL Name",
            ),
        ),
        migrations.AlterField(
            model_name="search",
            name="source",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "External link"),
                    (1, "PubMed"),
                    (2, "HERO"),
                    (3, "RIS (EndNote/Reference Manager)"),
                    (4, "DOI"),
                    (5, "Web of Science"),
                    (6, "Scopus"),
                    (7, "Embase"),
                ],
                help_text="Database used to identify literature.",
            ),
        ),
        migrations.AlterField(
            model_name="search",
            name="title",
            field=models.CharField(
                help_text="A brief-description to describe the identified literature.",
                max_length=128,
            ),
        ),
    ]
