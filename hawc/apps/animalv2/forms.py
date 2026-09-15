from crispy_forms import layout as cfl
from django import forms
from django.forms import ModelForm
from django.urls import reverse

from ..assessment.autocomplete import DSSToxAutocomplete
from ..common.autocomplete import AutocompleteSelectWidget, AutocompleteTextWidget
from ..common.forms import ArrayCheckboxSelectMultiple, BaseFormHelper, CopyForm
from . import autocomplete, constants, models


def set_textarea_height(fields: dict, n_rows: int = 3):
    for field in fields.values():
        if isinstance(field.widget, forms.Textarea):
            field.widget.attrs["rows"] = n_rows


"""
class StudyLevelValueForm(forms.ModelForm):
    class Meta:
        model = models.StudyLevelValue
        exclude = ("study", "created", "last_updated")
        widgets = {}

    def __init__(self, *args, **kwargs):
        study = kwargs.pop("parent", None)
        prefix = f"studylevelvalue-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if study:
            self.instance.study = study
            self.instance.assessment = study.get_assessment()

        self.fields["comments"].widget.attrs["rows"] = 3

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.layout = cfl.Layout(
            cfl.Row(
                cfl.Column("system"),
            ),
            cfl.Row(
                cfl.Column("value_type"),
                cfl.Column("value"),
                cfl.Column("units"),
            ),
            cfl.Row(
                cfl.Column("comments"),
            ),
        )
        return helper
"""


class ExperimentForm(ModelForm):
    class Meta:
        model = models.Experiment
        exclude = ("study",)
        widgets = {
            "dev_or_repro_toxicity_types": ArrayCheckboxSelectMultiple(
                choices=constants.DevelopmentalOrReproductiveToxicityType.choices
            ),
        }

    def __init__(self, *args, **kwargs):
        parent = kwargs.pop("parent", None)
        super().__init__(*args, **kwargs)
        if parent:
            self.instance.study = parent

        """
        if self.instance.study.assessment.enable_observations:
            self.fields["guideline"].required = True
            self.fields["guideline"].empty_label = None

        # change checkbox to select box
        self.fields["has_multiple_generations"].widget = forms.Select(
            choices=((True, "Yes"), (False, "No"))
        )
        """

    @property
    def helper(self):
        # by default take-up the whole row
        for fld in list(self.fields.keys()):
            widget = self.fields[fld].widget
            if type(widget) is not forms.CheckboxInput:
                widget.attrs["class"] = "form-control"

        if self.instance.id:
            inputs = {
                "legend_text": f"Update {self.instance}",
            }
            helper = BaseFormHelper(self, **inputs)
            helper.form_tag = False
        else:
            inputs = {
                "legend_text": "Create new experiment",
                "help_text": """
                    Create a new experiment. Each experiment is a associated with a
                    study, and may have one or more collections of animals. For
                    example, one experiment may be a 2-year cancer bioassay,
                    while another multi-generational study. It is possible to
                    create multiple separate experiments within a single study,
                    with different study-designs, durations, or test-species.""",
                "cancel_url": self.instance.study.get_absolute_url(),
            }
            helper = BaseFormHelper(self, **inputs)

        helper.form_id = "aniv2-experiment-form"
        helper.add_row("experiment_type", 2, "col-md-6")
        # helper.add_row("route_of_administration", 2, "col-md-6")
        # helper.add_row("guideline_name", 3, "col-md-4")
        # set_textarea_height(self.fields)

        return helper


