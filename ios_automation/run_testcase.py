import logging
import time
import unittest
import subprocess

from appium.webdriver.appium_service import AppiumService
from ios_setup import dajjeong_setup
from ios_automation.test_cases.sample_test import AutomationTesting
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException


class IOSTestAutomation(unittest.TestCase):

    def setUp(self):
        # yaml을 사용할 경우
        # with open('../../info.yaml') as ym:
        #     self.conf = yaml.load(ym, Loader=yaml.FullLoader)
        # self.account_id = self.conf['account_email']
        # json을 사용할 경우
        # self.conf = user_data.json()

        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4724', '--base-path', '/wd/hub', '--default-capabilities', '{"appium:chromedriverExecutable": "/usr/local/bin"}'])

        # webdriver
        self.wd, self.iOS_cap = dajjeong_setup()
        self.wd.implicitly_wait(5)

    def tearDown(self):
        try:
            self.wd.quit()
            self.appium.stop()
            subprocess.run(['pkill', '-9', '-f', 'WebDriverAgentRunner'])
        except InvalidSessionIdException:
            self.appium.stop()

    def test_sample(self):
        AutomationTesting.default_test(self, self.wd)
        AutomationTesting.scroll_test(self, self.wd)

if __name__ == '__main__':
    unittest.main()
