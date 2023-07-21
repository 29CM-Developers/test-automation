import time
import unittest
import sys
import requests

from appium.webdriver.appium_service import AppiumService
from android_setup import dajjeong_setup
from android_automation.test_cases.sample_test import AutomationTesting
from com_utils import slack_result_notifications


class AndroidTestAutomation(unittest.TestCase):

    def setUp(self):
        # user_info = requests.get(f"http://192.168.103.13:50/qa/personal/{os.environ.get('user')}")
        user_info = requests.get(f"http://192.168.103.13:50/qa/personal/mpark")
        self.pconf = user_info.json()
        public_info = requests.get(f"http://192.168.103.13:50/qa/personal/info")
        self.conf = public_info.json()

        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4923', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin/chromedriver"}'])

        # webdriver
        self.wd, self.and_cap = dajjeong_setup()
        self.wd.implicitly_wait(5)

        # report data
        self.count = 0
        self.total_time = ''
        self.slack_result = ''

    def tearDown(self):
        try:
            self.wd.close_app()
            print('앱 종료 실행')
            self.wd.quit()
            print('wd quit 실행')
            time.sleep(2)
            self.appium.stop()
            print('appium service stop 성공')
        except Exception:
            self.appium.stop()
            print('exception')

    def test_sample_def_name(self):
        # 테스트 자동화 실행 return값을 self.result_data에 넣으면 해당 값들을 가지고 slack noti를 보내게 됩니다
        self.def_name = sys._getframe().f_code.co_name
        self.device_platform = self.and_cap.capabilities['platformName']
        self.device_name = self.and_cap.capabilities['appium:deviceName']

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


if __name__ == '__main__':
    unittest.main()