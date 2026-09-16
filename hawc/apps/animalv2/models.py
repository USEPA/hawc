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

# TODO - related_name is currently a mishmash of plain names (e.g. 'testsubstances') and model-name-convention where there were conflicts with aniv2 (e.g. 'aniv2_dosegroups'). Let's take a pass and do EVRYTHING as aniv2_xxx; means redoing migrations (which we should likely do anyway), but also updating the templates in particular, and probabyl some python code. Do it at the end but let's start using aniv2 going forward...


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

    # TODO - could we make a generic version of this available via mixin that uses naming convention + introspection to work? I have played with this some but can't seemt o get it to work; not sure making manual ones like this is worthwhile...possibly a model could create/register such methods on the fly somehow?
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


class Husbandry(models.Model):
    objects = managers.HusbandryManager()

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name="husbandries")

    animal_group = models.ForeignKey(
        AnimalGroup, on_delete=models.CASCADE, related_name="husbandries"
    )

    number_per_cage = models.CharField(
        max_length=255,
        help_text="Provide the number of animals per cage.",
        verbose_name="Number of Animals per Cage",
    )

    animal_randomization = models.CharField(
        max_length=3,
        choices=constants.HusbandryRandomization.choices,
        help_text="Select whether a randomization method was used to assign animals to cages. If yes, include a description of animal randomization method. If not available from picklist, select 'other' and specify",
    )

    animal_randomization_remarks = models.CharField(max_length=255, blank=True)

    cage_material = models.CharField(
        max_length=3,
        choices=constants.HusbandryCageMaterial.choices,
        help_text="Select animal cage material. If not available from picklist, select 'other' and specify.",
    )

    cage_material_remarks = models.CharField(max_length=255, blank=True)

    bedding_material = models.CharField(
        max_length=3,
        choices=constants.HusbandryBeddingMaterial.choices,
        help_text="Select the animal bedding material. If not available from picklist, select 'other' and specify.",
    )

    bedding_material_remarks = models.CharField(max_length=255, blank=True)

    enrichment_material = models.CharField(
        max_length=3,
        choices=constants.HusbandryEnrichmentMaterial.choices,
        help_text="Select the type of enrichment provided for animals. If none apply, select “other” and describe the test material. If not available from picklist, select 'other' and specify.",
    )

    enrichment_material_remarks = models.CharField(max_length=255, blank=True)

    water_bottle_material = models.CharField(
        max_length=3,
        choices=constants.HusbandryWaterBottleMaterial.choices,
        help_text="Select the water bottle material. If not available from picklist, select 'other' and specify.",
    )

    water_bottle_material_remarks = models.CharField(max_length=255, blank=True)

    animal_identification = models.CharField(
        max_length=3,
        choices=constants.HusbandryIdentification.choices,
        help_text="Select the animal identification method. If not available from picklist, select 'other' and specify.",
    )

    animal_identification_remarks = models.CharField(max_length=255, blank=True)

    ambient_temperature = models.CharField(
        max_length=255,
        help_text="Describe the animal husbandry temperature.",
        verbose_name="Ambient Temperature (°C)",
    )

    humidity_percentage = models.CharField(
        max_length=255,
        help_text="Describe the animal husbandry humidity in %",
        verbose_name="Humidity (%)",
    )

    photo_period = models.CharField(
        max_length=255,
        help_text="Describe the photoperiod as hours dark / hours light.",
        verbose_name="Photoperiod (hrs dark / hrs light)",
    )

    feeding_frequency = models.CharField(
        max_length=3,
        choices=constants.HusbandryFeedingFrequency.choices,
        help_text="Select the feeding frequency and provide additional details in the “Animal Feeding and Diet Remarks” field.",
    )

    diet = models.CharField(
        max_length=3,
        choices=constants.HusbandryDiet.choices,
        help_text="Select the type of diet (e.g. conventional laboratory diet / caloric restriction), whether it was provided ad libitum, restricted, etc. ",
    )

    feeding_and_diet_remarks = models.TextField(
        max_length=32768,
        help_text="Describe the animal feeding protocol. For fasting, describe the fasting protocol (e.g. animals were fasted 4 hours prior to sacrifice).",
    )

    water = models.CharField(
        max_length=3,
        choices=constants.HusbandryWater.choices,
        help_text="Describe type (e.g. drinking water, tap distilled), and whether it was provided ad libitum. If not available from picklist, select 'other' and specify.",
    )

    water_remarks = models.CharField(max_length=255, blank=True)

    food_and_water_quality = models.TextField(
        max_length=2500,
        help_text="Provide analytical information (if available) on the nutrient and dietary contaminant levels. Similarly provide analytical information on the drinking water used in the study.",
    )

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)

    def get_assessment(self):
        return self.experiment.get_assessment()

    def get_study(self):
        return self.experiment.get_study()

    def clone(self):
        self.id = None
        self.save()
        return self


