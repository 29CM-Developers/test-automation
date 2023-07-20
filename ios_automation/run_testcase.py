import logging
import subprocess
import sys
import time
import unittest

import appium.options.ios
import requests
from appium.webdriver.appium_service import AppiumService

import ios_automation.ios_setup
from com_utils import slack_result_notifications
from ios_setup import dajjeong_setup
from ios_automation.test_cases.login_test import UserLoginTest
from ios_automation.test_cases.not_login_user_test import NotLoginUserTest
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
            # subprocess.run(['pkill', '-9', '-f', 'WebDriverAgentRunner'])

            print("테스트 종료")
        except InvalidSessionIdException:
            self.appium.stop()

    def test_iOS_bvt(self):

        self.def_name = sys._getframe().f_code.co_name

        # 비로그인 유저 사용 불가
        self.result_data = NotLoginUserTest.test_not_login_user_impossible(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 로그인 테스트
        self.result_data = UserLoginTest.test_login(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 로그인 실패 테스트
        self.result_data = UserLoginTest.test_login_error(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

    def test_iOS_full(self):
        self.def_name = sys._getframe().f_code.co_name

        # 비로그인 유저 사용 불가
        self.result_data = NotLoginUserTest.full_test_not_login_user_impossible(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

if __name__ == '__main__':
    unittest.main()
