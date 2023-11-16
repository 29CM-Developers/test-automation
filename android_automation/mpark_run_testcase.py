import time
import unittest
import os
import sys
and_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(and_path)
import requests
import subprocess

from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from android_setup import mpark_setup
from time import sleep
from android_automation.test_cases.sample_test import AutomationTesting
from com_utils import values_control, slack_result_notifications
from com_utils.element_control import aal, aalc, aalk, aals
from com_utils.testrail_api import *


class AndroidTestAutomation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pconf = requests.get(f"http://192.168.103.13:50/qa/personal/mpark").json()
        cls.conf = requests.get(f"http://192.168.103.13:50/qa/personal/info").json()
        cls.dconf = requests.get(f"http://192.168.103.13:50/qa/personal/def_names").json()
        cls.econf = requests.get(f"http://192.168.103.13:50/qa/personal/test_environment").json()

        # report data
        cls.count = 0
        cls.result_lists = []
        cls.total_time = ''
        cls.slack_result = ''

        cls.testcase_data = create_plan(cls, 'iOS')
        cls.testcases = get_tests(cls)


    def setUp(self):
        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4723', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin/chromedriver"}'])

        # webdriver
        self.wd, self.and_cap = mpark_setup()
        self.wd.implicitly_wait(5)
        self.device_platform = self.and_cap.capabilities['platformName']
        self.device_name = self.and_cap.capabilities['appium:deviceName']

    @classmethod
    def tearDownClass(cls):
        close_plan(cls)

    def tearDown(self):
        try:
            self.wd.quit()
            self.appium.stop()
        except Exception:
            self.appium.stop()

    def test_sample_def_name(self):
        # 테스트 자동화 실행 return값을 self.result_data에 넣으면 해당 값들을 가지고 slack noti를 보내게 됩니다
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        self.result_data = AutomationTesting.default_test(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        self.result_data = AutomationTesting.default_fail_test(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        self.result_data = AutomationTesting.default_test(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)


    def test_pass(self):
        # start_time = time.time()
        # self.wd.find_element(AppiumBy.ACCESSIBILITY_ID, "women_tab").click()
        sleep(10)
        post_layer = aal(self.wd, 'com.the29cm.app29cm:id/weloveRecyclerView')

        post = aal(post_layer, '//android.widget.LinearLayout[3]/android.widget.RelativeLayout/android.widget.TextView[1]')

        if post.is_displayed():
            print('display success')
        else:
            print('display fail')
        # post = post_layer.find_element(AppiumBy.XPATH, '//android.widget.LinearLayout[3]/android.widget.RelativeLayout/android.widget.TextView[1]')
        # print(f"{time.time() - start_time:.2f}")
        sleep(2)

    def test_testrail_api(self):
        pass

    def test_pass(self):
        send_test_result(self, 'PASS', '설정화면 진입')

if __name__ == '__main__':
    unittest.main()