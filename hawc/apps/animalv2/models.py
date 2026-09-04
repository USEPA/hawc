from typing import Self

import reversion
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from ..assessment.models import DSSTox, EffectTag
from ..common.models import clone_name
from ..study.models import Study
from ..vocab.constants import ObservationStatus
from ..vocab.models import Guideline, GuidelineProfile, Term
from . import constants, managers


class Experiment(models.Model):
    objects = managers.ExperimentManager()

    study = models.ForeignKey(
        "study.Study", on_delete=models.CASCADE, related_name="aniv2_experiments"
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


class Chemical(models.Model):
    objects = managers.ChemicalManager()

    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="aniv2_chemicals")
    name = models.CharField(
        max_length=255,
        verbose_name="Chemical name",
        help_text="""Name of the chemical substance tested in the study. ‘<Not Reported>’ is an appropriate selection if this information is not reported within the document. Trade names and abbreviations are acceptable if they are specified as the tested material. Including the full chemical name or other listed synonyms is not necessary. This field is commonly used for visualizations, so consider using a common acronym, e.g., BPA instead of Bisphenol A.""",
    )
    dtxsid = models.ForeignKey(
        DSSTox,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Distributed Structure-Searchable Toxicity Database (DSSTox) substance identifier (recommended). When assigning a DTXSID, CASRN and preferred chemical name will populate from DSSTox.",
        related_name="aniv2_chemicals",
        help_text=DSSTox.help_text(),
    )
    casrn = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="Chemical identifier (CAS)",
        help_text="""CASRN: CAS (Chemical Abstracts Service) Registry Number. Leave blank if this information is not reported within the document.""",
    )
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    BREADCRUMB_PARENT = "study"

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name

    def get_assessment(self):
        return self.study.get_assessment()

    def get_study(self):
        return self.study

    def get_absolute_url(self):
        return reverse("animalv2:chemical_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("animalv2:chemical_update", args=(self.pk,))

    def get_delete_url(self):
        return reverse("animalv2:chemical_delete", args=(self.pk,))

    def clone(self):
        self.id = None
        self.name = clone_name(self, "name")
        self.save()
        return self


class TestSubstance(models.Model):
    objects = managers.TestSubstanceManager()

    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="testsubstances"
    )
    chemical = models.ForeignKey(Chemical, on_delete=models.CASCADE, related_name="testsubstances")

    source = models.CharField(
        max_length=255,
        help_text="""Any pertinent information regarding a substance’s origin (the corporation, organization, or facility that produced the substance) and catalog number if available. 
Other notable information about the test substance in general or special handling of the chemical, such as milling, can be noted in this field.""",
    )

    composition = models.CharField(
        blank=True,
        default="",
        max_length=3,
        choices=constants.TestSubstanceComposition.choices,
        help_text="""A chemical can be created for a mixture/product. If the chemical refers to the composition of the mixture/product. Select the chemical composition and specify the chemical composition in the “Composition Remarks” field.""",
    )

    composition_remarks = models.CharField(
        blank=True, max_length=255, help_text="Specify the chemical composition."
    )

    purity = models.CharField(
        blank=True,
        default="",
        max_length=2,
        choices=constants.TestSubstancePurity.choices,
        help_text="""If detailed information on the purity of the composition is not known, a qualitative statement can be provided in this field, e.g. 'analytical grade' or 'technical grade'.""",
    )

    percent_purity = models.CharField(
        max_length=255,
        verbose_name="% Purity",
        help_text="Provide the % purity or chemical composition",
    )

    expiration_date = models.DateField(help_text="Provide the expiration date or re-test date")

    lot_batch_number = models.CharField(
        max_length=255,
        verbose_name="Lot / Batch #",
        help_text="Lot or batch number assigned to chemical by chemical supplier. Leave blank if this information is not reported within the document.",
    )

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)

    def get_assessment(self):
        return self.experiment.get_assessment()

    def get_study(self):
        return self.experiment.get_study()

    def __str__(self):
        return f"{self.chemical.name} / {self.get_composition_display()}"

    def clone(self):
        self.id = None
        self.save()
        return self


class Guideline(models.Model):
    objects = managers.GuidelineManager()

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name="guidelines")

    guideline_status = models.CharField(
        default="",
        blank=True,
        max_length=2,
        choices=constants.YesNoNr.choices,
        help_text="""Select whether a guideline study was conducted.""",
    )

    name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Guideline name",
        help_text="""Name of the Office of Chemical Safety and Pollution Prevention (OCSPP) Health Effects or OECD (Organization for Economic Cooperation and Development) guideline to which a study (most closely) adheres to.""",
    )

    number = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Guideline number",
        help_text="""Number associated with the OCSPP or OECD guideline that a study (most closely) adheres to. Guideline numbers are differentiated by the distinct number proceeding 870/890, as dictated by the EPA Health Effects Test Guidelines. 
The guideline number should be entered in the box with both the acronym and full number. For example, “OPPTS 870.3700.”""",
    )

    version_year = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Guideline Version/Year",
        help_text="Describe the guideline version/year",
    )

    deviations = models.TextField(
        max_length=1500,
        blank=True,
        verbose_name="Guideline Deviations",
        help_text="""List each deviation from the protocol and classify the deviation as major or minor.  Also report any rationale provided by the investigator’s for the deviation.  Similarly list, classify, and discuss all other deficiencies with the conduct, results, and reporting of the study.  Discuss the possibility of resolving the deficiencies and what would be required.  Major deficiencies may be presented and discussed in paragraph form, whereas minor deficiencies can be presented in a bulleted list.""",
    )

    compliance = models.CharField(
        default="",
        blank=True,
        max_length=2,
        choices=constants.YesNoNr.choices,
        help_text="Are GLP and Quality Assurance statements provided, signed, and dated?",
    )

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)

    def get_assessment(self):
        return self.experiment.get_assessment()

    def get_study(self):
        return self.experiment.get_study()

    def __str__(self):
        return self.name

    def clone(self):
        self.id = None
        self.save()
        return self


