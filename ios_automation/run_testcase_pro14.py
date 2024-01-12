
import unittest
import requests
import os
import sys

iOS_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(iOS_path)

from appium.webdriver.appium_service import AppiumService
from com_utils import slack_result_notifications
from ios_setup import pro14_setup
from ios_automation.test_cases.login_test import UserLoginTest
from ios_automation.test_cases.home_test import Home
from ios_automation.page_action.bottom_sheet import close_bottom_sheet
from ios_automation.test_cases.cart_test import Cart
from ios_automation.test_cases.my_test import My
from ios_automation.test_cases.pdp_test import Pdp
from ios_automation.test_cases.payment_test import Payment
from ios_automation.test_cases.join_test import Join
from selenium.common.exceptions import InvalidSessionIdException
from com_utils.testrail_api import *


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

        cls.testcase_data = create_plan(cls, 'iOS', 'iPhone Pro 14', cls.pconf['pro14_tc_ids'])
        cls.testcases = get_tests(cls)

    def setUp(self):
        # Appium Service
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4743', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin"}'])

        # webdriver
        self.wd, self.iOS_cap = pro14_setup()
        self.wd.implicitly_wait(3)

        self.device_platform = self.iOS_cap.capabilities['platformName']
        self.device_name = self.iOS_cap.capabilities['appium:deviceName']

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

    @classmethod
    def tearDownClass(cls):
        close_plan(cls)

    def test_automation_iOS_bvt(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 앱 실행 후, 바텀 시트 노출 여부 확인
        close_bottom_sheet(self.wd)

        # 이메일 로그인 성공
        self.result_data = UserLoginTest.test_email_login_success(self, self.wd)
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

        # 장바구니 리스트
        self.result_data = Cart.test_cart_list(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 장바구니 상품 변경
        self.result_data = Cart.test_change_cart_items(self, self.wd)
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

        # PDP에서 선물 주문서로 이동
        self.result_data = Pdp.test_gift_on_pdp(self, self.wd)
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

        # 로그아웃
        self.result_data = UserLoginTest.test_logout(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 간편 회원가입 실패
        self.result_data = Join.test_simple_membership_registration_failure(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)


if __name__ == '__main__':
    unittest.main()
