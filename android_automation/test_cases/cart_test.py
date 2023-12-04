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
from com_utils.api_control import search_popular_keyword, search_result, product_detail
from com_utils.element_control import tap_control
from android_automation.page_action import product_detail_page, navigation_bar, cart_page, order_page
from com_utils.deeplink_control import move_to_home_Android
from com_utils.testrail_api import send_test_result
from com_utils import values_control, element_control
from com_utils.element_control import aalc, aal, aals
from time import sleep, time


class Cart:
    def product_name(self, product_item_no):
        response = requests.get(f'https://cache.29cm.co.kr/item/detail/{product_item_no}/')
        if response.status_code == 200:
            product_data = response.json()
            product_name = product_data['item_name']
            print(f"api 호출로 받은 product_name : {product_name}")
            return product_name
        else:
            print('PDP 옵션 정보 API 불러오기 실패')

    # 옵션 존재 여부 확인
    def option_exist(self, product_item_no):
        print(f"option_exist product_item_no : {product_item_no}")
        response = requests.get(f'https://cache.29cm.co.kr/item/detail/{product_item_no}/')
        if response.status_code == 200:
            option_data = response.json()
            option_items_list = option_data['option_items']['list']
            print(option_items_list)
            if not option_items_list:
                option_exist = False
                print('옵션 없는 상품')
                return option_exist
            else:
                option_exist = True
                print('옵션 있는 상품')
                return option_exist
        else:
            print('PDP 옵션 정보 API 불러오기 실패')

    # 옵션의 항목명 리스트
    def option_layout(self, product_item_no):
        response = requests.get(f'https://cache.29cm.co.kr/item/detail/{product_item_no}/')
        if response.status_code == 200:
            option_data = response.json()
            option_items = option_data['option_items']['layout']
            print(f"option_items : {option_items}")
            return option_items
        else:
            print('PDP 옵션 정보 API 불러오기 실패')

    # 옵션 리스트
    def option_item_list(self, product_item_no):
        response = requests.get(f'https://cache.29cm.co.kr/item/detail/{product_item_no}/')
        if response.status_code == 200:
            option_data = response.json()
            option_list = option_data['option_items']['list']
            print(f"option_list : {option_list}")
            return option_list
        else:
            print('PDP 옵션 정보 API 불러오기 실패')

    # 옵션 존재 여부와 개수에 따라 옵션 선택
    def select_options(self, wd, product_item_no):
        option_exist = Cart.option_exist(self, product_item_no)
        if option_exist == True:
            option_layout = Cart.option_layout(self, product_item_no)
            option_item_list = Cart.option_item_list(self, product_item_no)

            # 웹뷰 컨텍스트로 전환
            current_context = wd.current_context
            print(current_context)
            native = wd.contexts[0]
            webview = wd.contexts[1]
            print(wd.contexts[1])

            wd.switch_to.context(webview)
            print(wd.contexts)
            sleep(1)
            WebDriverWait(wd, 10).until(EC.presence_of_element_located(
                (By.XPATH, f"//input[@class='text' and @placeholder='{option_layout[i]}' and @type='text']")))
            print("스위치 완료11")
            wd.switch_to.context(native)
            print("스위치 완료2")

            for i in range(len(option_layout)):
                print(f"항목 : {option_layout[i]}")
                option_layout = wd.find_element(By.XPATH,
                                                f"//input[@class='text' and @placeholder='{option_layout[i]}' and @type='text']")

                if option_layout:
                    # 엘리먼트를 사용하거나 값을 가져올 수 있습니다.
                    option_layout = option_layout[0]
                    option_layout.click()  # 엘리먼트를 클릭하거나 다른 작업 수행
                print(option_layout)
                option_layout.click()
                print(f"옵션 : {option_item_list[0]['title']}")
                option_item_list = wd.find_elements(AppiumBy.XPATH,
                                                    f"//*[contains(@text, '{option_item_list[0]['title']}')]")
                print(option_item_list)
                option_item_list[0].click()

                if i < len(option_layout) - 1:
                    if 'list' in option_item_list[0]:
                        option_item_list = option_item_list[0]['list']
                    else:
                        break
                wd.switch_to.context(native)
        else:
            pass

    def test_cart_list(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 여성의류 베스트 중 품절 상태가 아닌 첫번째 상품의 상품 번호 확인
            product_item_no = product_detail_page.save_no_soldout_product_no()

            # 딥링크로 베스트 상품 PDP 진입
            com_utils.deeplink_control.move_to_pdp(wd, product_item_no)

            # PDP 상세 API 호출하여 상품명 확인
            best_product = product_detail(product_item_no)['item_name']

            # PDP에 노출되는 상품명과 API 호출된 상품명 동일한 지 확인
            pdp_name1 = product_detail_page.save_product_name(wd)
            test_result = product_detail_page.check_product_name(warning_texts, pdp_name1, best_product)

            # 구매하기 버튼 선택
            product_detail_page.click_purchase_btn(wd)

            sleep(5)

            # 옵션의 존재 여부 확인하여 옵션 선택
            product_detail_page.select_options(wd, product_item_no)

            # 상품 장바구니에 담기
            product_detail_page.click_put_in_cart_btn(wd)

            # 상품 장바구니에 담기 완료 바텀시트 노출 확인
            test_result = product_detail_page.check_add_product_to_cart(wd, warning_texts)

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
            pdp_name2 = product_detail_page.save_product_name(wd)
            test_result = product_detail_page.check_product_name(warning_texts, pdp_name2, search_product)

            # 구매하기 버튼 선택
            product_detail_page.click_purchase_btn(wd)

            # 옵션의 존재 여부 확인하여 옵션 선택
            product_detail_page.select_options(wd, search_product_item_no)

            # 상품 장바구니에 담기
            product_detail_page.click_put_in_cart_btn(wd)

            # 상품 장바구니에 담기 완료 바텀시트 노출 확인
            test_result = product_detail_page.check_add_product_to_cart(wd, warning_texts)

            # 장바구니로 이동
            product_detail_page.click_move_to_cart(wd)
            # 웹뷰로 변경
            cart_page.change_webview_contexts(wd)
            wd.switch_to.window(wd.window_handles[1])
            print(wd.current_window_handle)
            test_result = cart_page.check_product_name(wd, warning_texts, pdp_name1, pdp_name2)
            # 네이티브로 변경
            cart_page.change_native_contexts(wd)
            # Home 탭으로 이동
            move_to_home_Android(self, wd)

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
            except Exception:
                pass
            wd.get('app29cm://home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '장바구니에 상품을 담고 장바구니 리스트 확인')
            return result_data

    def test_change_cart_items(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')
            navigation_bar.move_to_cart(wd)
            sleep(3)
            # 첫번째 상품 주문 금액 저장
            # 웹뷰로 변경
            cart_page.change_webview_contexts(wd)
            delete_product_price = cart_page.save_product_price(wd)
            # 토탈 금액 저장
            before_delete_total_price = cart_page.save_total_price(wd)
            # 첫번째 상품 삭제
            cart_page.click_delete_btn_to_first_product(wd)
            # 주문 상품 수 총 1개로 변경 확인
            test_result = cart_page.check_change_in_number_of_products(wd, warning_texts)
            # 삭제 후 토탈 금액 저장
            after_delete_total_price = cart_page.save_total_price(wd)
            # 총 주문금액이 해당 상품의 가격만큼 차감 확인
            test_result = cart_page.check_total_order_amount(wd, warning_texts, delete_product_price,
                                                             before_delete_total_price, after_delete_total_price)

            # 첫번째 상품 주문 금액 저장
            first_product_price = cart_page.save_product_price(wd)
            # 남은 상품의 구매 개수 [+] 1번 선택
            cart_page.click_to_increase_the_number_of_products(wd)
            # 상품의 개수 정보 2로 변경 확인
            test_result = cart_page.check_increase_in_product_count(wd, warning_texts)
            change_total_price = cart_page.save_total_price(wd)
            # 총 주문금액 변경 확인
            test_result = cart_page.check_change_total_order_amount(wd, warning_texts, first_product_price,
                                                                    change_total_price)
            # 네이티브 변경
            cart_page.change_native_contexts(wd)
            # Home 탭으로 이동
            move_to_home_Android(self, wd)

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
            except Exception:
                pass
            wd.get('app29cm://home')
        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '장바구니에 상품을 담고 장바구니 리스트 확인')
            return result_data

    def test_purchase_on_cart(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')
            # 장바구니 화면 진입
            navigation_bar.move_to_cart(wd)
            sleep(3)

            cart_page.change_webview_contexts(wd)
            # 상품명 저장
            product_name = cart_page.save_product_name_one(wd)
            # 총 결제 금액 저장
            total_price = cart_page.save_total_price(wd)

            cart_page.change_native_contexts(wd)
            # 1. [CHECK OUT] 버튼 선택
            cart_page.click_check_out_btn(wd)
            # 확인1 : 배송정보 타이틀 확인 - 구매하기 결제 화면 진입 확인
            test_result = order_page.check_delivery_info(wd, warning_texts)
            # 확인2 : 주문상품 정보 상품명 비교 확인 - 주문서 상품명 확인
            # 주문 상품 정보 상품명 확인
            order_page.check_order_product_name(wd, warning_texts, product_name)
            # # 확인3 : 가격 정보 비교 (스크롤 최하단 결제금액, 결제 버튼의 금액) - 주문서 가격 확인
            test_result = order_page.check_purchase_price(wd, warning_texts, total_price)
            # cart_page.change_native_contexts(wd)
            # Home 탭으로 이동
            move_to_home_Android(self, wd)

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
            except Exception:
                pass
            wd.get('app29cm://home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '장바구니에 상품을 담고 장바구니 리스트 확인')
            return result_data