class ChemicalForm(forms.ModelForm):
    class Meta:
        model = models.Chemical
        exclude = ("study",)
        widgets = {
            "name": AutocompleteTextWidget(
                autocomplete_class=autocomplete.ChemicalAutocomplete, field="name"
            ),
            "dtxsid": AutocompleteSelectWidget(autocomplete_class=DSSToxAutocomplete),
        }

    def __init__(self, *args, **kwargs):
        """
        experiment = kwargs.pop("parent", None)
        instance_ref = kwargs.get("instance")
        prefix = f"chemical-{instance_ref.pk if instance_ref is not None else 'new'}"
        if "instance" in kwargs:
            del kwargs["instance"]
        print(f"{kwargs=}")
        print(f"loaded '{prefix}' FROM {instance_ref}")
        # prefix = f"chemical-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if experiment:
            self.instance.experiment = experiment
        """
        study = kwargs.pop("parent", None)
        super().__init__(*args, **kwargs)
        if study:
            self.instance.study = study

    @property
    def helper(self):
        inputs = {
            "legend_text": ("Add" if not self.instance.id else "Update") + " Chemical",
            "cancel_url": self.instance.study.get_absolute_url(),
            "submit_text": "Save",
        }
        helper = BaseFormHelper(self, **inputs)
        # helper.form_tag = False
        helper.form_id = "form-mech-chemical"
        # helper.add_row("name", 3, "col-md-4")
        # helper.add_row("source", 3, "col-md-4")
        # helper.add_row("cas", 3, "col-md-4")
        # helper.add_row("composition_purity", 2, "col-md-6")
        # helper.add_row("percent_purity", 3, "col-md-4")
        # helper.add_row("stability", 2, "col-md-6")
        # helper.add_row("solubility", 2, "col-md-6")
        # helper.add_create_btn("dtxsid", reverse("assessment:dtxsid_create"), "Add new DTXSID")
        set_textarea_height(self.fields)
        return helper


class ChemicalSelectorForm(CopyForm):
    legend_text = "Copy chemical"
    help_text = "Select an existing chemical as a template to create a new one."
    create_url_pattern = "animalv2:chemical_create"
    selector = forms.ModelChoiceField(
        queryset=models.Chemical.objects.all(), empty_label=None, label="Select template"
    )

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.fields["selector"].queryset = self.fields["selector"].queryset.filter(
            study=self.parent
        )


class TestSubstanceForm(forms.ModelForm):
    class Meta:
        model = models.TestSubstance
        exclude = ("experiment",)
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        experiment = kwargs.pop("parent", None)
        prefix = f"testsubstance-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if experiment:
            self.instance.experiment = experiment

        self.fields["chemical"].queryset = self.instance.experiment.study.aniv2_chemicals.all()

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.add_row("chemical", 2, "col-md-6")
        helper.add_row("composition", 2, "col-md-6")
        helper.add_row("purity", 2, "col-md-6")
        helper.add_row("expiration_date", 2, "col-md-6")

        return helper


class GuidelineForm(forms.ModelForm):
    class Meta:
        model = models.Guideline
        exclude = ("experiment",)

    def __init__(self, *args, **kwargs):
        experiment = kwargs.pop("parent", None)
        prefix = f"guideline-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if experiment:
            self.instance.experiment = experiment

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.add_row("number", 2, "col-md-6")

        return helper


class AnimalGroupForm(forms.ModelForm):
    class Meta:
        model = models.AnimalGroup
        exclude = ("experiment",)

    def __init__(self, *args, **kwargs):
        experiment = kwargs.pop("parent", None)
        prefix = f"animalgroup-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if experiment:
            self.instance.experiment = experiment

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.add_row("generation", 2, "col-md-6")
        helper.add_row("cohort_type", 2, "col-md-6")
        helper.add_row("source", 2, "col-md-6")
        helper.add_row("sex", 3, "col-md-4")

        return helper


class HusbandryForm(forms.ModelForm):
    class Meta:
        model = models.Husbandry
        exclude = ("experiment",)

    def __init__(self, *args, **kwargs):
        experiment = kwargs.pop("parent", None)
        prefix = f"husbandry-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if experiment:
            self.instance.experiment = experiment

        self.fields["animal_group"].queryset = self.instance.experiment.aniv2_animalgroups.all()

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.add_row("animal_group", 2, "col-md-6")
        helper.add_row("animal_randomization", 2, "col-md-6")
        helper.add_row("cage_material", 2, "col-md-6")
        helper.add_row("bedding_material", 2, "col-md-6")
        helper.add_row("enrichment_material", 2, "col-md-6")
        helper.add_row("water_bottle_material", 2, "col-md-6")
        helper.add_row("animal_identification", 2, "col-md-6")
        helper.add_row("water", 2, "col-md-6")

        return helper


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = models.Treatment
        exclude = ("experiment",)

    def __init__(self, *args, **kwargs):
        experiment = kwargs.pop("parent", None)
        prefix = f"treatment-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if experiment:
            self.instance.experiment = experiment

        self.fields["test_substance"].queryset = self.instance.experiment.testsubstances.all()

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.add_row("route_of_exposure", 2, "col-md-6")
        helper.add_row("exposure_method", 2, "col-md-6")
        helper.add_row("age_start", 2, "col-md-6")
        helper.add_row("age_end", 2, "col-md-6")
        helper.add_row("verification", 3, "col-md-4")

        return helper


