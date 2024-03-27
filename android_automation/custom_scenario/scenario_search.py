import unittest
import os
import sys
and_path = os.path.join(os.path.dirname(__file__), '../..')
sys.path.append(and_path)
from appium.webdriver.appium_service import AppiumService
from android_automation.test_cases.search_test import Search
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

    def test_scenario_search(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # SEARCH -> 인기브랜드 확인
        self.result_data = Search.test_search_popular_brand(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # SEARCH -> 인기검색어 확인
        self.result_data = Search.test_search_popular_keyword(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # # SEARCH -> 검색 결과 화면 확인
        self.result_data = Search.test_search_results_page(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)

if __name__ == '__main__':
    unittest.main()
