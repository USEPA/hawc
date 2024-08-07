import pandas as pd
import pytest

from hawc.apps.common.helper import FlatExport
from hawc.apps.riskofbias import exports
from hawc.apps.riskofbias.models import RiskOfBiasScore


def check_metadata_accuracy(export: FlatExport):
    # check that metadata descriptive columns match those in data export
    assert isinstance(export.metadata, pd.DataFrame)
    assert export.metadata.columns.to_list() == ["Header", "Description"]
    assert export.metadata.Header.to_list() == export.df.columns.to_list()


@pytest.mark.django_db
class TestRiskOfBiasFlat:
    def test_metadata(self):
        qs = RiskOfBiasScore.objects.none()
        export = exports.RiskOfBiasExporter.flat_export(qs, filename="test")
        check_metadata_accuracy(export)


@pytest.mark.django_db
class TestRiskOfBiasCompleteFlat:
    def test_metadata(self):
        qs = RiskOfBiasScore.objects.none()
        export = exports.RiskOfBiasCompleteExporter.flat_export(qs, filename="test")
        check_metadata_accuracy(export)