"""
class AnimalGroupForm(forms.ModelForm):
    class Meta:
        model = models.AnimalGroup
        exclude = ("experiment",)

    def __init__(self, *args, **kwargs):
        experiment = kwargs.pop("parent", None)
        prefix = f"animalgroup-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if experiment:
            self.instance.experiment = experiment

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.add_row("species", 3, "col-md-4")
        helper.add_row("lifestage_at_exposure", 2, "col-md-6")
        helper.add_row("generation", 2, "col-md-6")
        helper.add_row("husbandry_and_diet", 2, "col-md-6")
        set_textarea_height(self.fields)

        assessment_id = self.instance.experiment.study.assessment.pk
        helper.add_create_btn(
            "species",
            reverse("assessment:species_create", args=(assessment_id,)),
            "Create species",
        )
        helper.add_create_btn(
            "strain",
            reverse("assessment:strain_create", args=(assessment_id,)),
            "Create strain",
        )
        return helper

    def clean(self):
        cleaned_data = super().clean()
        if "species" in cleaned_data and "strain" in cleaned_data:
            species_obj = cleaned_data["species"]
            strain_obj = cleaned_data["strain"]
            if species_obj.id != strain_obj.species.id:
                raise forms.ValidationError(
                    {"strain": "Strain must be of the same species as the selected species"}
                )
        return cleaned_data


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = models.Treatment
        exclude = ("experiment",)

    def __init__(self, *args, **kwargs):
        experiment = kwargs.pop("parent", None)
        prefix = f"treatment-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if experiment:
            self.instance.experiment = experiment
        self.fields["chemical"].queryset = self.instance.experiment.v2_chemicals.all()

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.add_row("name", 3, "col-md-4")
        helper.add_row("exposure_duration", 3, "col-md-4")
        set_textarea_height(self.fields)

        return helper


class DoseGroupForm(forms.ModelForm):
    formset_parent_key = "treatment_id"

    class Meta:
        model = models.DoseGroup
        exclude = ("treatment",)

    def __init__(self, *args, **kwargs):
        treatment = kwargs.pop("parent", None)
        super().__init__(*args, **kwargs)
        if treatment:
            self.instance.treatment = treatment


class EndpointForm(forms.ModelForm):
    class Meta:
        model = models.Endpoint
        # TODO - for now, we've got EHV fields for controlled vocab in the model, but we'll hide them from UI
        exclude = (
            "experiment",
            "name_term",
            "system_term",
            "organ_term",
            "effect_term",
            "effect_subtype_term",
        )

    def __init__(self, *args, **kwargs):
        experiment = kwargs.pop("parent", None)
        prefix = f"endpoint-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if experiment:
            self.instance.experiment = experiment
        # TODO - if/when we add EHV terms back in, we'll need this kind of filtering...
        # self.fields["name_term"].queryset = Term.objects.filter(type=VocabularyTermType.endpoint_name)
        # self.fields["system_term"].queryset = Term.objects.filter(type=VocabularyTermType.system)
        # self.fields["organ_term"].queryset = Term.objects.filter(type=VocabularyTermType.organ)
        # self.fields["effect_term"].queryset = Term.objects.filter(type=VocabularyTermType.effect)
        # self.fields["effect_subtype_term"].queryset = Term.objects.filter(type=VocabularyTermType.effect_subtype)

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.add_row("system", 4, "col-md-3")
        helper.add_row("effect_modifier_timing", 4, "col-md-3")
        helper.add_row("additional_tags", 2, "col-md-6")
        set_textarea_height(self.fields)

        return helper


class ObservationTimeForm(forms.ModelForm):
    class Meta:
        model = models.ObservationTime
        exclude = ()

    def __init__(self, *args, **kwargs):
        experiment = kwargs.pop("parent", None)
        prefix = f"observationtime-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        # TODO - right now with name/name_term, the associated dropdown for picking an endpoint shows
        # an empty string for endpoints with a name_term but no freetext name.
        #
        # if we go back to using EHV name_term etc., we need to address this.
        #
        # but also, maybe the ObservationTime UI should be more like the Treatment/DoseGroup formset
        # style, as opposed to separate entry as in the mockup? If we do it that way, then we don't
        # need a UI widget for picking the endpoint at all, b/c it's implicit in the nested structure.
        #
        # in short, right now it's a minor issue, but not worth fixing til we make some other decisions.
        if self.instance.id:
            # editing an existing timepoint
            self.fields["endpoint"].queryset = self.instance.endpoint.experiment.v2_endpoints.all()
        else:
            # creating a new one
            self.fields["endpoint"].queryset = experiment.v2_endpoints.all()

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.add_row("observation_time", 3, "col-md-4")
        set_textarea_height(self.fields)

        return helper


class DataExtractionForm(forms.ModelForm):
    class Meta:
        model = models.DataExtraction
        exclude = ("experiment",)

    def __init__(self, *args, **kwargs):
        experiment = kwargs.pop("parent", None)
        prefix = f"dataextraction-{kwargs.get('instance').pk if 'instance' in kwargs else 'new'}"
        super().__init__(*args, prefix=prefix, **kwargs)
        if experiment:
            self.instance.experiment = experiment
        self.fields["endpoint"].queryset = self.instance.experiment.v2_endpoints.all()
        self.fields["treatment"].queryset = self.instance.experiment.v2_treatments.all()
        self.fields["observation_timepoint"].queryset = models.ObservationTime.objects.filter(
            endpoint__in=self.instance.experiment.v2_endpoints.all()
        )

    @property
    def helper(self):
        helper = BaseFormHelper(self)
        helper.form_tag = False
        helper.add_row("endpoint", 3, "col-md-4")
        helper.add_row("data_location", 3, "col-md-4")
        helper.add_row("statistical_method", 2, "col-md-6")
        helper.add_row("method_to_control_for_litter_effects", 3, "col-md-4")
        set_textarea_height(self.fields)

        return helper

    def is_valid(self):
        if "is_qualitative_only" in self.data and self.data["is_qualitative_only"] == "on":
            # TODO - if "is qualitative only" is checked, we are hiding other fields...
            # so relax the required'ness of some...
            for usually_required_field in ["dose_response_observations", "result_details"]:
                self.fields[usually_required_field].required = False

            # and in clean we'll set some defaults on those hidden fields.

        return super().is_valid()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("is_qualitative_only") is True:
            # TODO - set sensible values on the hidden fields
            hidden_defaults = {
                "data_location": "",
                "dataset_type": "",
                "variance_type": constants.VarianceType.NA,
                "statistical_method": "",
                "statistical_power": "",
                "method_to_control_for_litter_effects": constants.MethodToControlForLitterEffects.NA,
                "values_estimated": False,
                "response_units": "",
                "dose_response_observations": "",
                "result_details": "",
            }

            for field_name in hidden_defaults:
                cleaned_data[field_name] = hidden_defaults[field_name]

        return cleaned_data


class DoseResponseGroupLevelDataForm(forms.ModelForm):
    formset_parent_key = "data_extraction_id"

    class Meta:
        model = models.DoseResponseGroupLevelData
        exclude = ("data_extraction",)

    def __init__(self, *args, **kwargs):
        data_extraction = kwargs.pop("parent", None)
        super().__init__(*args, **kwargs)
        if data_extraction:
            self.instance.data_extraction = data_extraction


class DoseResponseAnimalLevelDataForm(forms.ModelForm):
    formset_parent_key = "data_extraction_id"

    class Meta:
        model = models.DoseResponseAnimalLevelData
        exclude = ("data_extraction",)

    def __init__(self, *args, **kwargs):
        data_extraction = kwargs.pop("parent", None)
        super().__init__(*args, **kwargs)
        if data_extraction:
            self.instance.data_extraction = data_extraction
"""
