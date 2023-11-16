import os.path
import sys
import traceback
import logging
from telnetlib import EC

import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from com_utils.testrail_api import send_test_result
from com_utils import values_control, element_control
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
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[장바구니]CASE 시작")
            sleep(2)
            # 상품A 딥링크로 진입
            # API 호출하여 itemNo 저장 > itemNo 사용하여 딥링크로 PDP 직행
            response = requests.get(
                'https://recommend-api.29cm.co.kr/api/v4/best/items?categoryList=268100100&periodSort=NOW&limit=100&offset=0')
            if response.status_code == 200:
                api_data = response.json()
                # content 배열에서 isSoldOut이 false인 첫 번째 아이템 찾기
                for item in api_data["data"]["content"]:
                    if not item["isSoldOut"]:
                        first_available_item_no = item["itemNo"]
                        print(f'first_available_item_no : {first_available_item_no}')
                        wd.get(f'app29cm://product/{first_available_item_no}')
                        print('딥링크 이동')
                        sleep(5)
                        best_product = Cart.product_name(self, first_available_item_no)
                        # PDP 상품명과 API 호출된 상품명 동일한 지 확인
                        # 스페셜 오더 상품 확인
                        try:
                            wd.find_element(AppiumBy.XPATH, "//*[contains(@text, 'SPECIAL-ORDER')]")
                            element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=4]'
                            print('SPECIAL-ORDER 상품 발견')
                        except NoSuchElementException:
                            print('SPECIAL-ORDER 상품 미발견')
                            element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=3]'
                            pass

                        PDP_product_title = wd.find_element(AppiumBy.XPATH, element_xpath).text
                        print(f"PDP_product_title : {PDP_product_title} ")
                        if best_product in PDP_product_title:
                            print("pdp 진입 확인 - 베스트 상품")
                        else:
                            print("pdp 진입 확인 실패 - 베스트 상품")
                            test_result = 'WARN'
                            warning_texts.append("베스트 상품 PDP 정상 확인 실패")
                        print(f"베스트 상품명 : {best_product} , PDP 상품명 : {PDP_product_title}  ")
                        sleep(1)

                        buy_button = wd.find_element(AppiumBy.XPATH, '//*[contains(@text,"구매하기")]')
                        buy_button.click()
                        sleep(2)

                        # 옵션의 존재 여부 확인하여 옵션 선택
                        # Cart.select_options(self, wd, first_available_item_no)

                        # 상품 장바구니에 담기
                        wd.find_element(AppiumBy.XPATH, "//*[contains(@text, '장바구니 담기')]").click()
                        sleep(2)
                        # 쿠폰 이슈로 한번더 선택
                        wd.find_element(AppiumBy.XPATH, "//*[contains(@text, '장바구니 담기')]").click()
                        sleep(2)
                        try:
                            add_to_cart = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/textAddToCart').text
                            print(f"add_to_cart : {add_to_cart}")
                            if add_to_cart == "장바구니에 상품이 담겼습니다.":
                                print("상품 장바구니 담기 확인 - 베스트 상품")
                            else:
                                test_result = 'WARN'
                                warning_texts.append('상품 장바구니 담기 확인 실패 - 베스트 상품')
                                print('상품 장바구니 담기 확인 실패 - 베스트 상품11')
                        except NoSuchElementException:
                            test_result = 'WARN'
                            warning_texts.append('상품 장바구니 담기 확인 실패 - 베스트 상품')
                            print('상품 장바구니 담기 확인 실패 - 베스트 상품22')
                        break
            else:
                print("API 호출에 실패했습니다.")
            # B상품 추가
            # 인기 검색어 1위 저장
            popular_1st_keyword = ''
            popular_response = requests.get(
                'https://search-api.29cm.co.kr/api/v4/keyword/popular?limit=100&brandLimit=30')
            if popular_response.status_code == 200:
                popluar_keyword_data = popular_response.json()
                popular_1st_keyword = popluar_keyword_data['data']['popularKeyword'][0]
                print(f'인기검색어 1위 : {popular_1st_keyword}')
            else:
                print('베스트 PLP API 불러오기 실패')
            # 1위 인기 검색어 검색 결과의 첫번째 상품 정보 불러오기
            search_product_itemno = ''
            search_response = requests.get(
                f'https://search-api.29cm.co.kr/api/v4/products/search?keyword={popular_1st_keyword}&excludeSoldOut=false')
            if search_response.status_code == 200:
                search_result_data = search_response.json()
                search_product_itemno = search_result_data['data']['products'][0]['itemNo']
                print(f'검색 싱픔 번호 : {search_product_itemno}')
            else:
                print('베스트 PLP API 불러오기 실패')

            search_product = Cart.product_name(self, search_product_itemno)
            print(f'검색 상품 : {search_product}')

            # 딥링크로 검색 상품 진입
            wd.get(f'app29cm://product/{search_product_itemno}')
            sleep(3)
            # PDP 상품명과 API 호출된 상품명 동일한 지 확인
            # 스페셜 오더 상품 확인
            try:
                wd.find_element(AppiumBy.XPATH, "//*[contains(@text, 'SPECIAL-ORDER')]")
                element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=4]'
                print('SPECIAL-ORDER 상품 발견')
            except NoSuchElementException:
                print('SPECIAL-ORDER 상품 미발견')
                element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=3]'
                pass

            PDP_product_title = wd.find_element(AppiumBy.XPATH, element_xpath).text
            print(f"PDP_product_title : {PDP_product_title} ")
            if search_product in PDP_product_title:
                print("pdp 진입 확인 - 베스트 상품")
            else:
                print("pdp 진입 확인 실패 - 베스트 상품")
                test_result = 'WARN'
                warning_texts.append("베스트 상품 PDP 정상 확인 실패")
            print(f"search_product : {search_product} , PDP 상품명 : {PDP_product_title}")
            sleep(1)

            buy_button = wd.find_element(AppiumBy.XPATH, '//*[contains(@text,"구매하기")]')
            buy_button.click()
            sleep(1)

            # 옵션의 존재 여부 확인하여 옵션 선택
            #  Cart.select_options(self, wd, first_available_item_no)

            # 상품 장바구니에 담기
            wd.find_element(AppiumBy.XPATH, "//*[contains(@text, '장바구니 담기')]").click()
            sleep(2)
            # 쿠폰 이슈로 한번더 선택
            wd.find_element(AppiumBy.XPATH, "//*[contains(@text, '장바구니 담기')]").click()
            sleep(2)
            try:
                add_to_cart = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/textAddToCart').text
                print(f"add_to_cart : {add_to_cart}")
                if add_to_cart == "장바구니에 상품이 담겼습니다.":
                    print("상품 장바구니 담기 확인 - 베스트 상품")
                else:
                    test_result = 'WARN'
                    warning_texts.append('상품 장바구니 담기 확인 실패 - 베스트 상품')
                    print(f'상품 장바구니 담기 확인 실패 - 베스트 상품 : {add_to_cart}')
                # 바로가기 버튼 선택, 확인 : 장바구니 리스트의 상품명과 PDP에서 저장한 상품명 비교 확인
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/textShortcuts').click()
                print("장바구니 바로가기 선택")
                sleep(2)
                print(f"PDP_product_title : {PDP_product_title}")
                product_title = wd.find_elements(By.XPATH, f"//*[contains(@text, '{PDP_product_title}')]")
                if len(product_title) != 0:
                    print('상품 장바구니 담기 확인 - 베스트 상품')
                    print(product_title[0].text)
                else:
                    test_result = 'WARN'
                    warning_texts.append('상품 장바구니 담기 확인 실패 - 베스트 상품')
                    print('상품 장바구니 담기 확인 실패 - 베스트 상품 NoSuchElementException')


            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('상품 장바구니 담기 확인 실패 - 베스트 상품')
                print('상품 장바구니 담기 확인 실패 - 베스트 상품 NoSuchElementException')

            print("[장바구니]CASE 종료")

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
