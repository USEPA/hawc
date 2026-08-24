from typing import Self

import reversion
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from ..assessment.models import DSSTox, EffectTag
from ..common.models import clone_name
from ..vocab.constants import ObservationStatus
from ..vocab.models import Guideline, GuidelineProfile, Term
from . import constants, managers


class Experiment(models.Model):
    objects = managers.ExperimentManager()

    study = models.ForeignKey(
        "study.Study", on_delete=models.CASCADE, related_name="v2_experiments"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Experiment name",
        help_text="""Short-text used to describe the experiment (i.e. 2-Year Cancer Bioassay, 10-Day Oral, 28-Day Inhalation, etc.) using title style (all words capitalized). If study contains more than one chemical, then also include the chemical name (e.g. 28-Day Oral PFBS).""",
    )
    experiment_type = models.CharField(
        blank=True,
        default="",
        max_length=3,
        choices=constants.ExperimentType.choices,
        help_text="""Classification to describe animal toxicity testing that was conducted. Based on either dose period, subjects involved, or measured effects of interest, 
select the most-relevant option. The option 'other' can be used for atypical study designs.""",
    )
    experiment_type_other = models.CharField(
        blank=True, default="", verbose_name="Other Experiment Type Details"
    )
    dev_or_repro_toxicity_types = ArrayField(
        models.CharField(max_length=2, choices=constants.DevelopmentalOrReproductiveToxicityType),
        help_text="Select the type(s) of developmental or reproductive toxicity study.",
        verbose_name="Developmental Toxicity and Reproduction Study Details",
    )
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    BREADCRUMB_PARENT = "study"

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name

    # TODO - make a generic version of this available via mixin that uses naming convention + introspection to work...
    def get_other_aware_experiment_type(self):
        return (
            self.get_experiment_type_display()
            if self.experiment_type != constants.ExperimentType.OTH
            else f"other ({self.experiment_type_other})"
        )

    def get_absolute_url(self):
        return reverse("animalv2:experiment_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("animalv2:experiment_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("animalv2:experiment_delete", args=(self.pk,))

    def get_assessment(self):
        return self.study.get_assessment()

    def get_study(self):
        return self.study


reversion.register(Experiment)
