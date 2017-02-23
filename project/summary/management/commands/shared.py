import logging
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from summary.models import DataPivot


HELP_TEXT = """Print row-override fields"""


def get_webdriver():
    # enable browser logging
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=d)
    driver.set_window_position(0, 0)
    driver.set_window_size(2560, 1440)
    return driver


def login(driver, hostname, username, password):
    driver.get('{}/user/login/'.format(hostname))
    time.sleep(5)
    driver.find_element_by_id("id_username").send_keys(username)
    driver.find_element_by_id("id_password").send_keys(password)
    driver.find_element_by_id("submit-id-login").submit()


def get_pivots_with_overrides(hostname):
    pivots = []
    for dp in DataPivot.objects.order_by('assessment_id', 'id').all():
        try:
            if dp.settings != 'undefined':
                settings = json.loads(dp.settings)
        except:
            logging.info('Failed: {}\n'.format(dp.settings))
            settings = None
        if settings:
            for row in settings['row_overrides']:
                if row['offset'] != 0:
                    pivots.append({
                        'id': dp.id,
                        'url': '{}{}'.format(hostname, dp.get_absolute_url()),
                        'original_settings': dp.settings,
                    })
                    break
    return pivots


def get_content(driver, url):
    timeout = 300  # 5 min
    time_interval = 2

    driver.get(url)
    dp_display = None
    new_overrides = None
    row_order = None
    elapsed_time = 0
    while row_order is None:
        time.sleep(time_interval)
        elapsed_time += time_interval
        try:
            dp_display = driver.find_element_by_id('dp_display')
            new_overrides = driver.find_element_by_id('newOverrides')
            row_order = driver.find_element_by_id('rowOrder')
        except Exception:
            pass

        loader = driver.find_element_by_id('loading_div')
        if 'display: none;' in loader.get_attribute('style'):
            break

        if elapsed_time > timeout:
            break

    return (dp_display, new_overrides, row_order)
