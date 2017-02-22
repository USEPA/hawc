from django.core.management.base import BaseCommand

import logging
import json
import os

from . import shared


HELP_TEXT = """Print row-override fields"""


class Command(BaseCommand):
    help = HELP_TEXT

    def add_arguments(self, parser):
        parser.add_argument('username', type=str,
                            help='Superuser username')
        parser.add_argument('password', type=str,
                            help='Superuser password')
        parser.add_argument('filename', type=str,
                            help='Override filename')
        parser.add_argument(
            '--hostname',
            dest='hostname',
            action='store',
            default='http://127.0.0.1:8000',
            help='Hostname for webcrawler')

    def handle(self, username, password, filename, **options):

        with open(os.path.expanduser(filename), 'r') as f:
            updates = json.loads(f.read())

        hostname = options['hostname']
        driver = shared.get_webdriver()
        shared.login(driver, hostname, username, password)
        for update in updates:
            id = update['id']
            url = update['url']
            old_display = update['html']

            expected_order = update['expected_order']

            logging.info(url)
            (dp_display, new_overrides, row_order) = \
                shared.get_content(driver, url)

            if str(expected_order['_dp_pk']) == \
                str(json.loads(row_order.get_attribute('innerHTML'))['_dp_pk']):
                self.stdout.write('Expected order identical: {}'.format(id))
            else:
                self.stdout.write('Expected order different: {}'.format(id))

            if old_display == dp_display.get_attribute('innerHTML'):
                self.stdout.write('Display identical: {}'.format(id))
            else:
                self.stdout.write('Display different: {}'.format(id))
