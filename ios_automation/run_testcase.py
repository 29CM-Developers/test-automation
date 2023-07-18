import logging
import time
import unittest

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
        self.wd.implicitly_wait(3)

    def tearDown(self):
        try:
            self.wd.terminate_app('kr.co.29cm.App29CM')
            print("앱 종료 완료")
            self.wd.quit()
            print("wd 종료 완료")
            self.appium.stop()
            print("appium 종료 완료")

            print("테스트 종료")
        except InvalidSessionIdException:
            self.appium.stop()

    def test_login(self):
        AutomationTesting.login_test(self, self.wd)

    def test_error_id_login(self):
        AutomationTesting.id_error_test(self, self.wd)


if __name__ == '__main__':
    unittest.main()
