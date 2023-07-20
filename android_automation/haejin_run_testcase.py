
import time
import unittest
import os
import sys
and_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(and_path)
import requests
import subprocess
from appium.webdriver.appium_service import AppiumService

from android_automation.test_cases.loginpage_test import LoginLogout
from android_automation.test_cases.notlogin_test import NotLogin
from android_setup import hhj2008_setup
from android_automation.test_cases.sample_test import AutomationTesting
from com_utils import values_control, slack_result_notifications, element_control


class AndroidTestAutomation(unittest.TestCase):

    def setUp(self):

        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4823', '--base-path', '/wd/hub', '--default-capabilities','{"appium:chromedriverExecutable": "/usr/local/bin"}'])
        # webdriver
        self.wd, self.android_options = hhj2008_setup()
        self.wd.implicitly_wait(5)

        user_info = requests.get(f"http://192.168.103.13:50/qa/personal/hhj2008")
        self.pconf = user_info.json()
        public_info=requests.get(f"http://192.168.103.13:50/qa/personal/info")
        self.conf = public_info.json()

        # 필요 report data
        self.count = 0
        self.total_time = ''
        self.slack_result = ''

    def tearDown(self):
        try:
            self.wd.terminate_app('com.the29cm.app29cm')
            self.wd.quit()
            self.appium.stop()
        except InvalidSessionIdException:
            self.appium.stop()

    def test_android_bvt_haejin(self):
        # 현재 함수명 저장 - slack noti에 사용
        self.def_name = sys._getframe().f_code.co_name

        # testcases 실행
        self.result_data = LoginLogout.email_login_fail(self, self.wd)
        # slack noti 작성 - 1회만 필요. ts값이 필요하여 self.response에 반환값 저장
        self.response = slack_result_notifications.slack_notification(self)
        # slack 스레드 추가 -
        self.count = slack_result_notifications.slack_thread_notification(self)
        # slack noti 업데이트
        self.total_time, self.slack_result  = slack_result_notifications.slack_update_notification(self)

        # 복수 testcases 실행 시 slack 스레드 추가 와 slack noti 업데이트 만 계속 추가
        # 실제 실행
        self.result_data = LoginLogout.email_login_pass(self, self.wd)
        # slack 스레드 추가
        self.count = slack_result_notifications.slack_thread_notification(self)
        # slack noti 업데이트
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # # 실제 실행
        # self.result_data = AutomationTesting.def_name_fail(self, self.wd)
        # # slack 스레드 추가
        # self.count = slack_result_notifications.slack_thread_notification(self)
        # # slack noti 업데이트
        # self.total_time, self.slack_result  = slack_result_notifications.slack_update_notification(self)


if __name__ == '__main__':
    unittest.main()