class AnimalGroup(models.Model):
    objects = managers.AnimalGroupManager()

    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="aniv2_animalgroups"
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Animal Group Name",
        help_text="""Name should be sex, common strain name, species (plural) and use Title Style (e.g. Male Sprague Dawley Rat). For developmental toxicity and reproduction studies include the generation before the sex in title (e.g. F1 Male Sprague Dawley Rat or P0 Female C57 Mice). For cohort type include""",
    )

    generation = models.CharField(
        default="",
        max_length=2,
        choices=constants.AnimalGroupGeneration.choices,
        help_text="""Generation of the test animal group. F0: The default choice for animals exposed in non-reproductive studies (chronic CHR, subchronic SUB, subacute SAC), dams in reproductive DEV studies, and the first-generation mating group for multigenerational MGR studies. F1: The second generation, born to F0. F2: The third generation, born to F1. F3: The fourth generation, born to F2. Fetal: The fetal generation is the group produced by F0 matings in DEV studies, typically removed from a female via cesarean section. Pups from live births are not fetal.""",
    )

    generation_remarks = models.CharField(
        blank=True,
        max_length=255,
        default="",
        help_text='Specify the generation of the test animal for "other"',
    )

    cohort_type = models.CharField(
        default="",
        max_length=3,
        choices=constants.AnimalGroupCohortType.choices,
        help_text="""Select the term from the list below that best characterizes when the treatment group was evaluated for effects.<br><em>Satellite</em>: Group of animals included in the design and conduct of a toxicity study, treated, and housed under conditions identical to those of the main study animals, but used primarily for some separate purpose to be defined as needed in the Comment section.<br><em>Recovery</em>: Group examined after a recovery period that followed the dosing period at the end of the study. Recovery groups will have explicitly stated recovery periods. For example, if dosing stopped on day 15 and animals were sacrificed and examined on day 16 or later, this would be considered terminal and not recovery unless the study explicitly defines this time as recovery.<br><em>Sentinel</em>: Group used primarily for health or microbiological monitoring, not endpoint evaluation.<br><em>Interim</em>: Group sacrificed and examined within the dosing period.<br><em>Terminal</em>: Group sacrificed and examined at study completion and after the dosing period. These animals are not mated.<br><em>Post first mating</em>: Group examined after first mating.<br><em>Post second mating</em>: Group examined after second mating.<br><em>Post third mating</em>: Group examined after third mating.<br><em>Other</em>: Group of animals that may have deviated from the full study design, to be defined as needed in the “Cohort Type Remarks” field.""",
    )

    cohort_type_remarks = models.CharField(
        blank=True,
        max_length=255,
        default="",
        help_text="If “other” is selected for Cohort Type, describe the animal group.",
    )

    # INSERT species/strain/straingroup after checking w/ michelle...

    source = models.CharField(
        default="",
        max_length=3,
        verbose_name="Animal Source",
        choices=constants.AnimalGroupSource.choices,
    )

    source_remarks = models.CharField(
        verbose_name="Animal Source Remarks",
        blank=True,
        max_length=255,
        help_text="""Provide information on the source of the animal species and strain using complete genetic nomenclature. Provide the supplier’s name and address (if available)""",
    )

    sex = models.CharField(
        default="",
        max_length=2,
        choices=constants.AnimalGroupSex.choices,
    )

    number_of_animals = models.CharField(
        blank=True,
        max_length=255,
        help_text="Provide the full number of animals included in the study.",
    )

    age_and_condition = models.CharField(
        blank=True,
        verbose_name="Animal Age and Condition",
        max_length=255,
        help_text="Provide age, health status (e.g. good health, animal model of disease, etc.) and body weight range",
    )

    acclimatization = models.TextField(
        blank=True,
        max_length=2000,
        help_text="Describe the acclimatization period and animal husbandry conditions prior to the initiation of test method.",
    )

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)

    def get_assessment(self):
        return self.experiment.get_assessment()

    def get_study(self):
        return self.experiment.get_study()

    def __str__(self):
        return self.name

    def clone(self):
        self.id = None
        self.save()
        return self


reversion.register(Experiment)
reversion.register(Chemical)
reversion.register(TestSubstance)
reversion.register(Guideline)
reversion.register(AnimalGroup)
