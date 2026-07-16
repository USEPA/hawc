import json
from django.http import HttpRequest
from django.shortcuts import render

from ..assessment.models import TimeSpentEditing
from ..common.htmx import HtmxViewSet, action, can_edit, can_view
from ..common.views import (
    BaseCopyForm,
    BaseCreate,
    BaseDelete,
    BaseDetail,
    BaseUpdate,
)
from ..mgmt.views import EnsureExtractionStartedMixin
from ..study.models import Study
from . import forms, models


class ExperimentCreate(EnsureExtractionStartedMixin, BaseCreate):
    success_message = "Experiment created."
    parent_model = Study
    parent_template_name = "study"
    model = models.Experiment
    form_class = forms.ExperimentForm

    def get_success_url(self):
        super().get_success_url()
        return self.object.get_update_url()


class ExperimentUpdate(BaseUpdate):
    success_message = "Experiment updated."
    parent_model = Study
    parent_template_name = "study"
    model = models.Experiment
    form_class = forms.ExperimentForm
    template_name = "mechanistic/experiment_update.html"

    """
    def get_queryset(self):
        return super().get_queryset().complete()
    """


class ExperimentDetail(BaseDetail):
    model = models.Experiment

    """
    def get_queryset(self):
        return super().get_queryset().complete()
    """


class ExperimentDelete(BaseDelete):
    success_message = "Experiment deleted."
    model = models.Experiment

    """
    def get_queryset(self):
        return super().get_queryset().complete()
    """

    def get_success_url(self):
        return self.object.study.get_absolute_url()


class ExperimentCopyForm(BaseCopyForm):
    copy_model = models.Experiment
    form_class = forms.ExperimentSelectorForm
    model = Study


# Experiment viewset
class ExperimentViewSet(HtmxViewSet):
    actions = {"read", "update"}
    parent_model = Study
    model = models.Experiment
    form_fragment = "mechanistic/fragments/_experiment_edit.html"
    detail_fragment = "mechanistic/fragments/_experiment_table.html"

    @action(permission=can_view)
    def read(self, request: HttpRequest, *args, **kwargs):
        return render(request, self.detail_fragment, self.get_context_data())

    @action(methods=("get", "post"), permission=can_edit)
    def update(self, request: HttpRequest, *args, **kwargs):
        template = self.form_fragment
        data = request.POST if request.method == "POST" else None

        # prepopulate it with data from the Experiment...this is kind of weird. If you instantiate the form like this:
        #
        #       form = forms.ExperimentForm(data=data, instance=request.item.object)
        #
        # you don't need to set data like this; django/crispy must use the instance to prepopulate fields. But, if
        # you instantiate the form like this:
        #
        #       form = forms.ExperimentForm(data=data, instance=request.item.object, files=request.FILES)
        #
        # (which we have to do, since Experiment has a FileField for protocol), then the form will render initially
        # with no existing data filled in (i.e., the "name" field doesn't have the model.name filled in to start!
        #
        # I spent an *extremely* long time trying to figure out why and eventually settled on this as the fix. Is something
        # weird with the crispy setup? With the model/view? Is htmx confusing things? I give up, this works. -tfeiler 20260417
        if data is None:
            obj = request.item.object
            data = {
                "name": obj.name,
                "has_high_throughput": obj.has_high_throughput,
                "description": obj.description,
                "test_facility": obj.test_facility,
                "guideline": obj.guideline,
                "guideline_name_number": obj.guideline_name_number,
                "guideline_compliance": obj.guideline_compliance,
                # TestSystem-start
                "test_system_type": obj.test_system_type,
                "test_system_type_other": obj.test_system_type_other,
                "test_system_description": obj.test_system_description,
                "species": obj.species,
                "supplier": obj.supplier,
                "supplier_remarks": obj.supplier_remarks,
                "catalogue_number": obj.catalogue_number,
                "batch_number": obj.batch_number,
                "genetic_modification": obj.genetic_modification,
                "genetic_modification_remarks": obj.genetic_modification_remarks,
                "metabolic_competence": obj.metabolic_competence,
                "metabolic_competence_remarks": obj.metabolic_competence_remarks,
                "medium_buffer": obj.medium_buffer,
                "serum_supplements": obj.serum_supplements,
                "maintenance": obj.maintenance,
                "qc_confirmation": obj.qc_confirmation,
                "qc_confirmation_remarks": obj.qc_confirmation_remarks,
                "controls_used": obj.controls_used,
                # TestSystem-end
                # TestDesign-start
                "vehicle": obj.vehicle,
                "vehicle_other": obj.vehicle_other,
                "final_concentration_vehicle": obj.final_concentration_vehicle,
                "final_concentration_vehicle_other": obj.final_concentration_vehicle_other,
                "final_concentration_vehicle_units": obj.final_concentration_vehicle_units,
                "concentration_selection": obj.concentration_selection,
                "concentration_selection_remarks": obj.concentration_selection_remarks,
                "concentrations_tested": json.dumps(obj.concentrations_tested),
                # TestDesign-end
                # MechControl-start
                "control_type": obj.control_type,
                "control_type_other": obj.control_type_other,
                "control_description": obj.control_description,
                "control_remarks": obj.control_remarks,
                # MechControl-end
                # ExperimentalDesign-start
                "test_system_concentration": obj.test_system_concentration,
                "passage_number": obj.passage_number,
                "exposure_medium_composition": obj.exposure_medium_composition,
                "incubation_conditions": obj.incubation_conditions,
                "incubation_conditions": obj.incubation_conditions,
                "exposure_duration": obj.exposure_duration,
                "administration_frequency": obj.administration_frequency,
                "technical_replicates": obj.technical_replicates,
                "biological_replicates": obj.biological_replicates,
                "vessel_type": obj.vessel_type,
                "experimental_design_remarks": obj.experimental_design_remarks,
                # ExperimentalDesign-end
            }

        # useful reading:
        # https://www.reddit.com/r/django/comments/b2xn3l/requestfiles_is_empty_file_didnt_upload/
        # https://stackoverflow.com/questions/680770/django-imagefield-not-working-properly-via-modelform/681657#681657
        # https://stackoverflow.com/questions/7920128/what-is-the-difference-between-initial-data-and-bound-data-django-forms
        form = forms.ExperimentForm(data=data, instance=request.item.object, files=request.FILES)
        # form = forms.ExperimentForm(data=data, instance=request.item.object)

        if request.method == "GET":
            TimeSpentEditing.set_start_time(request)
        elif request.method == "POST" and form.is_valid():
            TimeSpentEditing.add_time_spent_job(
                request, request.item.object, request.item.assessment.id
            )
            self.perform_update(request.item, form)
            template = self.detail_fragment
        context = self.get_context_data(form=form)

        return render(request, template, context)


