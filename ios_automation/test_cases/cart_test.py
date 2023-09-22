import os
import sys
import traceback
import requests
import com_utils.element_control

from time import time, sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils import values_control


class Cart:

    # 상품명 확인
    def product_name(self, product_item_no):
        response = requests.get(f'https://cache.29cm.co.kr/item/detail/{product_item_no}/')
        if response.status_code == 200:
            product_data = response.json()
            product_name = product_data['item_name']
            return product_name
        else:
            print('PDP 옵션 정보 API 불러오기 실패')

    # 옵션 존재 여부 확인
    def option_exist(self, product_item_no):
        response = requests.get(f'https://cache.29cm.co.kr/item/detail/{product_item_no}/')
        if response.status_code == 200:
            option_data = response.json()
            option_items_list = option_data['option_items']['list']
            if not option_items_list:
                exist = '옵션 없음'
                print('옵션 없는 상품')
                return exist
            else:
                exist = '옵션 있음'
                print('옵션 있는 상품')
                return exist
        else:
            print('PDP 옵션 정보 API 불러오기 실패')

    # 옵션의 항목명 리스트
    def option_layout(self, product_item_no):
        response = requests.get(f'https://cache.29cm.co.kr/item/detail/{product_item_no}/')
        if response.status_code == 200:
            option_data = response.json()
            option_items = option_data['option_items']['layout']
            return option_items
        else:
            print('PDP 옵션 정보 API 불러오기 실패')

    # 옵션 리스트
    def option_item_list(self, product_item_no):
        response = requests.get(f'https://cache.29cm.co.kr/item/detail/{product_item_no}/')
        if response.status_code == 200:
            option_data = response.json()
            option_list = option_data['option_items']['list']
            return option_list
        else:
            print('PDP 옵션 정보 API 불러오기 실패')

    # 옵션 존재 여부와 개수에 따라 옵션 선택
    def select_options(self, wd, product_item_no):
        exist = Cart.option_exist(self, product_item_no)
        if exist == '옵션 있음':
            option_layout = Cart.option_layout(self, product_item_no)
            option_item_list = Cart.option_item_list(self, product_item_no)

            for i in range(len(option_layout)):
                print(f'{i + 1}/{len(option_layout)}')
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, option_layout[i]).click()
                print(f'항목 : {option_layout[i]}')

                if i < len(option_layout) - 1:
                    wd.find_element(AppiumBy.XPATH,
                                    f'//XCUIElementTypeButton[@name="{option_item_list[0]["title"]}"]').click()
                    print(f'옵션 : {option_item_list[0]["title"]}')

                    if 'list' in option_item_list[0]:
                        option_item_list = option_item_list[0]['list']
                    else:
                        break
                else:
                    for option in range(len(option_item_list)):
                        if option_item_list[option]['limited_qty'] != 0:
                            wd.find_element(AppiumBy.XPATH,
                                            f'//XCUIElementTypeButton[@name="{option_item_list[option]["title"]}"]').click()
                            print(f'옵션 : {option_item_list[option]["title"]}')
                            break
                        else:
                            print(f'{option + 1}번째 옵션 품절')
                            pass
        else:
            pass

    def test_cart_list(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 여성의류 베스트 중 품절 상태가 아닌 첫번째 상품의 PDP에 딥링크로 진입
            product_item_no = ''
            best_response = requests.get(
                'https://recommend-api.29cm.co.kr/api/v4/best/items?categoryList=268100100&periodSort=NOW&limit=100&offset=0')
            if best_response.status_code == 200:
                best_product_data = best_response.json()

                for i in range(0, 100):
                    product_soldout = best_product_data['data']['content'][i]['isSoldOut']
                    if not product_soldout:
                        product_item_no = best_product_data['data']['content'][i]['itemNo']
                        print(f'베스트 상품 번호 : {product_item_no}')
                        break
                    else:
                        pass
            else:
                print('베스트 PLP API 불러오기 실패')

            best_product = Cart.product_name(self, product_item_no)
            print(f'베스트 상품 : {best_product}')

            # 딥링크로 베스트 상품 PDP 진입
            wd.get(f'app29cm://product/{product_item_no}')
            sleep(3)

            # PDP 상품명과 API 호출된 상품명 동일한 지 확인
            pdp_web = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView')
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'Select a slide to show')
                pdp_name = pdp_web.find_element(AppiumBy.XPATH,
                                                '//XCUIElementTypeOther[@index="5"]/XCUIElementTypeStaticText').get_attribute(
                    'name')
            except NoSuchElementException:
                pdp_name = pdp_web.find_element(AppiumBy.XPATH,
                                                '//XCUIElementTypeOther[@index="4"]/XCUIElementTypeStaticText').get_attribute(
                    'name')

            if best_product in pdp_name:
                print('pdp 진입 확인 - 베스트 상품')
            else:
                test_result = 'WARN'
                warning_texts.append(f'pdp 진입 확인 실패 - 베스트 상품 : {pdp_name} / {best_product}')
                print('pdp 진입 확인 실패 - 베스트 상품')

            # 구매하기 버튼 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '구매하기').click()

            # 옵션의 존재 여부 확인하여 옵션 선택
            Cart.select_options(self, wd, product_item_no)

            # 상품 장바구니에 담기
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니 담기').click()

            # 쿠폰 툴팁 발생 시, 장바구니 담기 완료 바텀시트 미노출로 장바구니 담기 버튼 재선택
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '받지 않은 쿠폰이 있어요')
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니 담기').click()
            except NoSuchElementException:
                pass

            # 상품 장바구니에 담기 완료 바텀시트 노출 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니에 상품이 담겼습니다.')
                print('상품 장바구니 담기 확인 - 베스트 상품')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('상품 장바구니 담기 확인 실패 - 베스트 상품')
                print('상품 장바구니 담기 확인 실패 - 베스트 상품')

            # 바텀시트 닫기
            element = wd.find_element(AppiumBy.XPATH,
                                      '//XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]')
            com_utils.element_control.element_scroll_control(wd, element, 'U', 40)

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
            pdp_web = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView')
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'Select a slide to show')
                pdp_name = pdp_web.find_element(AppiumBy.XPATH,
                                                '//XCUIElementTypeOther[@index="5"]/XCUIElementTypeStaticText').get_attribute(
                    'name')
            except NoSuchElementException:
                pdp_name = pdp_web.find_element(AppiumBy.XPATH,
                                                '//XCUIElementTypeOther[@index="4"]/XCUIElementTypeStaticText').get_attribute(
                    'name')

            if search_product in pdp_name:
                print('pdp 진입 확인 - 검색 상품')
            else:
                test_result = 'WARN'
                warning_texts.append(f'pdp 진입 확인 실패 - 검색 상품 : {pdp_name} / {search_product}')
                print('pdp 진입 확인 실패 - 검색 상품')

            # 구매하기 버튼 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '구매하기').click()

            # 옵션의 존재 여부 확인하여 옵션 선택
            Cart.select_options(self, wd, search_product_itemno)

            # 상품 장바구니에 담기
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니 담기').click()

            # 쿠폰 툴팁 발생 시, 장바구니 담기 완료 바텀시트 미노출로 장바구니 담기 버튼 재선택
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '받지 않은 쿠폰이 있어요')
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니 담기').click()
            except NoSuchElementException:
                pass

            # 상품 장바구니에 담기 완료 바텀시트 노출 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니에 상품이 담겼습니다.')
                print('상품 장바구니 담기 확인 - 베스트 상품')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('상품 장바구니 담기 확인 실패 - 베스트 상품')
                print('상품 장바구니 담기 확인 실패 - 베스트 상품')

            # 장바구니로 이동
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`label == "바로가기"`]').click()

            # # 장바구니에 담긴 베스트 상품 확인
            # try:
            #     wd.find_element(AppiumBy.ACCESSIBILITY_ID, best_product)
            #     print('장바구니 리스트 확인 - 베스트 상품')
            # except NoSuchElementException:
            #     test_result = 'WARN'
            #     warning_texts.append('장바구니 리스트 확인 실패 - 베스트 상품')
            #     print('장바구니 리스트 확인 실패 - 베스트 상품')
            #
            # # 장바구니에 담긴 검색 상품 확인
            # try:
            #     wd.find_element(AppiumBy.ACCESSIBILITY_ID, search_product)
            #     print('장바구니 리스트 확인 - 검색 상품')
            # except NoSuchElementException:
            #     test_result = 'WARN'
            #     warning_texts.append('장바구니 리스트 확인 실패 - 검색 상품')
            #     print('장바구니 리스트 확인 실패 - 검색 상품')

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
            wd.get(self.conf['deeplink']['home'])

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data
