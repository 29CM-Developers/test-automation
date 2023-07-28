import unittest
import os
import sys
import requests
from appium.webdriver.appium_service import AppiumService
from android_automation.test_cases.loginpage_test import LoginLogout
from android_automation.test_cases.not_login_user_test import NotLogin
from android_setup import hhj2008_setup
from com_utils import slack_result_notifications
from selenium.common import InvalidSessionIdException

and_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(and_path)
class AndroidTestAutomation(unittest.TestCase):

    def setUp(self):

        user_info = requests.get(f"http://192.168.103.13:50/qa/personal/hhj2008")
        self.pconf = user_info.json()
        public_info=requests.get(f"http://192.168.103.13:50/qa/personal/info")
        self.conf = public_info.json()
        def_info = requests.get(f"http://192.168.103.13:50/qa/personal/def_names")
        self.dconf = def_info.json()

        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4823', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin/chromedriver"}'])
        # webdriver
        self.wd, self.android_options = hhj2008_setup()
        self.wd.implicitly_wait(5)

        # 필요 report data
        self.count = 0
        self.total_time = ''
        self.slack_result = ''

        self.device_platform = self.android_options.capabilities['platformName']
        self.device_name = self.android_options.capabilities['appium:deviceName']

    def tearDown(self):
        try:
            self.wd.terminate_app('com.the29cm.app29cm')
            self.wd.quit()
            self.appium.stop()
        except InvalidSessionIdException:
            self.appium.stop()

    def test_android_bvt(self):
        # 현재 함수명 저장 - slack noti에 사용
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # testcases 실행 - 비로그인 사용 불가 기능 사용
        self.result_data = NotLogin.test_not_login_user_impossible(self, self.wd)
        # slack noti 작성 - 1회만 필요. ts값이 필요하여 self.response에 반환값 저장
        self.response = slack_result_notifications.slack_notification(self)
        # slack 스레드 추가 -
        self.count = slack_result_notifications.slack_thread_notification(self)
        # slack noti 업데이트
        self.total_time, self.slack_result  = slack_result_notifications.slack_update_notification(self)

        # 복수 testcases 실행 시 slack 스레드 추가 와 slack noti 업데이트 만 계속 추가
        # 실제 실행 - 비로그인 사용 가능 기능 사용
        self.result_data = NotLogin.test_not_login_user_possible(self, self.wd)
        # slack 스레드 추가
        self.count = slack_result_notifications.slack_thread_notification(self)
        # slack noti 업데이트
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 실제 실행 - 이메일 로그인 실패
        self.result_data = LoginLogout.test_email_login_error(self, self.wd)
        # slack 스레드 추가
        self.count = slack_result_notifications.slack_thread_notification(self)
        # slack noti 업데이트
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 실제 실행 - 이메일 로그인 성공
        self.result_data = LoginLogout.test_email_login_success(self, self.wd)
        # slack 스레드 추가
        self.count = slack_result_notifications.slack_thread_notification(self)
        # slack noti 업데이트
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)
        # 실제 실행 - 이메일 로그아웃 성공
        self.result_data = LoginLogout.test_logout(self, self.wd)
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