class Treatment(models.Model):
    objects = managers.TreatmentManager()

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name="treatments")

    test_substance = models.ForeignKey(
        TestSubstance, on_delete=models.CASCADE, related_name="treatments"
    )

    route_of_exposure = models.CharField(
        max_length=3,
        choices=constants.TreatmentRouteOfExposure.choices,
        help_text="Select the route of administration as appropriate. If not available from the picklist, select 'other' and specify.",
    )

    route_of_exposure_remarks = models.CharField(
        max_length=250,
        blank=True,
        help_text="If “other” was selected in the “Route of exposure” field, specify.",
    )

    exposure_method = models.CharField(
        max_length=5,
        choices=constants.TreatmentExposureMethod.choices,
        help_text="Specific description of how substance was given to test subjects via the administration route.",
    )

    exposure_method_remarks = models.CharField(
        max_length=250,
        blank=True,
        help_text="If “other” was selected in the “Route of exposure” field, specify.",
    )

    lifestage_start = models.CharField(
        max_length=3,
        verbose_name="Animal Lifestage at the Start of Exposure",
        choices=constants.TreatmentLifestage.choices,
        help_text="Embryonic Stage:<br>Description: The initial stage of development within the egg or womb, where the organism begins to form and differentiate.<br>Characteristics: Rapid cell division and formation of basic body structures.<p>Fetal:<br>Later stage of development within the eff or womb characterized by continued growth, differentiation, and maturation of organs and tissues. <br> Characteristics: The organism has an established body-plan and recognizable anatomical features but remains dependent on the maternal environment for development. <p> Neonatal Stage:<br>Description: The period immediately after birth or hatching.<br> Characteristics: Animals are usually highly dependent on parental care and nourishment.<p> Juvenile Stage:<br>Description: The phase following the neonatal stage, where the animal grows and develops but is not yet sexually mature.<br>Characteristics: Increased independence, rapid growth, and learning survival skills.<p>Adolescent Stage:<br>Description: The transition phase between juvenile and adult stages, marked by the onset of puberty.<br>Characteristics: Development of secondary sexual characteristics and increased social interactions.<p>Adult Stage:<br>Description: The stage where the animal is fully grown and sexually mature.<br>Characteristics: Reproductive capability and establishment of social hierarchies or territories.<p>Senior Stage:<br>Description: The later stage of life where the animal experiences aging and a decline in physical capabilities.<br>Characteristics: Reduced reproductive capability and increased susceptibility to disease.",
    )

    age_start = models.CharField(
        max_length=255,
        help_text="Record the age of animals at the start of test item administration.",
        verbose_name="Animal Age at Start of Exposure",
    )

    age_start_unit = models.CharField(
        max_length=3,
        choices=constants.TreatmentAgeUnit.choices,
        verbose_name="Animal Age at Start Unit",
        help_text="Record the animal age unit of measure.",
    )

    age_end = models.CharField(
        max_length=255,
        help_text="Record the age of animals at the start of test item administration.",
        verbose_name="Animal Age at End of Exposure",
    )

    age_end_unit = models.CharField(
        max_length=3,
        choices=constants.TreatmentAgeUnit.choices,
        verbose_name="Animal Age at End Unit",
        help_text="Record the animal age unit of measure.",
    )

    verification = models.CharField(
        max_length=3,
        choices=constants.YesNoNs.choices,
        verbose_name="Analytical Verification of Doses or Concentrations",
        help_text="Were concentrations/doses analytically verified in the experiment?",
    )

    exposure_duration = models.CharField(
        max_length=255,
        help_text="Indicate duration in days, weeks or months, e.g. '104 weeks' or '90 days'.",
    )

    frequency_of_treatment = models.CharField(
        max_length=255,
        help_text="Indicate the frequency of the administration of doses to the test animals (e.g., 'daily, 7 days each week'). Use of non-standard dosing regimen (e.g. a five-day per week regime) should be justified.",
    )

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)

    def get_assessment(self):
        return self.experiment.get_assessment()

    def get_study(self):
        return self.experiment.get_study()

    def clone(self):
        self.id = None
        self.save()
        return self


