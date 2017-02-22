from django.core.management.base import BaseCommand

import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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

    def get_webdriver(self):
        # enable browser logging
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'browser': 'ALL'}
        driver = webdriver.Chrome(desired_capabilities=d)
        driver.set_window_position(0, 0)
        driver.set_window_size(2560, 1440)
        return driver

    def login(self, driver, hostname, username, password):
        driver.get('{}/user/login/'.format(hostname))
        time.sleep(5)
        driver.find_element_by_id("id_username").send_keys(username)
        driver.find_element_by_id("id_password").send_keys(password)
        driver.find_element_by_id("submit-id-login").submit()

    def get_pivots_with_overrides(self, hostname):
        pivots = []
        for dp in DataPivot.objects.order_by('assessment_id', 'id').all():
            try:
                if dp.settings != 'undefined':
                    settings = json.loads(dp.settings)
            except:
                self.stdout.write('Failed: {}\n'.format(dp.settings))
                settings = None
            if settings:
                for row in settings['row_overrides']:
                    if row['offset'] != 0:
                        pivots.append({
                            'id': dp.id,
                            'url': '{}{}'.format(hostname, dp.get_absolute_url()),
                        })
                        break
        return pivots

    def handle(self, username, password, **options):
        hostname = options['hostname']
        pivots = self.get_pivots_with_overrides(hostname)
        driver = self.get_webdriver()
        self.login(driver, hostname, username, password)

        timeout = 10
        time_interval = 5

        for pivot in pivots:
            self.stdout.write(pivot['url'])

            driver.get(pivot['url'])
            dp_display = None
            newOverrides = None
            rowOrder = None
            elapsed_time = 0
            while rowOrder is None:
                time.sleep(time_interval)
                elapsed_time += time_interval
                try:
                    dp_display = driver.find_element_by_id('dp_display')
                    newOverrides = driver.find_element_by_id('newOverrides')
                    rowOrder = driver.find_element_by_id('rowOrder')
                except Exception:
                    pass

                if elapsed_time > timeout:
                    break

            if rowOrder is None:
                pivot.update({
                    'error': True,
                })
            else:
                pivot.update({
                    'error': False,
                    'html': dp_display.get_attribute('innerHTML'),
                    'new_overrides': json.loads(newOverrides.get_attribute('innerHTML')),
                    'expected_order': json.loads(rowOrder.get_attribute('innerHTML'))
                })

        driver.close()
        self.stdout.write(json.dumps(pivots))
