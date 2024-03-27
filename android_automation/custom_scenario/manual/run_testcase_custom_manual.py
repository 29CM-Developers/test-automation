import unittest
import os
import sys
and_path = os.path.join(os.path.dirname(__file__), '../../..')
sys.path.append(and_path)
from appium.webdriver.appium_service import AppiumService
from android_automation.test_cases.not_login_user_test import NotLogin
from android_automation.test_cases.cart_test import Cart
from android_automation.test_cases.category_test import Category
from android_automation.test_cases.join_test import Join
from android_automation.test_cases.like_test import Like
from android_automation.test_cases.my_test import My
from android_automation.test_cases.payment_test import Payment
from android_automation.test_cases.pdp_test import Pdp
from android_automation.test_cases.plp_test import Plp
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
        cls.user = 'custom_manual'

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

    def test_scenario_not_login_user(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 비로그인 유저 사용 가능
        self.result_data = NotLogin.test_not_login_user_possible(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 비로그인 유저 사용 불가
        self.result_data = NotLogin.test_not_login_user_impossible(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)
    def test_scenario_plp(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # PLP 기능 확인
        self.result_data = Plp.test_product_listing_page(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)
    def test_scenario_category(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 카테고리 화면 확인
        self.result_data = Category.test_category_page(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # welove 화면 확인
        self.result_data = Category.test_welove(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)
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
    def test_scenario_like(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # Like 존재하는 경우
        self.result_data = Like.test_like_item(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # Like 존재하지 않을 경우
        self.result_data = Like.test_no_like_item(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)

    def test_scenario_cart(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 장바구니 리스트
        self.result_data = Cart.test_cart_list(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)
    def test_scenario_cart_1(self):

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

        slack_result_notifications.slack_add_end_emoji(self)

    def test_scenario_join(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 간편 회원가입 실패
        self.result_data = Join.test_simple_membership_registration_failure(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)
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
    def test_scenario_pdp(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # PDP에서 좋아요
        self.result_data = Pdp.test_like_on_pdp(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # PDP에서 선물 주문서로 이동 - 안정성 떨어져 안정화 후 적용 예정
        self.result_data = Pdp.test_gift_on_pdp(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # PDP에서 구매 주문서로 이동
        self.result_data = Pdp.test_purchase_on_pdp(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)
    def test_scenario_order_payment(self):
        # 메소드명과 일치하는 정보 받아오기
        self.def_name = self.dconf[sys._getframe().f_code.co_name]

        # 무통장 입금으로 구매하기
        self.result_data = Payment.test_pay_with_virtual_account(self, self.wd)
        self.response = slack_result_notifications.slack_notification(self)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        # 신용카드로 구매하기
        self.result_data = Payment.test_pay_with_credit_card(self, self.wd)
        self.count = slack_result_notifications.slack_thread_notification(self)
        self.total_time, self.slack_result = slack_result_notifications.slack_update_notification(self)

        slack_result_notifications.slack_add_end_emoji(self)

if __name__ == '__main__':
    unittest.main()
