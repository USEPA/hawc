from django.core.management.base import BaseCommand

import logging
import json

from . import shared
from summary.models import DataPivot

HELP_TEXT = """Print row-override fields"""


class Command(BaseCommand):
    help = HELP_TEXT

    def add_arguments(self, parser):
        parser.add_argument('username', type=str,
                            help='Superuser username')
        parser.add_argument('password', type=str,
                            help='Superuser password')
        parser.add_argument(
            '--hostname',
            dest='hostname',
            action='store',
            default='http://127.0.0.1:8000',
            help='Hostname for webcrawler')

    def handle(self, username, password, **options):
        hostname = options['hostname']
        pivots = shared.get_pivots_with_overrides(hostname)
        driver = shared.get_webdriver()
        shared.login(driver, hostname, username, password)
        for pivot in pivots:
            dp = DataPivot.objects.get(id=pivot['id'])
            logging.info(pivot['url'])
            (dp_display, new_overrides, row_order) = \
                shared.get_content(driver, pivot['url'])
            if row_order is None:
                pivot.update({
                    'error': True,
                    'html': dp_display.get_attribute('innerHTML'),
                    'settings': dp.settings,
                })
            else:
                pivot.update({
                    'error': False,
                    'html': dp_display.get_attribute('innerHTML'),
                    'settings': dp.settings,
                    'new_overrides': json.loads(new_overrides.get_attribute('innerHTML')),
                    'expected_order': json.loads(row_order.get_attribute('innerHTML'))
                })

        driver.close()
        self.stdout.write(json.dumps(pivots))