class DoseGroup(models.Model):
    objects = managers.DoseGroupManager()

    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="aniv2_dosegroups"
    )

    treatment = models.ForeignKey(
        Treatment, on_delete=models.CASCADE, related_name="aniv2_dosegroups"
    )

    animal_group = models.ForeignKey(
        AnimalGroup, on_delete=models.CASCADE, related_name="aniv2_dosegroups"
    )

    dose_group_type = models.CharField(
        max_length=3,
        choices=constants.DoseGroupType.choices,
        help_text="Select the role of the dose group within the experiment.",
    )

    dose_group_type_remarks = models.CharField(
        max_length=250,
        blank=True,
        help_text="If “other” was selected in the “Dose Group Type” field, specify.",
    )

    # # of dose groups -- this is derived and let's put it on the treatment field maybe?

    dose_value = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Numerical concentration value of a test chemical. If a study changes dosing over time (e.g., gradually increased over a few weeks, decreased due to palatability or toxicity), enter final concentrations. You do not need to calculate the average. In unusual cases, not all doses will be converted from ppm to mg/kg/day. Enter the mixed dosing units (do not attempt conversion), unless only one dose is converted. If only one dose is converted (often the critical effect dose) then put the conversion(s) in the comments and keep all doses as ppm.",
    )

    dose_units = models.CharField(
        max_length=5,
        choices=constants.DoseGroupUnit.choices,
        help_text="Unit associated with a concentration of a test chemical. Preferred unit is milligrams per kilogram per day (mg/kg/day) if reported. If the mg/kg/day is not reported based on ppm or other units, do not attempt to estimate the mg/kg/day dose.",
    )

    dose_units_remarks = models.CharField(
        max_length=250,
        blank=True,
        help_text="If “other” was selected in the “Dose Units” field, specify.",
    )

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)

    def get_assessment(self):
        return self.experiment.get_assessment()

    def get_study(self):
        return self.experiment.get_study()

    def get_value_including_units(self):
        return f"{self.dose_value} {self.get_dose_units_display()}"

    def clone(self):
        self.id = None
        self.save()
        return self


