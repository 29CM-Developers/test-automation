import unittest
import os
import sys

and_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(and_path)
from appium.webdriver.appium_service import AppiumService
from android_automation.test_cases.loginpage_test import LoginLogout
from android_automation.test_cases.home_test import Home
from android_automation.test_cases.like_test import Like
from android_automation.test_cases.my_test import My
from android_automation.test_cases.cart_test import Cart
from android_automation.test_cases.payment_test import Payment
from android_automation.test_cases.pdp_test import Pdp
from android_automation.test_cases.join_test import Join
from android_setup import note20_setup
from com_utils import slack_result_notifications
from selenium.common import InvalidSessionIdException
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
        cls.user = 'manual'

    def setUp(self):

        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4733', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin/chromedriver"}'])

        # webdriver
        self.wd, self.and_cap = note20_setup()
        self.wd.implicitly_wait(5)
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

    def test_automation_android_bvt1(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 이메일 로그인 성공
        self.result_data = LoginLogout.test_email_login_success(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
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

        # PDP에서 좋아요
        self.result_data = Pdp.test_like_on_pdp(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

    def test_automation_android_bvt2(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 장바구니 리스트
        self.result_data = Cart.test_cart_list(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

    def test_automation_android_bvt3(self):

        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 장바구니 상품 변경
        self.result_data = Cart.test_change_cart_items(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 장바구니에서 구매 주문서로 이동
        self.result_data = Cart.test_purchase_on_cart(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 신용카드로 구매하기
        self.result_data = Payment.test_pay_with_credit_card(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

    def test_automation_android_bvt4(self):

        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # PDP에서 선물 주문서로 이동
        self.result_data = Pdp.test_gift_on_pdp(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # PDP에서 구매 주문서로 이동
        self.result_data = Pdp.test_purchase_on_pdp(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 무통장 입금으로 구매하기
        self.result_data = Payment.test_pay_with_virtual_account(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 로그아웃
        self.result_data = LoginLogout.test_logout(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 간편 회원가입 실패
        self.result_data = Join.test_simple_membership_registration_failure(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)


if __name__ == '__main__':
    unittest.main()
