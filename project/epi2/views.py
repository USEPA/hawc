from django.core.urlresolvers import reverse

from utils.views import (BaseDetail, BaseDelete,
                         BaseVersion, BaseUpdate, BaseCreate,
                         BaseCreateWithFormset, BaseUpdateWithFormset,
                         CloseIfSuccessMixin, BaseList, GenerateReport)

from assessment.models import Assessment
from study.models import Study
from study.views import StudyRead

from . import forms, exports, models


# Study criteria
class StudyCriteriaCreate(CloseIfSuccessMixin, BaseCreate):
    success_message = 'Criteria created.'
    parent_model = Assessment
    parent_template_name = 'assessment'
    model = models.Criteria
    form_class = forms.CriteriaForm


# Study population
class StudyPopulationCreate(BaseCreate):
    success_message = 'Study-population created.'
    parent_model = Study
    parent_template_name = 'study'
    model = models.StudyPopulation
    form_class = forms.StudyPopulationForm


class StudyPopulationCopyAsNewSelector(StudyRead):
    template_name = 'epi2/studypopulation_copy_selector.html'

    def get_context_data(self, **kwargs):
        context = super(StudyPopulationCopyAsNewSelector, self).get_context_data(**kwargs)
        context['form'] = forms.StudyPopulationSelectorForm(parent_id=self.object.id)
        return context


class StudyPopulationDetail(BaseDetail):
    model = models.StudyPopulation


class StudyPopulationUpdate(BaseUpdate):
    success_message = "Study Population updated."
    model = models.StudyPopulation
    form_class = forms.StudyPopulationForm


class StudyPopulationDelete(BaseDelete):
    success_message = "Study Population deleted."
    model = models.StudyPopulation

    def get_success_url(self):
        self.parent = self.object.study
        return reverse("study:detail", kwargs={"pk": self.parent.pk})


# Factors
class AdjustmentFactorCreate(CloseIfSuccessMixin, BaseCreate):
    success_message = 'Adjustment factor created.'
    parent_model = Assessment
    parent_template_name = 'assessment'
    model = models.AdjustmentFactor
    form_class = forms.AdjustmentFactorForm


# Exposure
class ExposureCreate(BaseCreate):
    success_message = 'Exposure created.'
    parent_model = models.StudyPopulation
    parent_template_name = 'study_population'
    model = models.Exposure2
    form_class = forms.ExposureForm


class ExposureCopyAsNewSelector(StudyPopulationDetail):
    template_name = 'epi2/exposure_copy_selector.html'

    def get_context_data(self, **kwargs):
        context = super(ExposureCopyAsNewSelector, self).get_context_data(**kwargs)
        context['form'] = forms.ExposureSelectorForm(parent_id=self.object.id)
        return context


class ExposureDetail(BaseDetail):
    model = models.Exposure2


class ExposureUpdate(BaseUpdate):
    success_message = "Study Population updated."
    model = models.Exposure2
    form_class = forms.ExposureForm


class ExposureDelete(BaseDelete):
    success_message = "Study Population deleted."
    model = models.Exposure2

    def get_success_url(self):
        return self.object.study_population.get_absolute_url()


# Outcome
class OutcomeList(BaseList):
    parent_model = Assessment
    model = models.Outcome

    def get_paginate_by(self, qs):
        val = 25
        try:
            val = int(self.request.GET.get('paginate_by', val))
        except ValueError:
            pass
        return val

    def get_queryset(self):
        filters = {"assessment": self.assessment}
        perms = self.get_obj_perms()
        if not perms['edit']:
            filters["study_population__study__published"] = True
        return self.model.objects.filter(**filters).order_by('name')


class OutcomeExport(OutcomeList):
    """
    Full XLS data export for the epidemiology outcome.
    """
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        exporter = exports.OutcomeComplete(
                self.object_list,
                export_format="excel",
                filename='{}-epi'.format(self.assessment),
                sheet_name='epi')
        return exporter.build_response()


class OutcomeCreate(BaseCreate):
    success_message = 'Outcome created.'
    parent_model = models.StudyPopulation
    parent_template_name = 'study_population'
    model = models.Outcome
    form_class = forms.OutcomeForm

    def get_form_kwargs(self):
        kwargs = super(OutcomeCreate, self).get_form_kwargs()
        kwargs['assessment'] = self.assessment
        return kwargs


class OutcomeCopyAsNewSelector(StudyPopulationDetail):
    template_name = 'epi2/outcome_copy_selector.html'

    def get_context_data(self, **kwargs):
        context = super(OutcomeCopyAsNewSelector, self).get_context_data(**kwargs)
        context['form'] = forms.OutcomeSelectorForm(parent_id=self.object.id)
        return context


class OutcomeDetail(BaseDetail):
    model = models.Outcome


class OutcomeUpdate(BaseUpdate):
    success_message = "Outcome updated."
    model = models.Outcome
    form_class = forms.OutcomeForm


class OutcomeDelete(BaseDelete):
    success_message = "Outcome deleted."
    model = models.Outcome

    def get_success_url(self):
        return self.object.study_population.get_absolute_url()


