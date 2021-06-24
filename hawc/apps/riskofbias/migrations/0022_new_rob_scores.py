# Generated by Django 2.2.11 on 2020-07-14 18:44

from django.db import migrations, models


def update_overall_confidence(apps, schema_editor):
    RiskOfBiasScore = apps.get_model("riskofbias", "RiskOfBiasScore")
    RiskOfBiasScore.objects.filter(metric__domain__is_overall_confidence=True, score=24).update(
        score=34
    )
    RiskOfBiasScore.objects.filter(metric__domain__is_overall_confidence=True, score=25).update(
        score=35
    )
    RiskOfBiasScore.objects.filter(metric__domain__is_overall_confidence=True, score=26).update(
        score=36
    )
    RiskOfBiasScore.objects.filter(metric__domain__is_overall_confidence=True, score=27).update(
        score=37
    )


def rollback_changes(apps, schema_editor):
    RiskOfBiasScore = apps.get_model("riskofbias", "RiskOfBiasScore")
    RiskOfBiasScore.objects.filter(metric__domain__is_overall_confidence=True, score=34).update(
        score=24
    )
    RiskOfBiasScore.objects.filter(metric__domain__is_overall_confidence=True, score=35).update(
        score=25
    )
    RiskOfBiasScore.objects.filter(metric__domain__is_overall_confidence=True, score=36).update(
        score=26
    )
    RiskOfBiasScore.objects.filter(metric__domain__is_overall_confidence=True, score=37).update(
        score=27
    )


class Migration(migrations.Migration):

    dependencies = [
        ("riskofbias", "0021_riskofbiasscore_bias_direction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="riskofbiasscore",
            name="score",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "None"),
                    (10, "Not applicable"),
                    (12, "Not reported"),
                    (14, "Definitely high risk of bias"),
                    (15, "Probably high risk of bias"),
                    (16, "Probably low risk of bias"),
                    (17, "Definitely low risk of bias"),
                    (20, "Not applicable"),
                    (22, "Not reported"),
                    (24, "Critically deficient"),
                    (25, "Deficient"),
                    (26, "Adequate"),
                    (27, "Good"),
                    (34, "Uninformative"),
                    (35, "Low confidence"),
                    (36, "Medium confidence"),
                    (37, "High confidence"),
                    (40, "Yes"),
                    (41, "No"),
                ],
            ),
        ),
        migrations.RunPython(update_overall_confidence, reverse_code=rollback_changes),
    ]
