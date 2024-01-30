import unittest
import os
import sys
and_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(and_path)
from appium.webdriver.appium_service import AppiumService
from android_automation.test_cases.loginpage_test import LoginLogout
from android_automation.test_cases.not_login_user_test import NotLogin
from android_automation.test_cases.category_test import Category
from android_automation.test_cases.home_test import Home
from android_automation.test_cases.plp_test import Plp
from android_automation.test_cases.search_test import Search
from android_automation.test_cases.my_test import My
from android_automation.test_cases.like_test import Like
from android_setup import s22_setup
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
        cls.result_lists = []
        cls.total_time = ''
        cls.slack_result = ''
        cls.user = 'manual'

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

    def tearDown(self):
        try:
            self.wd.quit()
            self.appium.stop()
        except Exception:
            self.appium.stop()

    def test_automation_android_bvt(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 비로그인 유저 사용 불가
        self.result_data = NotLogin.test_not_login_user_impossible(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 비로그인 유저 사용 가능
        self.result_data = NotLogin.test_not_login_user_possible(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 이메일 로그인 실패 및 성공
        self.result_data = LoginLogout.test_email_login_error_success(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 홈화면에서 다른 탭 이동 확인
        self.result_data = Home.test_move_tab_from_home(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # Like 존재하지 않을 경우
        self.result_data = Like.test_no_like_item(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # Like 존재하는 경우
        self.result_data = Like.test_like_item(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # PLP 기능 확인
        self.result_data = Plp.test_product_listing_page(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 카테고리 화면 확인
        self.result_data = Category.test_category_page(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # welove 화면 확인
        self.result_data = Category.test_welove(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # SEARCH -> 인기브랜드 확인
        self.result_data = Search.test_search_popular_brand(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # SEARCH -> 인기검색어 확인
        self.result_data = Search.test_search_popular_keyword(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # SEARCH -> 검색 결과 화면 확인
        self.result_data = Search.test_search_results_page(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # My -> 주문 건이 없을 경우, 주문 배송 조회
        self.result_data = My.test_track_delivery_without_orders(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # My -> 주문 건이 없을 경우, 상품 리뷰
        self.result_data = My.test_review_without_orders(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 로그아웃
        self.result_data = LoginLogout.test_logout(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)


if __name__ == '__main__':
    unittest.main()
