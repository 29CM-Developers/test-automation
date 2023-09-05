import unittest
import os
import sys
and_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(and_path)
import requests
from appium.webdriver.appium_service import AppiumService
from android_automation.test_cases.bottom_sheet import test_bottom_sheet
from android_automation.test_cases.loginpage_test import LoginLogout
from android_automation.test_cases.not_login_user_test import NotLogin
from android_automation.test_cases.home_test import Home
from android_automation.test_cases.category_test import Category
from android_automation.test_cases.like_test import Like
from android_setup import note20_setup
from com_utils import slack_result_notifications
from selenium.common import InvalidSessionIdException


class AndroidTestAutomation(unittest.TestCase):

    def setUp(self):

        self.pconf = requests.get(f"http://192.168.103.13:50/qa/personal/hhj2008").json()
        self.conf = requests.get(f"http://192.168.103.13:50/qa/personal/info").json()
        self.dconf = requests.get(f"http://192.168.103.13:50/qa/personal/def_names").json()

        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4733', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin/chromedriver"}'])

        # webdriver
        self.wd, self.and_cap = note20_setup()
        self.wd.implicitly_wait(5)

        # report data
        self.count = 0
        self.result_lists = []
        self.total_time = ''
        self.slack_result = ''
        self.device_platform = self.and_cap.capabilities['platformName']
        self.device_name = self.and_cap.capabilities['appium:deviceName']

    def tearDown(self):
        try:
            self.wd.terminate_app('com.the29cm.app29cm')
            self.wd.quit()
            self.appium.stop()
        except InvalidSessionIdException:
            self.appium.stop()


    def test_automation_android_bvt(self):
        # 앱 실행 후, 바텀 시트 노출 여부 확인
        test_bottom_sheet(self.wd)

        # 현재 함수명 저장 - slack noti에 사용
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 실제 실행 - 이메일 로그인 성공
        self.result_data = LoginLogout.test_email_login_success(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 실제 실행 - 홈 배너 성공
        self.result_data = Home.test_home_banner(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 실제 실행 - 홈 컨텐츠 성공
        self.result_data = Home.test_home_contents(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 실제 실행 -   카테고리 기능 확인 성공
        self.result_data = Category.test_category_page(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 실제 실행 -   LIKE 존재하지 않는 경우 화면 확인 성공
        self.result_data = Like.test_no_like_item(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 실제 실행 -   LIKE 존재하는 경우 화면 확인 성공
        self.result_data = Like.test_like_item(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 실제 실행 - 이메일 로그아웃 성공
        self.result_data = LoginLogout.test_logout(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

if __name__ == '__main__':
    unittest.main()