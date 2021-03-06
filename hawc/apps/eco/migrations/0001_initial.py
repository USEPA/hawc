# Generated by Django 3.2.13 on 2022-04-13 20:43
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("epi", "0018_django31"),
        ("taggit", "0004_alter_taggeditem_content_type_alter_taggeditem_tag"),
        ("study", "0011_auto_20190416_2035"),
    ]

    operations = [
        migrations.CreateModel(
            name="State",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("code", models.CharField(max_length=2, unique=True)),
                ("name", models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Vocab",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "category",
                    models.IntegerField(
                        choices=[
                            (0, "Study type"),
                            (1, "Study setting"),
                            (2, "Habitat"),
                            (3, "Cause term"),
                            (4, "Cause measure"),
                            (5, "Biological organization"),
                            (6, "Effect term"),
                            (7, "Effect measure"),
                            (8, "Response measure type"),
                            (9, "Response variability"),
                            (10, "Statistical significance measure"),
                            (11, "Climate"),
                            (12, "Ecoregion"),
                        ]
                    ),
                ),
                ("value", models.CharField(max_length=100)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.deletion.CASCADE,
                        related_name="children",
                        related_query_name="children",
                        to="eco.vocab",
                    ),
                ),
            ],
            options={
                "verbose_name": "Controlled vocabulary",
                "verbose_name_plural": "Vocabularies",
            },
        ),
        migrations.CreateModel(
            name="Effect",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "measure_detail",
                    models.CharField(
                        blank=True,
                        help_text="Add help-text. autocomplete?",
                        max_length=100,
                        verbose_name="Effect measure detail",
                    ),
                ),
                (
                    "units",
                    models.CharField(
                        help_text="Type the unit associated with the effect term. autocomplete?",
                        max_length=100,
                        verbose_name="Effect units",
                    ),
                ),
                (
                    "species",
                    models.CharField(
                        blank=True,
                        help_text="Type the species name, if applicable; use the format Common name (Latin binomial)",
                        max_length=100,
                        verbose_name="Effect species",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        help_text="Type any other useful information not captured in other fields",
                        verbose_name="Effect comment",
                    ),
                ),
                (
                    "as_reported",
                    models.TextField(
                        help_text="Copy and paste exact phrase up to 1-2 sentences from article. If not stated in the article, leave blank.",
                        verbose_name="Effect as reported",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "bio_org",
                    models.ForeignKey(
                        blank=True,
                        help_text="Select the level of biological organization associated with the effect, if applicable",
                        limit_choices_to={"category": 5},
                        null=True,
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                        verbose_name="Level of biological organization",
                    ),
                ),
                (
                    "measure",
                    models.ForeignKey(
                        help_text="Add help-text. autocomplete?",
                        limit_choices_to={"category": 7},
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                        verbose_name="Effect measure",
                    ),
                ),
                (
                    "modifying_factors",
                    taggit.managers.TaggableManager(
                        help_text="Type a comma-separated list of any modifying factors, confounding variables, model co-variates, etc. that were analyzed and tested for the potential to influence the relationship between cause and effect",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Modifying factors",
                    ),
                ),
                (
                    "study",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, to="study.study"),
                ),
                (
                    "term",
                    models.ForeignKey(
                        limit_choices_to={"category": 6},
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                        verbose_name="Effect term",
                    ),
                ),
            ],
            options={
                "verbose_name": "Effect/Response",
            },
        ),
        migrations.CreateModel(
            name="Design",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "habitat_as_reported",
                    models.TextField(
                        blank=True,
                        help_text="Copy and paste exact phrase up to 1-2 sentences from article. If not stated in the article, leave blank.",
                        verbose_name="Habitat as reported",
                    ),
                ),
                (
                    "climate_as_reported",
                    models.TextField(
                        blank=True,
                        help_text="Copy and paste exact phrase up to 1-2 sentences from article. If not stated in the article, leave blank.",
                        verbose_name="Climate as reported",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "climate",
                    models.ManyToManyField(
                        help_text="Select one or more climates to which the evidence applies",
                        limit_choices_to={"category": 11},
                        related_name="_eco_design_climate_+",
                        to="eco.Vocab",
                    ),
                ),
                (
                    "countries",
                    models.ManyToManyField(
                        help_text="Select one or more countries",
                        related_name="eco_designs",
                        to="epi.Country",
                    ),
                ),
                (
                    "design",
                    models.ForeignKey(
                        help_text="Select study design",
                        limit_choices_to={"category": 0},
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                    ),
                ),
                (
                    "ecoregion",
                    models.ManyToManyField(
                        help_text="Select one or more Level III Ecoregions, if known",
                        limit_choices_to={"category": 12},
                        related_name="_eco_design_ecoregion_+",
                        to="eco.Vocab",
                    ),
                ),
                (
                    "habitat",
                    models.ForeignKey(
                        help_text="Select the habitat to which the evidence applies",
                        limit_choices_to={"category": 2},
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                        verbose_name="Habitat",
                    ),
                ),
                (
                    "state",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Select one or more states, if applicable.",
                        to="eco.State",
                    ),
                ),
                (
                    "study",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, to="study.study"),
                ),
                (
                    "study_setting",
                    models.ForeignKey(
                        help_text="Select the setting in which evidence was generated",
                        limit_choices_to={"category": 1},
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ecological Design",
                "verbose_name_plural": "Ecological Designs",
            },
        ),
        migrations.CreateModel(
            name="Cause",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "measure_detail",
                    models.TextField(blank=True, verbose_name="Cause measure detail"),
                ),
                (
                    "units",
                    models.CharField(
                        help_text="Type the unit associated with the cause term. autocomplete?",
                        max_length=100,
                        verbose_name="Cause units",
                    ),
                ),
                (
                    "species",
                    models.CharField(
                        blank=True,
                        help_text="Type the species name, if applicable; use the format Common name (Latin binomial)",
                        max_length=100,
                        verbose_name="Cause/treatment species",
                    ),
                ),
                (
                    "level",
                    models.CharField(
                        help_text="Describe the specific treatment/exposure/dose level or range of levels of the cause measure",
                        max_length=128,
                        verbose_name="Cause/treatment level",
                    ),
                ),
                (
                    "level_value",
                    models.FloatField(
                        blank=True,
                        help_text="Type the the specific treatment/exposure/dose level (if applicable)",
                        null=True,
                        verbose_name="Cause/treatment value",
                    ),
                ),
                (
                    "level_units",
                    models.CharField(
                        help_text="Type the units associated with the cause value term",
                        max_length=100,
                        verbose_name="Cause/treatment level units",
                    ),
                ),
                (
                    "duration",
                    models.CharField(
                        help_text="Describe the duration or range of durations of the treatment/exposure",
                        max_length=100,
                        verbose_name="Cause/treatment duration",
                    ),
                ),
                (
                    "duration_value",
                    models.FloatField(
                        blank=True,
                        help_text="Type the numeric value of the specific duration of the treatment/exposure",
                        null=True,
                        verbose_name="Cause/treatment duration value",
                    ),
                ),
                (
                    "duration_units",
                    models.CharField(
                        blank=True,
                        help_text="Type the unit associated with the cause duration term. Autocomplete.",
                        max_length=100,
                        verbose_name="Cause/treatment duration units",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        help_text="Type any other useful information not captured in other fields",
                        verbose_name="Cause/treatment comment",
                    ),
                ),
                (
                    "as_reported",
                    models.TextField(
                        help_text="Copy and paste exact phrase up to 1-2 sentences from article. If not stated in the article, leave blank.",
                        verbose_name="Cause/treatment as reported",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "bio_org",
                    models.ForeignKey(
                        blank=True,
                        help_text="Select the level of biological organization associated with the cause, if applicable",
                        limit_choices_to={"category": 5},
                        null=True,
                        on_delete=models.deletion.CASCADE,
                        to="eco.vocab",
                        verbose_name="Level of biological organization",
                    ),
                ),
                (
                    "measure",
                    models.ForeignKey(
                        help_text="Add help text - autocomplete field?",
                        limit_choices_to={"category": 4},
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                    ),
                ),
                (
                    "study",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, to="study.study"),
                ),
                (
                    "term",
                    models.ForeignKey(
                        help_text="Add help text - autocomplete field?",
                        limit_choices_to={"category": 3},
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cause/Treatment",
            },
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "sort_order",
                    models.PositiveSmallIntegerField(
                        default=0,
                        help_text="Sort order of a multiple responses",
                        verbose_name="Sort order",
                    ),
                ),
                (
                    "relationship_direction",
                    models.IntegerField(
                        choices=[
                            (0, "Increase"),
                            (1, "Decrease"),
                            (2, "Change"),
                            (3, "No change"),
                            (10, "Other"),
                        ],
                        help_text="Select the direction of the relationship between selected cause and effect",
                        verbose_name="Direction of relationship",
                    ),
                ),
                (
                    "relationship_comment",
                    models.TextField(
                        blank=True,
                        help_text="Describe the relationship in 1-2 sentences",
                        verbose_name="Relationship comment",
                    ),
                ),
                (
                    "modifying_factors_comment",
                    models.TextField(
                        blank=True,
                        help_text="Describe how the important modifying factor(s) affect the relationship in 1-2 sentences. Consider factors associated with the study that have an important influence on the relationship between cause and effect. For example, statistical significance of a co-variate in a model can indicate importance.",
                        verbose_name="Modifying factors comment",
                    ),
                ),
                (
                    "sample_size",
                    models.IntegerField(
                        blank=True,
                        help_text="Type the number of samples used to calculate the response measure value, if known",
                        null=True,
                        verbose_name="Sample size",
                    ),
                ),
                (
                    "measure_value",
                    models.FloatField(
                        blank=True,
                        help_text="Numerical value of the response measure",
                        null=True,
                        verbose_name="Response measure value",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Describe any other useful information about the response measure not captured in other fields",
                        verbose_name="Response measure description",
                    ),
                ),
                (
                    "low_variability",
                    models.FloatField(
                        blank=True,
                        help_text="Type the lower numerical bound of the response variability",
                        null=True,
                        verbose_name="Lower response variability measure",
                    ),
                ),
                (
                    "upper_variability",
                    models.FloatField(
                        blank=True,
                        help_text="Type the upper numerical bound of the response variability",
                        null=True,
                        verbose_name="Upper response variability measure",
                    ),
                ),
                (
                    "statistical_sig_value",
                    models.FloatField(
                        blank=True,
                        help_text="Type the numerical value of the statistical significance",
                        null=True,
                        verbose_name="Statistical significance measure value",
                    ),
                ),
                (
                    "derived_value",
                    models.FloatField(
                        blank=True,
                        help_text="Calculation from 'response measure value' based on a formula linked to 'response measure type', if applicable",
                        null=True,
                        verbose_name="Derived response measure value",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "cause",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="eco.cause", related_name="results"
                    ),
                ),
                (
                    "design",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="eco.design", related_name="results"
                    ),
                ),
                (
                    "effect",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="eco.effect", related_name="results"
                    ),
                ),
                (
                    "measure_type",
                    models.ForeignKey(
                        help_text="Select one response measure type",
                        limit_choices_to=models.Q(("category", 8), ("parent__isnull", False)),
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                        verbose_name="Response measure type",
                    ),
                ),
                (
                    "statistical_sig_type",
                    models.ForeignKey(
                        help_text="Select the type of statistical significance measure reported",
                        limit_choices_to={"category": 10},
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                        verbose_name="Statistical significance measure type",
                    ),
                ),
                (
                    "study",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        to="study.study",
                        related_name="eco_results",
                    ),
                ),
                (
                    "variability",
                    models.ForeignKey(
                        help_text="Select how variability in the response measure was reported, if applicable",
                        limit_choices_to={"category": 9},
                        on_delete=models.deletion.CASCADE,
                        related_name="+",
                        to="eco.vocab",
                        verbose_name="Response variability",
                    ),
                ),
            ],
            options={
                "verbose_name": "Result",
                "verbose_name_plural": "Results",
                "ordering": ("effect", "sort_order"),
                "unique_together": {("effect", "sort_order")},
            },
        ),
    ]
