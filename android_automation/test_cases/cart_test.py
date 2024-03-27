import os.path
import sys
import traceback
import com_utils.deeplink_control
from android_automation.page_action.context_change import change_webview_contexts, change_native_contexts, \
    switch_context
from com_utils.element_control import tap_control
from android_automation.page_action import product_detail_page, navigation_bar, cart_page, order_page, login_page, \
    selection_page
from com_utils.deeplink_control import move_to_home_Android
from com_utils.api_control import search_popular_keyword, search_result, product_detail, order_product_random_no
from time import sleep, time
from com_utils.code_optimization import finally_opt, exception_control


class Cart:
    def test_cart_list(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            login_page.check_login(self, wd, self.pconf['LOGIN_SUCCESS_ID'])

            print(f'[{test_name}] 테스트 시작')
            sleep(3)

            # 장바구니 진입하여 기존 상품 지우기
            cart_page.click_cart_btn(wd)
            cart_page.click_delete_btn_to_all_product(wd)

            # 필터를 건 검색 결과 화면에서 랜덤으로 상품번호 저장
            product_item_no = order_product_random_no()

            # 딥링크로 베스트 상품 PDP 진입
            com_utils.deeplink_control.move_to_pdp(wd, product_item_no)

            # PDP 상세 API 호출하여 상품명 확인
            best_product = product_detail(product_item_no)['item_name']

            # PDP에 노출되는 상품명과 API 호출된 상품명 동일한 지 확인
            best_pdp_name = product_detail_page.save_product_name(wd)
            product_detail_page.check_product_name(best_pdp_name, best_product)

            # 구매하기 버튼 선택
            product_detail_page.click_purchase_btn(wd)

            sleep(5)

            # 옵션의 존재 여부 확인하여 옵션 선택
            switch_context(wd, 'webview')
            product_detail_page.select_options(wd, product_item_no)
            change_native_contexts(wd)

            # 상품 장바구니에 담기
            product_detail_page.click_put_in_cart_btn(wd)

            # 상품 장바구니에 담기 완료 바텀시트 노출 확인
            product_detail_page.check_add_product_to_cart(wd)

            # 바텀시트 외의 영역 선택하여 바텀시트 닫기
            tap_control(wd)

            # 인기 검색어 1위 저장
            popular_1st_keyword = search_popular_keyword()['api_1st_keyword_name']

            # 1위 인기 검색어 검색 결과의 첫번째 상품 정보 불러오기
            search_product_item_no = search_result(popular_1st_keyword, 1)['product_item_no']

            # 딥링크로 검색 상품 진입
            com_utils.deeplink_control.move_to_pdp(wd, search_product_item_no)

            # PDP 상세 API 호출하여 상품명 확인
            search_product = product_detail(search_product_item_no)['item_name']

            # PDP 상품명과 API 호출된 상품명 동일한 지 확인
            keyword_pdp_name = product_detail_page.save_product_name(wd)
            product_detail_page.check_product_name(keyword_pdp_name, search_product)

            # 구매하기 버튼 선택
            product_detail_page.click_purchase_btn(wd)

            # 옵션의 존재 여부 확인하여 옵션 선택
            switch_context(wd, 'webview')
            product_detail_page.select_options(wd, search_product_item_no)
            change_native_contexts(wd)

            # 상품 장바구니에 담기
            product_detail_page.click_put_in_cart_btn(wd)

            # 상품 장바구니에 담기 완료 바텀시트 노출 확인
            product_detail_page.check_add_product_to_cart(wd)

            # 장바구니로 이동
            product_detail_page.click_move_to_cart(wd)
            # 웹뷰로 변경
            change_webview_contexts(wd)

            cart_page.check_product_name(wd, best_pdp_name, keyword_pdp_name)
            # 네이티브로 변경
            change_native_contexts(wd)
            # Home 탭으로 이동
            move_to_home_Android(wd)

            print(f'[{test_name}] 테스트 종료')

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      '장바구니에 상품을 담고 장바구니 리스트 확인')
            return result_data

    def test_change_cart_items(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            login_page.check_login(self, wd, self.pconf['LOGIN_SUCCESS_ID'])

            print(f'[{test_name}] 테스트 시작')
            # 장바구니 상품 추가 필요 여부 확인
            cart_page.check_need_to_add_product_to_cart(self, wd, self.pconf['LOGIN_SUCCESS_ID'], self.pconf['LOGIN_SUCCESS_PW'])

            navigation_bar.move_to_cart(wd)
            sleep(3)

            # 웹뷰로 전환
            change_webview_contexts(wd)

            # 상품 가격 저장
            product_price = cart_page.save_product_price(wd)

            # 장바구니 상품 삭제 전 주문 상품 수, 주문 가격 저장
            cart_total_count = cart_page.save_number_of_order_product(wd)
            cart_total_price = cart_page.save_total_order_price(wd)

            # 첫번째 상품 삭제 버튼 선택
            cart_page.click_delete_product(wd)

            # 상품 삭제 후, 주문 상품 수, 주문 가격 저장
            delete_total_count = cart_page.save_number_of_order_product(wd)
            delete_total_price = cart_page.save_total_order_price(wd)

            # 상품 삭제 확인
            cart_page.check_delete_product(cart_total_count, delete_total_count, cart_total_price,
                                           delete_total_price, product_price)

            # 상품 가격과 상품 개수 저장
            product_price = cart_page.save_product_price(wd)
            product_count = cart_page.save_product_count(wd)

            # 상품 추가 버튼 선택 후, 상품 개수와 총 주문 가격 저장
            cart_page.click_add_product(wd)
            add_product_count = cart_page.save_product_count(wd)
            add_total_price = cart_page.save_total_order_price(wd)
            sleep(3)

            # 상품 추가 확인
            cart_page.check_add_product(product_count, add_product_count, delete_total_price,
                                        add_total_price, product_price)

            # 네이티브로 전환
            change_native_contexts(wd)
            # Home 탭으로 이동
            move_to_home_Android(wd)

            print(f'[{test_name}] 테스트 종료')

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      '장바구니에 담긴 상품을 변경')
            return result_data

    def test_purchase_on_cart(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            login_page.check_login(self, wd, self.pconf['LOGIN_SUCCESS_ID'])

            print(f'[{test_name}] 테스트 시작')
            # 장바구니 화면 진입
            navigation_bar.move_to_cart(wd)
            sleep(3)
            # 웹뷰 전환
            change_webview_contexts(wd)
            # 상품명 저장
            product_name = cart_page.save_product_name_one(wd)
            # 총 결제 금액 저장
            total_price = cart_page.save_total_price(wd)
            # 1. [CHECK OUT] 버튼 선택
            cart_page.click_check_out_btn(wd)
            # 네이티브 전환
            change_native_contexts(wd)
            # 확인1 : 배송정보 타이틀 확인 - 구매하기 결제 화면 진입 확인
            order_page.check_delivery_info(wd)
            # 확인2 : 주문상품 정보 상품명 비교 확인 - 주문서 상품명 확인
            # 주문 상품 정보 상품명 확인
            order_page.check_order_product_name(wd, product_name)
            # # 확인3 : 가격 정보 비교 (스크롤 최하단 결제금액, 결제 버튼의 금액) - 주문서 가격 확인
            order_page.check_cart_purchase_price(wd, total_price)

            # Home 탭으로 이동
            # move_to_home_Android(wd)

            print(f'[{test_name}] 테스트 종료')

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      '장바구니에서 구매 주문서 화면으로 이동')
            return result_data