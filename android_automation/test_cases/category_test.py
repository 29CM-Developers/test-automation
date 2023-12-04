import os.path
import sys
import traceback
import logging
import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from com_utils import values_control, api_control, deeplink_control
from time import sleep, time
from com_utils.element_control import aal, aalk, aalc, scroll_to_element_id, scroll_up_to_element_id, scroll_control, \
    swipe_control, scroll_to_element_with_text, scroll, swipe_control, element_scroll_control
from android_automation.page_action import category_page, welove_page, navigation_bar
from com_utils.testrail_api import send_test_result

logger = logging.getLogger(name='Log')
logger.setLevel(logging.INFO)  ## 경고 수준 설정
formatter = logging.Formatter('|%(name)s||%(lineno)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler()  ## 스트림 핸들러 생성
stream_handler.setFormatter(formatter)  ## 텍스트 포맷 설정
logger.addHandler(stream_handler)  ## 핸들러 등록
class Category:

    def test_category_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[카테고리 기능 사용]CASE 시작")
            sleep(3)
            # 카테고리 탭 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'CATEGORY').click()

            api_large_list = []
            response = requests.get('https://recommend-api.29cm.co.kr/api/v5/best/categories/groups')
            if response.status_code == 200:
                large_category_data = response.json()
                # api에서 호출한 대 카테고리 리스트 저장
                for i in range(0, len(large_category_data['data'])):
                    api_large_category = large_category_data['data'][i]['categoryName']
                    api_large_list.append(api_large_category)
                print(f'api_large_list : {api_large_list}')

                # api에서 호출한 리스트 길이와 비교하여 노출되는 대 카테고리 리스트 저장
                large_list = []
                category_layer = aal(wd, 'com.the29cm.app29cm:id/shopComposeView')

                large_list.append(aal(wd, 'category_first_title').text)
                large_list.append(
                    aal(category_layer, '//android.view.View/android.view.View[2]/android.widget.TextView[2]').text)
                large_list.append(
                    aal(category_layer, '//android.view.View/android.view.View[2]/android.widget.TextView[3]').text)

                print(f'large_list : {large_list}')

                if set(large_list).intersection(api_large_list):
                    print('대 카테고리 리스트 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('카테고리 리스트 확인 실패')
                    print('대 카테고리 리스트 확인 실패')
            else:
                print('PDP 옵션 정보 API 불러오기 실패')

            # 대 카테고리, 중 카테고리 코드 번호 저장
            large_category_info = api_control.large_categories_info(self.conf["category_groups"]['women'],
                                                                    self.conf["large_categories"]['shoes'])
            large_category_code = large_category_info['large_category_code']
            large_category_name = large_category_info['large_category_name']
            medium_category_code = api_control.medium_categories_code(large_category_code,
                                                                      self.conf["medium_categories"]['sandals'])
            print(f'{large_category_code}/{large_category_name}/{medium_category_code}')

            # 신발 > 여성 > 전체 순으로 카테고리 선택
            category_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/shopComposeView')

            category_layer.find_element(AppiumBy.XPATH,
                                        '//android.view.View/android.view.View[2]/android.widget.TextView[@text="신발"]').click()
            category_layer.find_element(AppiumBy.XPATH,
                                        '//android.view.View/android.view.View[3]/android.widget.TextView[@text="WOMEN"]').click()

            category_layer.find_element(AppiumBy.ACCESSIBILITY_ID, 'all_title').click()

            # 타이틀명으로 카테고리 전체 페이지 진입 확인
            # API (large_category_info)에서 받아온 카테고리명으로 확인
            try:
                page_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtCategoryName')
                print(f'페이지 타이틀 : {page_title.text}')
                if '신발' in page_title.text:
                    print('카테고리 전체 페이지 진입 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('카테고리 전체 페이지 진입 확인 실패')
                    print('WARN : 카테고리 전체 페이지 진입 확인 실패')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('카테고리 전체 페이지 진입 확인 실패')
                print('WARN : 카테고리 전체 페이지 진입 확인 실패')

            # 카테고리 전체 리스트의 첫번째 상품 확인
            response = requests.get('https://search-api.29cm.co.kr/api/v4/products/category?categoryLargeCode=270100100&count=10')
            if response.status_code == 200:
                api_data = response.json()
                products = api_data['data']['products']
                first_product_name = products[0]['itemName']
                print(f"first_product_name : {first_product_name}")
                element = scroll_to_element_with_text(wd, first_product_name)
                if element.text in first_product_name:
                    print('상품 목록의 1번째 아이템명 일치 확인')
                else :
                    test_result = 'WARN'
                    warning_texts.append('상품 목록의 1번째 아이템명 일치 확인 실패')
                    print('상품 목록의 1번째 아이템명 일치 확인 실패')
            else:
                print('카테고리 그룹 API 호출 실패')
            element = scroll_up_to_element_id(wd, '샌들')
            element.click()
            sleep(3)
            try:
                page_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/mediumCategory')
                print(f'메뉴 트리 노출 확인 : {page_title.text}')
                if '샌들' in page_title.text:
                    print('중 카테고리 페이지 진입 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('중 카테고리 페이지 진입 확인 실패')
                    print('WARN : 중 카테고리 페이지 진입 확인 실패')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('중 카테고리 페이지 진입 확인 실패')
                print('WARN : 중 카테고리 페이지 진입 확인 실패')
            # selector_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/selector')
            # selector = aal(selector_layer,
            #                '//android.view.View/android.view.View/android.view.View[2]/android.widget.TextView')
            selector = aal(wd, 'plp_filter_sort')
            aalc(wd, 'plp_filter_sort')
            # 필터링 버튼 선택
            # selector.click()
            buttom_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/design_bottom_sheet')
            new_product_order = buttom_layer.find_element(AppiumBy.XPATH,
                                                          '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[2]/android.widget.TextView')
            new_product_order.click()
            sleep(1)
            print(f" 정렬 : {selector.text}")
            if '신상품순' in selector.text:
                print(f"정렬 확인 : {selector.text}")
            else:
                print(f"정렬 확인 실패 : {selector.text}")

            # 선택한 대 -> 중 카테고리에 해당하는 PLP API 호출
            response = requests.get(
                f'https://search-api.29cm.co.kr/api/v4/products/category?categoryLargeCode={large_category_code}&categoryMediumCode={medium_category_code}&count=50&sort=new')
            if response.status_code == 200:
                api_data = response.json()
                products = api_data['data']['products']
                first_product_name = products[0]['itemName']
                print(f"first_product_name : {first_product_name}")
                element = scroll_to_element_with_text(wd, first_product_name)
                if element.text in first_product_name:
                    print('상품 목록의 1번째 아이템명 일치 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('상품 목록의 1번째 아이템명 일치 확인 실패')
                    print('상품 목록의 1번째 아이템명 일치 확인 실패')

                print(f"api호출 1번째 아이템명 : {first_product_name} , 아이템명 : {element.text}")
                #1번째 상품 선택 PDP진입
                element.click()
                sleep(3)
                PDP_title_elements = wd.find_elements(By.XPATH, f"//*[contains(@text, '{first_product_name}')]")
                for PDP_title in PDP_title_elements:
                    print(PDP_title.text)
                    if PDP_title.text in first_product_name:
                        break
                PDP_product_title = PDP_title.text
                print(f"PDP_product_titile : {PDP_product_title} ")
                if first_product_name in PDP_product_title:
                    print("API 호출해서 불러온 상품명과 PDP 상품명이 동일한지 확인")
                else:
                    print("API 호출해서 불러온 상품명과 PDP 상품명이 동일한지 확인 실패")
                    test_result = 'WARN'
                    warning_texts.append("API 호출해서 불러온 상품명과 PDP 상품명이 동일한지 확인 실패")
                print(f"PDP 상품명 : {PDP_product_title} ")
                # 뒤로가기로 베스트 PLP 진입 확인
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
                print("뒤로가기 선택")
                sleep(2)
                # 뒤로가기로 카테고리 진입 확인
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
                print("뒤로가기 선택")
                sleep(2)
            else:
                print('카테고리 그룹 API 호출 실패')

            print("[카테고리 확인]CASE 종료")

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
            send_test_result(self, test_result, '카테고리를 선택해서 PLP 진입')
            return result_data

    def test_welove(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] CASE 시작')

            # 카테고리 탭 선택
            sleep(2)
            wd.get(self.conf['deeplink']['category'])
            print("카테고리탭 진입")
            close_bottom_sheet(self.wd)

            # 핀메뉴에서 위러브 페이지 진입
            category_page.click_pin_menu(wd, 'WELOVE')

            post_title = welove_page.save_first_post_title(wd)

            # 첫번째 포스트의 첫번째 해시태그 저장 후 선택
            post_hash_tag = welove_page.save_first_post_hashtag(wd)
            print(f'post_hash_tag : {post_hash_tag}')
            welove_page.click_first_post_hashtag(wd, post_hash_tag)

            # 해시태그 페이지 타이틀과 저장한 해시태그 비교 확인
            test_result = welove_page.check_hash_tag_title(wd, warning_texts, post_hash_tag)

            # welove 페이지에서 저장한 포스트가 해시태그 페이지에 노출되는지 확인
            test_result = welove_page.check_hash_tag_post(wd, warning_texts, post_title)

            # welove 페이지로 복귀
            welove_page.click_welove_back_btn(wd)

            # 포스트 추가 노출 확인
            test_result = welove_page.find_and_save_third_post(wd, warning_texts)

            # Home으로 복귀
            welove_page.click_welove_back_btn(wd)
            navigation_bar.move_to_home(wd)

            print(f'[{test_name}] CASE 종료')

        except Exception:
            test_result = 'FAIL'
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            error_text = traceback.format_exc().split('\n')
            try:
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
            except Exception:
                pass
            deeplink_control.move_to_home(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '카테고리 핀메뉴의 Welove 진입하여 탐색')
            return result_data
