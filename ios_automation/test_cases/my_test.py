import os
import sys
import traceback
import com_utils.deeplink_control
import com_utils.api_control

from time import time
from com_utils.code_optimization import exception_control, finally_opt
from com_utils.api_control import my_coupon_list
from ios_automation.page_action import my_page, my_setting_page, product_detail_page, welove_page, \
    delivery_order_page, product_review_page, my_coupon_page, context_change


class My:
    def test_enter_settings_screen(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            # 세팅 페이지 진입
            my_page.enter_setting_page(wd)

            # 세팅 페이지 내 알림 문구 확인
            my_setting_page.check_notification(wd)

            # 마이페이지로 복귀
            my_setting_page.click_back_btn(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '설정화면 진입'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_recently_viewed_content(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 여성의류 베스트 1위 상품의 itemNo 확인
            product_item_no = com_utils.api_control.best_plp_women_clothes(1, 'NOW')['item_no']

            # 딥링크로 베스트 상품 PDP 진입
            com_utils.deeplink_control.move_to_pdp_iOS(wd, product_item_no)

            # PDP 상품 이름 저장 -> 이미지 1개일 경우와 2개 이상일 경우, XPATH index 변경되어 아래와 같이 작성
            recent_product_name = product_detail_page.save_remove_prefix_product_name(wd)

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            # 최근 본 상품 영역 확인
            my_page.check_recent_title(wd, '상품', recent_product_name)

            # welove 페이지 이동
            com_utils.deeplink_control.move_to_welove(self, wd)

            # 첫번째 추천 게시물명 확인 및 선택
            context_change.switch_context(wd, 'webview')
            post_title = welove_page.save_first_post_title(wd)
            welove_page.click_first_post(wd)
            context_change.switch_context(wd, 'native')

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            # 최근 본 상품 영역 확인
            my_page.check_recent_title(wd, "컨텐츠", post_title)

            # 최근 본 상품 영역 확장
            my_page.expand_recent_contents(wd)

            # 최근 본 상품 히스토리 확인
            my_page.check_recent_history(wd, recent_product_name, post_title)

            # 최근 본 상품 영역 축소
            my_page.close_recent_contents(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '최근 본 컨텐츠 확인'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_track_delivery_without_orders(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            # 주문배송조회 메뉴 선택
            my_page.click_delivery_order_menu(wd)

            # 배송 상품 없음 확인
            delivery_order_page.check_no_delivery_order(wd)

            # 마이페이지로 복귀
            delivery_order_page.click_back_btn(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '주문 건이 없을 경우, 주문 배송 조회 없음 확인'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_review_without_orders(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            # 싱픔 리뷰 페이지 진입
            my_page.click_review_menu(wd)

            # 작성 가능한 리뷰 없음 확인
            product_review_page.check_no_reviews_available(wd)

            # 내 리뷰 탭 진입하여 작성한 리뷰 없음 확인
            product_review_page.click_my_review_tab(wd)
            product_review_page.check_no_written_reviews(wd)

            # Home 탭으로 복귀
            # product_review_page.click_back_btn(wd)
            # navigation_bar.move_to_home(wd)
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '주문 건이 없을 경우, 상품 리뷰 없음 확인'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_coupons_list(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            # 쿠폰 메뉴 선택
            my_page.click_coupon_menu(wd)

            # 장바구니 타입 선택
            my_coupon_page.click_coupon_type(wd)
            my_coupon_page.click_option_cart(wd)

            # API 호출 쿠폰 목록과 노출되는 쿠폰 목록 저장
            api_coupon_list = my_coupon_list(self.pconf['id_29cm'], self.pconf['password_29cm'], 'CART')
            coupon_list = my_coupon_page.save_my_coupon_list(wd)

            my_coupon_page.check_coupon_list(wd, api_coupon_list, coupon_list, '장바구니')

            # 상품 쿠폰 타입 선택
            my_coupon_page.click_coupon_type(wd)
            my_coupon_page.click_option_product(wd)

            # API 호출 쿠폰 목록과 노출되는 쿠폰 목록 저장
            api_coupon_list = my_coupon_list(self.pconf['id_29cm'], self.pconf['password_29cm'], 'PRODUCT')
            coupon_list = my_coupon_page.save_my_coupon_list(wd)

            my_coupon_page.check_coupon_list(wd, api_coupon_list, coupon_list, '상품')

            my_coupon_page.click_back_btn(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '보유하고 있는 쿠폰 목록 확인'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data
