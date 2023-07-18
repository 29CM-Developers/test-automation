import logging
import sys
import time
import unittest

import requests
from appium.webdriver.appium_service import AppiumService

from com_utils import slack_result_notifications
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

        user_info = requests.get(f"http://192.168.103.13:50/qa/personal/mpark")
        self.pconf = user_info.json()
        public_info = requests.get(f"http://192.168.103.13:50/qa/personal/info")
        self.conf = public_info.json()

        self.count = 0
        self.total_time = ''
        self.slack_result = ''

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

    def test_dajjeong_login(self):

        self.def_name = sys._getframe().f_code.co_name

        # 1번째 테스트
        self.result_data = AutomationTesting.dajjeong_test(self, self.wd)
        # slack noti 작성 - 1회만 필요. ts값이 필요하여 self.response에 반환값 저장
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 2번째 테스트
        self.result_data = AutomationTesting.scroll_test(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        self.result_data = AutomationTesting.error_test(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)


    def test_error_id_login(self):
        AutomationTesting.id_error_test(self, self.wd)


if __name__ == '__main__':
    unittest.main()
