from django.core import serializers
from django.db.models.loading import get_model
from django.core.management.base import BaseCommand, CommandError


HELP_TEXT = """Recursively dump data for a given assessment in HAWC."""


class Command(BaseCommand):
    help = HELP_TEXT

    def add_arguments(self, parser):
        parser.add_argument('assessment_id', type=int)
        parser.add_argument('--format', default='json', dest='format',
            help='Specifies the output serialization format for fixtures.')
        parser.add_argument('--output', default='output.txt', dest='output',
            help='Specifies file to which the output is written.')

    def handle(self, *args, **options):
        id_ = options['assessment_id']
        format_ = options['format']
        output = options['output']

        if format_ not in serializers.get_serializer_formats():
            raise CommandError("Output format not found: {}".format(format_))

        def get_objects():
            for qs in [

                # assessment
                get_model('assessment', 'assessment').objects.filter(id=id_),
                get_model('assessment', 'baseendpoint').objects.filter(assessment_id=id_),
                get_model('assessment', 'effecttag').objects.filter(baseendpoint__assessment_id=id_),

                # literature
                get_model('lit', 'reference').objects.filter(assessment_id=id_),
                get_model('lit', 'identifiers').objects.filter(references__assessment_id=id_),
                get_model('lit', 'search').objects.filter(assessment_id=id_),
                get_model('lit', 'referencetags').objects.filter(content_object__assessment_id=id_),
                get_model('lit', 'referencefiltertag').get_assessment_root(id_).get_descendants(),

                # study
                get_model('study', 'study').objects.filter(assessment_id=id_),
                get_model('study', 'studyqualitydomain').objects.filter(assessment_id=id_),
                get_model('study', 'studyqualitymetric').objects.filter(domain__assessment_id=id_),
                get_model('study', 'studyquality').objects.filter(metric__domain__assessment_id=id_),

                # animal
                get_model('animal', 'experiment').objects.filter(study__assessment_id=id_),

                get_model('animal', 'animalgroup').objects.filter(experiment__study__assessment_id=id_),
                get_model('animal', 'dosingregime').objects.filter(dosed_animals__experiment__study__assessment_id=id_),
                get_model('animal', 'dosegroup').objects.filter(dose_regime__dosed_animals__experiment__study__assessment_id=id_),
                get_model('assessment', 'doseunits').objects.filter(dosegroup__dose_regime__dosed_animals__experiment__study__assessment_id=id_),
                get_model('assessment', 'species').objects.filter(animalgroup__experiment__study__assessment_id=id_),
                get_model('assessment', 'strain').objects.filter(animalgroup__experiment__study__assessment_id=id_),

                get_model('animal', 'endpoint').objects.filter(assessment_id=id_),
                get_model('animal', 'endpointgroup').objects.filter(endpoint__assessment_id=id_),

                # export epi
                get_model('epi', 'studypopulation').objects.filter(study__assessment_id=id_),
                get_model('epi', 'studypopulationcriteria').objects.filter(criteria__assessment_id=id_),
                get_model('epi', 'country').objects.filter(studypopulation__study__assessment_id=id_),
                get_model('epi', 'criteria').objects.filter(assessment_id=id_),
                get_model('epi', 'adjustmentfactor').objects.filter(assessment_id=id_),

                get_model('epi', 'exposure').objects.filter(study_population__study__assessment_id=id_),

                get_model('epi', 'comparisonset').objects.filter(study_population__study__assessment_id=id_),
                get_model('epi', 'comparisonset').objects.filter(outcome__assessment_id=id_),
                get_model('epi', 'group').objects.filter(comparison_set__study_population__study__assessment_id=id_),
                get_model('epi', 'group').objects.filter(comparison_set__outcome__assessment_id=id_),

                get_model('epi', 'outcome').objects.filter(assessment_id=id_),
                get_model('epi', 'result').objects.filter(outcome__assessment_id=id_),
                get_model('epi', 'resultmetric').objects.filter(results__outcome__assessment_id=id_),
                get_model('epi', 'resultadjustmentfactor').objects.filter(adjustment_factor__assessment_id=id_),

                get_model('epi', 'groupresult').objects.filter(result__outcome__assessment_id=id_),

                # export meta-epi
                get_model('epimeta', 'metaprotocol').objects.filter(study__assessment_id=id_),
                get_model('epimeta', 'metaresult').objects.filter(protocol__study__assessment_id=id_),
                get_model('epimeta', 'singleresult').objects.filter(meta_result__protocol__study__assessment_id=id_),

                # export invitro
                get_model('invitro', 'ivexperiment').objects.filter(study__assessment_id=id_),
                get_model('invitro', 'ivchemical').objects.filter(study__assessment_id=id_),
                get_model('invitro', 'ivcelltype').objects.filter(study__assessment_id=id_),
                get_model('invitro', 'ivendpoint').objects.filter(assessment_id=id_),
                get_model('invitro', 'ivendpointgroup').objects.filter(endpoint__assessment_id=id_),
                get_model('invitro', 'ivbenchmark').objects.filter(endpoint__assessment_id=id_),
                get_model('invitro', 'ivendpointcategory').get_root(id_).get_descendants(),

                # export summary
                get_model('summary', 'datapivot').objects.filter(assessment_id=id_),
                get_model('summary', 'datapivotquery').objects.filter(assessment_id=id_),
                get_model('summary', 'datapivotupload').objects.filter(assessment_id=id_),
                get_model('summary', 'visual').objects.filter(assessment_id=id_),
                get_model('summary', 'summarytext').objects.filter(assessment_id=id_),
            ]:
                for obj in qs.iterator():
                    yield obj

        stream = open(output, 'w')
        serializers.serialize(format_, get_objects(), stream=stream)
        stream.close()
