import unittest
import yaml
import json

from appium.webdriver.appium_service import AppiumService
from selenium.common.exceptions import InvalidSessionIdException
from android_setup import mpark_setup
from android_automation.test_cases.sample_test import AutomationTesting


class AndroidTestAutomation(unittest.TestCase):

    def setUp(self):
        # yaml을 사용할 경우
        # with open('../../info.yaml') as ym:
        #     self.conf = yaml.load(ym, Loader=yaml.FullLoader)
        # self.account_id = self.conf['account_email']
        # json을 사용할 경우
        # self.conf = user_data.json()

        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4723', '--chromedriver-executable', '{chromedriver path}'])

        # webdriver
        self.wd, self.and_cap = mpark_setup()
        self.wd.implicitly_wait(5)

    def tearDown(self):
        try:
            self.wd.quit()
            self.appium.stop()
        except InvalidSessionIdException:
            self.appium.stop()

    def test_sample(self):
        error_text = AutomationTesting.default_test(self, self.wd)


if __name__ == '__main__':
    unittest.main()