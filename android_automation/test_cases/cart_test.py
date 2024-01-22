import os.path
import sys
import traceback
import logging
from telnetlib import EC
import requests
import com_utils.deeplink_control
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from android_automation.page_action.context_change import change_webview_contexts, change_native_contexts, \
    switch_context
from com_utils.api_control import search_popular_keyword, search_result, product_detail
from com_utils.element_control import tap_control
from android_automation.page_action import product_detail_page, navigation_bar, cart_page, order_page
from com_utils.deeplink_control import move_to_home_Android
from com_utils.testrail_api import send_test_result
from com_utils import values_control, element_control
from com_utils.element_control import aalc, aal, aals
from com_utils.api_control import search_popular_keyword, search_result, product_detail, order_product_random_no
from time import sleep, time


class Cart:
    def test_cart_list(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
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
            change_webview_contexts(wd)
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
            # 오류 발생 시 테스트 결과를 실패로 한다
            test_result = 'FAIL'
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc().split('\n')
            try:
                # 에러메시지 분류 시 예외처리
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
            except Exception:
                pass
            # 네이티브 변경
            change_native_contexts(wd)
            wd.get('app29cm://home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"

            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            send_test_result(self, test_result, '장바구니에 상품을 담고 장바구니 리스트 확인')
            return result_data

    def test_change_cart_items(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')
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
            # 오류 발생 시 테스트 결과를 실패로 한다
            test_result = 'FAIL'
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc().split('\n')
            try:
                # 에러메시지 분류 시 예외처리
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
            except Exception:
                pass
            # 네이티브 변경
            change_native_contexts(wd)
            wd.get('app29cm://home')
        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            send_test_result(self, test_result, '장바구니에 상품을 담고 장바구니 리스트 확인')
            return result_data

    def test_purchase_on_cart(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
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
            # 오류 발생 시 테스트 결과를 실패로 한다
            test_result = 'FAIL'
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc().split('\n')
            try:
                # 에러메시지 분류 시 예외처리
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
            except Exception:
                pass
            # 네이티브 변경
            change_native_contexts(wd)
            wd.get('app29cm://home')
        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            send_test_result(self, test_result, '장바구니에 상품을 담고 장바구니 리스트 확인')
            return result_data