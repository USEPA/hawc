from django.core.management.base import BaseCommand

import json
from summary.models import DataPivot

HELP_TEXT = """Print row-override fields"""


class Command(BaseCommand):
    help = HELP_TEXT

    def handle(self, *args, **options):
        for dp in DataPivot.objects.order_by('id').all():
            try:
                settings = json.loads(dp.settings)
            except:
                settings = None
            if settings:
                for row in settings['row_overrides']:
                    if row['offset'] != 0:
                        self.stdout.write('{{"id": {}, "overrides": [], "url": "http://127.0.0.1:8000{}"}},\n'.format(
                            dp.id, dp.get_absolute_url()))
                        break