class DosePreparation(models.Model):
    objects = managers.DosePreparationManager()

    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="aniv2_dosepreparations"
    )

    dose_group = models.ForeignKey(
        DoseGroup, on_delete=models.CASCADE, related_name="aniv2_dosepreparations"
    )

    vehicle = models.CharField(
        max_length=5,
        choices=constants.DosePreparationVehicle.choices,
        help_text="The media used in administration of the chemical. Select the vehicle used. If not available from picklist, select 'other' and specify. Further information can be given in the supplementary remarks field.<p>Note that some of the vehicles provided in this list are used for specific routes of administration only.",
    )

    vehicle_remarks = models.CharField(
        max_length=250,
        blank=True,
        help_text="If “other” was selected in the “Vehicle” field, specify.",
    )

    concentration = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Enter numerical value of all doses tested (numerical value only, e.g. 1, 3, 30, etc.)",
    )

    unit = models.CharField(
        max_length=5,
        choices=constants.DosePreparationUnit.choices,
        help_text="Enter the numerical value and concentration units from the picklist. If “other” is selected, indicate the units in the “Unit Remarks” field.",
    )

    unit_remarks = models.CharField(
        max_length=250,
        blank=True,
        help_text="If “other” was selected in the “Unit” field, specify.",
    )

    formulation_type = models.CharField(
        max_length=3,
        choices=constants.DosePreparationFormulation.choices,
        help_text="Select the appropriate information about formulation type of the test substance under storage conditions and under assay conditions.",
    )

    formulation_type_remarks = models.CharField(
        max_length=250,
        blank=True,
        help_text="If “other” was selected in the “Formulation Type” field, specify.",
    )

    stability = models.CharField(
        max_length=3,
        choices=constants.DosePreparationStability.choices,
        verbose_name="Stability in Vehicle",
        help_text="Select the appropriate information about stability of the chemical under storage conditions and under assay conditions.<p>In case this was not assessed or reported, select ‘unknown’",
    )

    solubility = models.CharField(
        max_length=3,
        choices=constants.DosePreparationSolubility.choices,
        verbose_name="Solubility in Vehicle",
        help_text="It should be confirmed that the highest concentration tested was soluble, in case not, a justification should be provided.<p>Specify the highest soluble concentration observed. If the highest tested concentration was insoluble, provide a justification for why insoluble concentrations were tested in the “Solubility Remarks” field. the appropriate information about stability of the chemical under storage conditions and under assay conditions.<p>In case this was not assessed or reported, select ‘unknown’",
    )

    solubility_remarks = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Solubility in Vehicle Remarks",
        help_text="If “The highest tested concentration was insoluble, specify” was selected in the “Solubility in Vehicle” field, specify.",
    )

    homogeneity = models.CharField(
        max_length=3,
        choices=constants.DosePreparationHomogeneity.choices,
        help_text="Select the appropriate information about homogeneity under dose preparation conditions. Provide details in the remarks field.",
    )

    analytical_verification = models.CharField(
        max_length=3,
        choices=constants.DosePreparationAnalyticalVerification.choices,
        help_text="Select the appropriate information about analytical verification under dose preparation conditions. Provide details in the remarks field for the analytical method used.",
    )

    analytical_verification_remarks = models.CharField(
        max_length=250,
        blank=True,
        help_text="Provide details for the analytical method used.",
    )

    preparation_frequency = models.CharField(
        max_length=3,
        choices=constants.DosePreparationFrequency.choices,
        help_text="Select the appropriate information about preparation frequency under dose preparation conditions. Provide details in the remarks field.",
    )

    preparation_frequency_remarks = models.CharField(
        max_length=250,
        blank=True,
        help_text="If “Other” was selected in the “Preparation Frequency” field, specify the preparation frequency.",
    )

    preparation_method = models.CharField(
        max_length=3,
        choices=constants.DosePreparationMethod.choices,
        help_text="Select the appropriate information about preparation method under dose preparation conditions. Provide details in the remarks field.",
    )

    preparation_method_remarks = models.CharField(
        max_length=250,
        blank=True,
        help_text="If “Other” was selected in the “Preparation Method” field, specify the preparation frequency.",
    )

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)

    def get_assessment(self):
        return self.experiment.get_assessment()

    def get_study(self):
        return self.experiment.get_study()

    def clone(self):
        self.id = None
        self.save()
        return self


reversion.register(Experiment)
reversion.register(Chemical)
reversion.register(TestSubstance)
reversion.register(Guideline)
reversion.register(AnimalGroup)
reversion.register(Husbandry)
reversion.register(Treatment)
reversion.register(DoseGroup)
reversion.register(DosePreparation)
