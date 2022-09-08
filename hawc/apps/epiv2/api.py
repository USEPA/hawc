from rest_framework.decorators import action
from rest_framework.response import Response

from ..assessment.api import AssessmentEditViewset, BaseAssessmentViewset
from ..assessment.models import Assessment
from ..common.api.viewsets import EditPermissionsCheckMixin
from ..common.renderers import PandasRenderers
from . import exports, models, serializers


class EpiAssessmentViewset(BaseAssessmentViewset):
    model = Assessment

    @action(detail=True, url_path="export", renderer_classes=PandasRenderers)
    def export(self, request, pk):
        """
        Retrieve epidemiology data for assessment.
        """
        assessment: Assessment = self.get_object()
        published_only = not assessment.user_can_edit_object(request.user)
        qs = (
            models.DataExtraction.objects.get_qs(assessment)
            .published_only(published_only)
            .complete()
        )
        exporter = exports.EpiFlatComplete(qs, filename=f"{assessment}-epi")
        return Response(exporter.build_export())


class Design(EditPermissionsCheckMixin, AssessmentEditViewset):
    edit_check_keys = ["study"]
    assessment_filter_args = "study__assessment"
    model = models.Design
    serializer_class = serializers.DesignSerializer

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.all()