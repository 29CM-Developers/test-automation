
import unittest
import requests
import os
import sys
iOS_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(iOS_path)

from appium.webdriver.appium_service import AppiumService
from com_utils import slack_result_notifications
from ios_setup import dajjeong_setup
from ios_automation.test_cases.login_test import UserLoginTest
from ios_automation.test_cases.not_login_user_test import NotLoginUserTest
from ios_automation.test_cases.home_test import Home
from selenium.common.exceptions import InvalidSessionIdException


class IOSTestAutomation(unittest.TestCase):

    def setUp(self):
        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4924', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin"}'])

        # webdriver
        self.wd, self.iOS_cap = dajjeong_setup()
        self.wd.implicitly_wait(3)

        user_info = requests.get(f"http://192.168.103.13:50/qa/personal/dajjeong")
        self.pconf = user_info.json()
        public_info = requests.get(f"http://192.168.103.13:50/qa/personal/info")
        self.conf = public_info.json()
        def_info = requests.get(f"http://192.168.103.13:50/qa/personal/def_names")
        self.dconf = def_info.json()

        self.count = 0
        self.total_time = ''
        self.slack_result = ''

        self.device_platform = self.iOS_cap.capabilities['platformName']
        self.device_name = self.iOS_cap.capabilities['appium:deviceName']

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

    def test_iOS_bvt(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 비로그인 유저 사용 불가
        self.result_data = NotLoginUserTest.test_not_login_user_impossible(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 비로그인 유저 사용 가능
        self.result_data = NotLoginUserTest.test_not_login_user_possible(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 이메일 로그인 실패
        self.result_data = UserLoginTest.test_email_login_error(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 이메일 로그인 성공
        self.result_data = UserLoginTest.test_email_login_success(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 홈화면 배너 확인
        self.result_data = Home.test_home_banner(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 홈화면 컨텐츠 확인
        self.result_data = Home.test_home_contents(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 로그아웃
        self.result_data = UserLoginTest.test_logout(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

    def test_iOS_full(self):
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 비로그인 유저 사용 불가
        self.result_data = NotLoginUserTest.full_test_not_login_user_impossible(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)


if __name__ == '__main__':
    unittest.main()
