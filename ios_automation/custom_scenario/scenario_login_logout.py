import unittest
import os
import sys

iOS_path = os.path.join(os.path.dirname(__file__), '../..')
sys.path.append(iOS_path)

from appium.webdriver.appium_service import AppiumService
from com_utils import slack_result_notifications
from ios_automation import ios_setup
from selenium.common.exceptions import InvalidSessionIdException
from ios_automation.test_cases.login_test import UserLoginTest
from ios_automation.page_action.bottom_sheet import find_icon_and_close_bottom_sheet
from com_utils.testrail_api import *
from time import sleep


class IOSTestAutomation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pconf = requests.get(f"http://192.168.103.13:50/qa/personal/dajjeong").json()
        cls.conf = requests.get(f"http://192.168.103.13:50/qa/personal/info").json()
        cls.dconf = requests.get(f"http://192.168.103.13:50/qa/personal/def_names").json()
        cls.econf = requests.get(f"http://192.168.103.13:50/qa/personal/test_environment").json()

        # report data
        cls.count = 0
        cls.result_lists = []
        cls.total_time = ''
        cls.slack_result = ''

    def setUp(self):
        # device data
        device_info = self.pconf.get('ios_test_device')

        # Appium Service
        self.appium = AppiumService()
        self.appium.start(
            args=['-p', device_info['ios_custom_port'], '--base-path', '/wd/hub', '--default-capabilities',
                  '{"appium:chromedriverExecutable": "/usr/local/bin"}'])

        # webdriver
        self.wd, self.iOS_cap = getattr(ios_setup, device_info['ios_custom_device'])()
        self.wd.implicitly_wait(3)

        self.device_platform = self.iOS_cap.capabilities['platformName']
        self.device_name = self.iOS_cap.capabilities['appium:deviceName']
        self.user = 'custom'

        context = self.wd.contexts
        print(f'context 최초 확인 : {context}')

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

    def test_scenario_login_logout(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 앱 실행 후, 바텀 시트 노출 여부 확인
        sleep(3)
        find_icon_and_close_bottom_sheet(self.wd)

        # 이메일 로그인 실패 및 성공
        self.result_data = UserLoginTest.test_email_login_error_success(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 로그아웃
        self.result_data = UserLoginTest.test_logout(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 이메일 로그인 성공
        self.result_data = UserLoginTest.test_email_login_success(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 로그아웃
        self.result_data = UserLoginTest.test_logout(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)


if __name__ == '__main__':
    unittest.main()
