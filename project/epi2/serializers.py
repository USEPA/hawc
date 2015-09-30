from rest_framework import serializers

from assessment.serializers import EffectTagsSerializer, DoseUnitsSerializer
from study.serializers import StudySerializer

from utils.helper import SerializerHelper

from . import models


class EthnicitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ethnicity
        fields = ('id', 'name')


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country
        fields = ('name', 'id')


class StudyPopulationCriteriaSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="criteria.id")
    description = serializers.ReadOnlyField(source="criteria.description")
    criteria_type = serializers.CharField(source='get_criteria_type_display', read_only=True)

    class Meta:
        model = models.StudyPopulationCriteria
        fields = ('id', 'description', 'criteria_type')


class ExposureLinkSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = models.Exposure2
        fields = ('id', 'name', 'url')


class OutcomeLinkSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = models.Outcome
        fields = ('id', 'name', 'url')


class GroupNumericalDescriptionsSerializer(serializers.ModelSerializer):
    mean_type = serializers.CharField(source='get_mean_type_display', read_only=True)
    variance_type = serializers.CharField(source='get_variance_type_display', read_only=True)
    lower_type = serializers.CharField(source='get_lower_type_display', read_only=True)
    upper_type = serializers.CharField(source='get_upper_type_display', read_only=True)

    class Meta:
        model = models.GroupNumericalDescriptions
        exclude = ('group', )


class GroupSerializer(serializers.ModelSerializer):
    sex = serializers.CharField(source='get_sex_display', read_only=True)
    descriptions = GroupNumericalDescriptionsSerializer(many=True)
    ethnicities = EthnicitySerializer(many=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = models.Group


class ResultMetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ResultMetric


class SimpleExposureSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    metric_units = DoseUnitsSerializer()

    class Meta:
        model = models.Exposure2


class ComparisonGroupsLinkSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = models.ComparisonGroups
        fields = ('id', 'name', 'url')


class StudyPopulationSerializer(serializers.ModelSerializer):
    study = StudySerializer()
    criteria = StudyPopulationCriteriaSerializer(source='spcriteria', many=True)
    outcomes = OutcomeLinkSerializer(many=True)
    exposures = ExposureLinkSerializer(many=True)
    can_create_groups = serializers.BooleanField(read_only=True)
    group_collections = ComparisonGroupsLinkSerializer(many=True)
    country = serializers.CharField(source='country.name', read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    design = serializers.CharField(source='get_design_display', read_only=True)

    class Meta:
        model = models.StudyPopulation


class ExposureSerializer(serializers.ModelSerializer):
    study_population = StudyPopulationSerializer()
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    metric_units = DoseUnitsSerializer()

    class Meta:
        model = models.Exposure2


class GroupResultSerializer(serializers.ModelSerializer):
    main_finding_support = serializers.CharField(source='get_main_finding_support_display', read_only=True)
    p_value_qualifier = serializers.CharField(source='get_p_value_qualifier_display', read_only=True)
    p_value_text = serializers.CharField(read_only=True)
    group = GroupSerializer()

    class Meta:
        model = models.GroupResult


class ResultAdjustmentFactorSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="adjustment_factor.id")
    description = serializers.ReadOnlyField(source="adjustment_factor.description")

    class Meta:
        model = models.ResultAdjustmentFactor
        fields = ('id', 'description', 'included_in_final_model')


class SimpleComparisonGroupsSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    exposure = SimpleExposureSerializer()

    class Meta:
        model = models.ComparisonGroups


class ResultSerializer(serializers.ModelSerializer):
    metric = ResultMetricSerializer()
    factors = ResultAdjustmentFactorSerializer(source='resfactors', many=True)
    dose_response = serializers.CharField(source='get_dose_response_display', read_only=True)
    statistical_power = serializers.CharField(source='get_statistical_power_display', read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    results = GroupResultSerializer(many=True)
    variance_type = serializers.CharField(source='get_variance_type_display', read_only=True)
    estimate_type = serializers.CharField(source='get_estimate_type_display', read_only=True)
    full_name = serializers.CharField(source='__unicode__', read_only=True)
    groups = SimpleComparisonGroupsSerializer()

    class Meta:
        model = models.Result
        exclude = ('adjustment_factors', )


class OutcomeSerializer(serializers.ModelSerializer):
    study_population = StudyPopulationSerializer()
    effects = EffectTagsSerializer()
    diagnostic = serializers.CharField(source='get_diagnostic_display', read_only=True)
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    results = ResultSerializer(many=True)
    group_collections = ComparisonGroupsLinkSerializer(many=True)

    class Meta:
        model = models.Outcome


class ComparisonGroupsSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    exposure = ExposureSerializer()
    outcome = OutcomeSerializer()
    study_population = StudyPopulationSerializer()
    groups = GroupSerializer(many=True)

    class Meta:
        model = models.ComparisonGroups


SerializerHelper.add_serializer(models.Outcome, OutcomeSerializer)