class ExperimentChildViewSet(HtmxViewSet):
    actions = {"create", "read", "update", "delete", "clone"}
    parent_model = models.Experiment
    model = None  # required
    form_class = None  # required
    form_fragment = "common/fragments/_object_edit_row.html"
    detail_fragment = None  # required

    @action(permission=can_view)
    def read(self, request: HttpRequest, *args, **kwargs):
        return render(request, self.detail_fragment, self.get_context_data())

    @action(methods=("get", "post"), permission=can_edit)
    def create(self, request: HttpRequest, *args, **kwargs):
        template = self.form_fragment
        if request.method == "GET":
            form = self.form_class(parent=request.item.parent)
            TimeSpentEditing.set_start_time(request)
        else:
            form = self.form_class(request.POST, parent=request.item.parent)
            if form.is_valid():
                self.perform_create(request.item, form)
                template = self.detail_fragment
                TimeSpentEditing.add_time_spent_job(
                    request, request.item.object, request.item.assessment.id
                )
        context = self.get_context_data(form=form)
        return render(request, template, context)

    @action(methods=("get", "post"), permission=can_edit)
    def update(self, request: HttpRequest, *args, **kwargs):
        template = self.form_fragment
        data = request.POST if request.method == "POST" else None
        form = self.form_class(data=data, instance=request.item.object)
        if request.method == "GET":
            TimeSpentEditing.set_start_time(request)
        elif request.method == "POST" and form.is_valid():
            self.perform_update(request.item, form)
            template = self.detail_fragment
            TimeSpentEditing.add_time_spent_job(
                request, request.item.object, request.item.assessment.id
            )
        context = self.get_context_data(form=form)
        return render(request, template, context)

    @action(methods=("get", "post"), permission=can_edit)
    def delete(self, request: HttpRequest, *args, **kwargs):
        if request.method == "POST":
            context = {"attribute": self.model.__name__.lower(), "id": request.item.object.id}
            self.perform_delete(request.item)
            return render(request, "common/fragments/_delete_rows.html", context)
        return render(request, self.detail_fragment, self.get_context_data())

    @action(methods=("post",), permission=can_edit)
    def clone(self, request: HttpRequest, *args, **kwargs):
        self.perform_clone(request.item)
        return render(request, self.detail_fragment, self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model"] = self.model.__name__.lower()
        context["app"] = "mechanistic"

        try:
            context["customTemplateScriptContext"] = self.model.get_custom_context(
                self.request.item.assessment, context["form"]
            )
        except Exception as e:
            context["customTemplateScriptContext"] = {}

        return context


class ChemicalCreate(EnsureExtractionStartedMixin, BaseCreate):
    success_message = "Chemical created."
    parent_model = Study
    parent_template_name = "study"
    model = models.Chemical
    form_class = forms.ChemicalForm

    def get_success_url(self):
        super().get_success_url()
        return self.object.get_update_url()


class ChemicalUpdate(BaseUpdate):
    success_message = "Chemical updated."
    parent_model = Study
    parent_template_name = "study"
    model = models.Chemical
    form_class = forms.ChemicalForm
    # template_name = "mechanistic/chemical_update.html"


class ChemicalDetail(BaseDetail):
    model = models.Chemical


class ChemicalDelete(BaseDelete):
    success_message = "Chemical deleted."
    model = models.Chemical

    def get_success_url(self):
        return self.object.study.get_absolute_url()


class ChemicalCopyForm(BaseCopyForm):
    copy_model = models.Chemical
    form_class = forms.ChemicalSelectorForm
    model = Study


# REMOVE NOW TAHT CHEMICALS ARE NOT AN EXPERIMENT SUBOBJ???
# Chemical viewset
"""
class ChemicalViewSet(ExperimentChildViewSet):
    model = models.Chemical
    form_class = forms.ChemicalForm
    detail_fragment = "mechanistic/fragments/chemical_row.html"
"""


class MethodViewSet(ExperimentChildViewSet):
    model = models.Method
    form_class = forms.MethodForm
    detail_fragment = "mechanistic/fragments/method_row.html"


class DataAnalysisViewSet(ExperimentChildViewSet):
    model = models.DataAnalysis
    form_class = forms.DataAnalysisForm
    detail_fragment = "mechanistic/fragments/dataanalysis_row.html"


class MechanisticEndpointViewSet(ExperimentChildViewSet):
    model = models.MechanisticEndpoint
    form_class = forms.MechanisticEndpointForm
    detail_fragment = "mechanistic/fragments/endpoint_row.html"