# Result
class ResultCreate(BaseCreateWithFormset):
    success_message = 'Result created.'
    parent_model = models.Outcome
    parent_template_name = 'outcome'
    model = models.Result
    form_class = forms.ResultForm
    formset_factory = forms.GroupResultFormset

    def post_object_save(self, form, formset):
        for form in formset.forms:
            form.instance.measurement = self.object

    def get_formset_kwargs(self):
        return {
            "outcome": self.parent,
            "study_population": self.parent.study_population
        }

    def build_initial_formset_factory(self):
        return forms.BlankGroupResultFormset(
            queryset=models.Group.objects.none(),
            **self.get_formset_kwargs())


class ResultCopyAsNewSelector(OutcomeDetail):
    template_name = 'epi2/result_copy_selector.html'

    def get_context_data(self, **kwargs):
        context = super(ResultCopyAsNewSelector, self).get_context_data(**kwargs)
        context['form'] = forms.ResultSelectorForm(parent_id=self.object.id)
        return context


class ResultDetail(BaseDetail):
    model = models.Result


class ResultUpdate(BaseUpdateWithFormset):
    success_message = "Result updated."
    model = models.Result
    form_class = forms.ResultUpdateForm
    formset_factory = forms.GroupResultFormset

    def build_initial_formset_factory(self):
        return forms.GroupResultFormset(
            queryset=self.object.results.all(),
            **self.get_formset_kwargs())

    def get_formset_kwargs(self):
        return {
            "study_population": self.object.outcome.study_population,
            "outcome": self.object.outcome,
            "result": self.object
        }

    def post_object_save(self, form, formset):
        # delete other results not associated with the selected collection
        models.GroupResult.objects\
            .filter(measurement=self.object)\
            .exclude(group__collection=self.object.groups)\
            .delete()


class ResultDelete(BaseDelete):
    success_message = "Result deleted."
    model = models.Result

    def get_success_url(self):
        return self.object.outcome.get_absolute_url()


# Group collection + group
class ComparisonGroupsCreate(BaseCreateWithFormset):
    success_message = 'Groups created.'
    parent_model = models.StudyPopulation
    parent_template_name = 'study_population'
    model = models.ComparisonGroups
    form_class = forms.ComparisonGroups
    formset_factory = forms.GroupFormset

    def post_object_save(self, form, formset):
        group_id = 0
        for form in formset.forms:
            form.instance.collection = self.object
            if form.is_valid() and form not in formset.deleted_forms:
                form.instance.group_id = group_id
                if form.has_changed() is False:
                    # ensure new group_id saved to db
                    form.instance.save()
                group_id += 1

    def build_initial_formset_factory(self):
        return forms.BlankGroupFormset(
            queryset=models.Group.objects.none())


class ComparisonGroupsOutcomeCreate(ComparisonGroupsCreate):
    parent_model = models.Outcome
    parent_template_name = 'outcome'


class ComparisonGroupsStudyPopCopySelector(StudyPopulationDetail):
    template_name = 'epi2/comparisongroups_sp_copy_selector.html'

    def get_context_data(self, **kwargs):
        context = super(ComparisonGroupsStudyPopCopySelector, self).get_context_data(**kwargs)
        context['form'] = forms.ComparisonGroupsByStudyPopulationSelectorForm(parent_id=self.object.id)
        return context


class ComparisonGroupsOutcomeCopySelector(OutcomeDetail):
    template_name = 'epi2/comparisongroups_outcome_copy_selector.html'

    def get_context_data(self, **kwargs):
        context = super(ComparisonGroupsOutcomeCopySelector, self).get_context_data(**kwargs)
        context['form'] = forms.ComparisonGroupsByOutcomeSelectorForm(parent_id=self.object.id)
        return context


class ComparisonGroupsDetail(BaseDetail):
    model = models.ComparisonGroups


class ComparisonGroupsUpdate(BaseUpdateWithFormset):
    success_message = "Groups updated."
    model = models.ComparisonGroups
    form_class = forms.ComparisonGroups
    formset_factory = forms.GroupFormset

    def build_initial_formset_factory(self):
        return forms.GroupFormset(queryset=self.object.groups.all()
                                            .order_by('group_id'))

    def post_object_save(self, form, formset):
        group_id = 0
        for form in formset.forms:
            form.instance.collection = self.object
            if form.is_valid() and form not in formset.deleted_forms:
                form.instance.group_id = group_id
                if form.has_changed() is False:
                    # ensure new group_id saved to db
                    form.instance.save()
                group_id += 1


class ComparisonGroupsDelete(BaseDelete):
    success_message = "Group collection deleted."
    model = models.ComparisonGroups

    def get_success_url(self):
        self.parent = self.object.study_population
        return reverse("epi2:sp_detail", kwargs={"pk": self.parent.pk})


class GroupDetail(BaseDetail):
    model = models.Group


class GroupUpdate(BaseUpdateWithFormset):
    success_message = "Groups updated."
    model = models.Group
    form_class = forms.SingleGroupForm
    formset_factory = forms.GroupNumericalDescriptionsFormset

    def build_initial_formset_factory(self):
        return forms.GroupNumericalDescriptionsFormset(
            queryset=self.object.descriptions.all())

    def post_object_save(self, form, formset):
        for form in formset:
            form.instance.group = self.object