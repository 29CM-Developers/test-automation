import unittest
import os
import sys
and_path = os.path.join(os.path.dirname(__file__), '../..')
sys.path.append(and_path)
from appium.webdriver.appium_service import AppiumService
from android_automation.test_cases.my_test import My
from android_automation.android_setup import s22_setup
from com_utils import slack_result_notifications
from com_utils.testrail_api import *


class AndroidTestAutomation(unittest.TestCase):
    @classmethod

    def setUpClass(cls):
        cls.pconf = requests.get(f"http://192.168.103.13:50/qa/personal/hhj2008").json()
        cls.conf = requests.get(f"http://192.168.103.13:50/qa/personal/info").json()
        cls.dconf = requests.get(f"http://192.168.103.13:50/qa/personal/def_names").json()
        cls.econf = requests.get(f"http://192.168.103.13:50/qa/personal/test_environment").json()

        # report data
        cls.count = 0
        cls.total_time = ''
        cls.slack_result = ''
        cls.user = 'custom'

    def setUp(self):

        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4734', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin/chromedriver"}'])

        # webdriver
        self.wd, self.and_cap = s22_setup()
        self.wd.implicitly_wait(5)
        # report data
        self.device_platform = self.and_cap.capabilities['platformName']
        self.device_name = self.and_cap.capabilities['appium:deviceName']
        # report data
        self.result_lists = []

    def tearDown(self):
        try:
            self.wd.quit()
            self.appium.stop()
        except Exception:
            self.appium.stop()
    def test_scenario_my(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # My -> 주문 건이 없을 경우, 주문 배송 조회
        self.result_data = My.test_track_delivery_without_orders(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # My -> 주문 건이 없을 경우, 상품 리뷰
        self.result_data = My.test_review_without_orders(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # My -> 설정
        self.result_data = My.test_enter_settings_screen(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # My -> 최근 본 컨텐츠 확인
        self.result_data = My.test_recently_viewed_content(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 쿠폰함
        self.result_data = My.test_coupons_list(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)

if __name__ == '__main__':
    unittest.main()
