from ..common.helper import FlatFileExporter
from ..study.models import Study
from ..study.serializers import VerboseStudySerializer
from . import models, serializers


class RiskOfBiasFlat(FlatFileExporter):
    """
    Returns a complete export of active Final Risk of Bias reviews, without
    reviewer information.
    """

    final_only = True  # only return final data

    def get_serialized_data(self):
        assessment_id = self.kwargs["assessment_id"]
        qs = (
            Study.objects.filter(assessment_id=assessment_id)
            .prefetch_related("identifiers", "riskofbiases__scores__overridden_objects")
            .select_related("assessment")
        )
        ser = VerboseStudySerializer(qs, many=True)
        study_data = ser.data

        if not self.final_only:
            qs = (
                models.RiskOfBias.objects.filter(study__assessment_id=assessment_id, active=True)
                .select_related("author")
                .prefetch_related("scores__overridden_objects")
            )
            ser = serializers.RiskOfBiasSerializer(qs, many=True)
            rob_data = ser.data
            for study in study_data:
                study["riskofbiases"] = [rob for rob in rob_data if rob["study"] == study["id"]]

        return study_data

    def _get_header_row(self):
        header = []
        header.extend(Study.flat_complete_header_row())
        header.extend(models.RiskOfBias.flat_header_row(final_only=self.final_only))
        header.extend(models.RiskOfBiasScore.flat_complete_header_row())
        return header

    def _get_data_rows(self):
        rows = []
        for ser in self.get_serialized_data():
            domains = ser["rob_settings"]["domains"]
            metrics = ser["rob_settings"]["metrics"]
            domain_map = {domain["id"]: domain for domain in domains}
            metric_map = {
                metric["id"]: dict(metric, domain=domain_map[metric["domain_id"]])
                for metric in metrics
            }

            row1 = []
            row1.extend(Study.flat_complete_data_row(ser))

            robs = [rob for rob in ser.get("riskofbiases", [])]
            if self.final_only:
                robs = [rob for rob in robs if rob["final"] and rob["active"]]

            for rob in robs:
                row2 = list(row1)
                row2.extend(models.RiskOfBias.flat_data_row(rob, final_only=self.final_only))
                for score in rob["scores"]:
                    row3 = list(row2)
                    score["metric"] = metric_map[score["metric_id"]]
                    row3.extend(models.RiskOfBiasScore.flat_complete_data_row(score))
                    rows.append(row3)

        return rows


class RiskOfBiasCompleteFlat(RiskOfBiasFlat):
    """
    Returns a complete export of all Risk of Bias reviews including reviewer
    information.
    """

    final_only = False
