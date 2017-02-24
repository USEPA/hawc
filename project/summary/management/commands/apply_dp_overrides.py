from django.core.management.base import BaseCommand

import os
import json

from summary.models import DataPivot

HELP_TEXT = """Apply new overrides to complete data migration"""


class Command(BaseCommand):
    help = HELP_TEXT

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str,
                            help='Override filename')

    def handle(self, filename, **options):

        with open(os.path.expanduser(filename), 'r') as f:
            updates = json.loads(f.read())

        for update in updates:
            id = update['id']
            url = update['url']
            dp = DataPivot.objects.get(id=update['id'])

            if update['error']:
                self.stdout.write('Not updating #{}: {}'.format(id, url))
                continue

            settings = json.loads(dp.settings)
            settings['row_overrides'] = update['new_overrides']

            dp.settings = json.dumps(settings)

            self.stdout.write('Updated #{}: {}'.format(id, url))
            dp.save()
