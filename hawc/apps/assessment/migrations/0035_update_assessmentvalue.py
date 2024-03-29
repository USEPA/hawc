# Generated by Django 3.2.18 on 2023-02-27 20:55


from django.db import migrations, models


def get_species_name(apps, schema_editor):
    AssessmentValue = apps.get_model("assessment", "AssessmentValue")
    Species = apps.get_model("assessment", "Species")
    updates = []
    for obj in AssessmentValue.objects.exclude(species_studied=""):
        obj.species_studied = Species.objects.get(pk=int(obj.species_studied)).name
        updates.append(obj)
    if updates:
        AssessmentValue.objects.bulk_update(updates, ["species_studied"])


class Migration(migrations.Migration):
    dependencies = [
        ("assessment", "0034_assessmentdetail_assessmentvalue"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assessmentvalue",
            name="non_adaf_value",
        ),
        migrations.AlterField(
            model_name="assessmentvalue",
            name="adaf",
            field=models.BooleanField(
                default=False,
                help_text="When checked, the ADAF note will appear as a footnote for the value. Add supporting information about ADAF in the comments.",
                verbose_name="Apply ADAF?",
            ),
        ),
        migrations.AlterField(
            model_name="assessmentvalue",
            name="duration",
            field=models.CharField(
                blank=True,
                help_text="Duration associated with the value (e.g., Chronic, Subchronic)",
                max_length=128,
                verbose_name="Value duration",
            ),
        ),
        migrations.AlterField(
            model_name="assessmentvalue",
            name="species_studied",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Provide information about the animal(s) studied, including species and strain information",
                verbose_name="Species and strain",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(get_species_name, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="assessmentdetail",
            name="report_id",
            field=models.CharField(
                blank=True,
                help_text="A external report number or identifier (e.g., a DOI, publication number)",
                max_length=128,
                verbose_name="Report identifier",
            ),
        ),
    ]
