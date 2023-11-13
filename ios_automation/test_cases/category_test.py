
import os
import sys
import traceback
import requests
import com_utils.api_control
import com_utils.element_control

from time import time, sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils import values_control
from ios_automation.page_action import category_page, welove_page, navigation_bar


class Category:
    def test_category_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        print(f'[{test_name}] 테스트 시작')

        try:
            # 카테고리 탭 선택
            wd.get(self.conf['deeplink']['category'])

            api_large_list = []
            response = requests.get('https://recommend-api.29cm.co.kr/api/v5/best/categories/groups')
            if response.status_code == 200:
                large_category_data = response.json()
                # api에서 호출한 대 카테고리 리스트 저장
                for i in range(0, len(large_category_data['data'])):
                    api_large_category = large_category_data['data'][i]['categoryName']
                    api_large_list.append(api_large_category)
                print(api_large_list)

                # api에서 호출한 리스트 길이와 비교하여 노출되는 대 카테고리 리스트 저장
                large_list = []
                for i in range(0, 3):
                    if len(large_list) < len(large_category_data['data']):
                        # 대 카테고리 리스트 저장
                        large_category = wd.find_elements(AppiumBy.ACCESSIBILITY_ID, 'large_category')
                        for large in large_category:
                            large_category_text = large.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text
                            if large_category_text not in large_list:
                                large_list.append(large_category_text)
                    else:
                        break
                    # 대 카테고리 영역 스크롤 동작
                    large_field = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'large_category_list')
                    com_utils.element_control.element_scroll_control(wd, large_field, 'D', 30)
                print(large_list)

                if api_large_list == large_list:
                    print('대 카테고리 리스트 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('카테고리 리스트 확인 실패')
                    print('대 카테고리 리스트 확인 실패')
            else:
                print('PDP 옵션 정보 API 불러오기 실패')

            # 대 카테고리, 중 카테고리 코드 번호 저장
            large_category_info = com_utils.api_control.large_category_info(self.conf["category_group"][0],
                                                                            self.conf["large_category"][0])
            large_category_code = large_category_info[0]
            large_category_name = large_category_info[1]
            medium_category_code = com_utils.api_control.medium_category_code(large_category_code,
                                                                              self.conf["medium_category"][0])
            print(f'{large_category_code}/{large_category_name}/{medium_category_code}')

            # 대 카테고리 리스트 상단으로 스크롤
            large_field = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'large_category_list')
            com_utils.element_control.element_scroll_control(wd, large_field, 'U', 30)

            # 신발 > 여성 > 전체 순으로 카테고리 선택
            wd.find_element(AppiumBy.XPATH,
                            f'//XCUIElementTypeButton[@name="{self.conf["large_category"][0]}"]').click()
            wd.find_element(AppiumBy.XPATH,
                            f'//XCUIElementTypeButton[@name="{self.conf["category_group"][0]}"]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '전체').click()

            # 타이틀명으로 카테고리 전체 페이지 진입 확인
            # API (large_category_info)에서 받아온 카테고리명으로 확인
            try:
                wd.find_element(AppiumBy.XPATH, f'//XCUIElementTypeButton[@name="{large_category_name}"]')
                print('카테고리 전체 페이지 진입 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('카테고리 전체 페이지 진입 확인 실패')
                print('WARN : 카테고리 전체 페이지 진입 확인 실패')

            # 카테고리 전체 리스트의 첫번째 상품 확인
            # 해당 영역 WEBVIEW Element 잡히지 않아 추후 업데이트 필요

            # 중 카테고리 : 샌들 선택
            wd.find_element(AppiumBy.XPATH, f'//XCUIElementTypeButton[@name="{large_category_name}"]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, self.conf["medium_category"][0]).click()

            sleep(3)

            # 타이틀명으로 중 카테고리 페이지 진입 확인
            try:
                wd.find_element(AppiumBy.XPATH, f'//XCUIElementTypeButton[@name="{self.conf["medium_category"][0]}"]')
                print('중 카테고리 페이지 진입 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('중 카테고리 페이지 진입 확인 실패')
                print('WARN: 중 카테고리 페이지 진입 확인 실패')

            # 정렬 신상품 순으로 변경
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'sort_filter').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "신상품순"`]').click()

            # 선택한 대 -> 중 카테고리에 해당하는 PLP API 호출
            response = requests.get(
                f'https://search-api.29cm.co.kr/api/v4/products/category?categoryLargeCode={large_category_code}&categoryMediumCode={medium_category_code}&count=50&sort=new')
            category_1st_item = ''
            if response.status_code == 200:
                category_list_data = response.json()
                category_1st_item = category_list_data['data']['products'][0]['itemName']
                print(category_1st_item)

                # 카테고리 페이지에 첫번째 아이템 노출 확인
                for i in range(0, 5):
                    category_product = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'product_name').text
                    if category_product == category_1st_item:
                        print('카테고리 페이지의 상품 확인')
                        break
                    else:
                        print('카테고리 페이지의 상품 확인 안되어 스크롤')
                        com_utils.element_control.scroll_control(wd, 'D', 50)
            else:
                test_result = 'WARN'
                warning_texts.append('피드 컨텐츠 API 불러오기 실패')
                print('WARN: 피드 컨텐츠 API 불러오기 실패')

            # 카테고리 페이지의 첫번째 아이템 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'product_name').click()
            sleep(3)

            # PDP 상품 이름 저장
            pdp_web = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView')
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'Select a slide to show')
                pdp_name = pdp_web.find_element(AppiumBy.XPATH,
                                                '//XCUIElementTypeOther[@index="5"]/XCUIElementTypeStaticText').get_attribute('name')
            except NoSuchElementException:
                pdp_name = pdp_web.find_element(AppiumBy.XPATH,
                                                '//XCUIElementTypeOther[@index="4"]/XCUIElementTypeStaticText').get_attribute('name')

            # 선택한 상품의 PDP에서 상품 이름 비교
            if pdp_name in category_1st_item:
                print('PDP 진입 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('PDP 진입 확인 실패')
                print(f'WARN: PDP 진입 확인 실패 : {category_1st_item} / {pdp_name}')

            # PDP 상단 네비게이션의 Home 아이콘 선택하여 Home 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common home icon black').click()

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
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def test_welove(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 카테고리 탭 선택
            wd.get(self.conf['deeplink']['category'])

            # 핀메뉴에서 위러브 페이지 진입
            category_page.click_pin_menu(wd, 'WELOVE')

            post_title = welove_page.save_first_post_title(wd)

            # 첫번째 포스트의 첫번째 해시태그 저장 후 선택
            post_hash_tag = welove_page.save_first_post_hashtag(wd)
            welove_page.click_first_post_hashtag(wd)

            # 해시태그 페이지 타이틀과 저장한 해시태그 비교 확인
            test_result = welove_page.check_hash_tag_title(wd, warning_texts, post_hash_tag)

            # welove 페이지에서 저장한 포스트가 해시태그 페이지에 노출되는지 확인
            test_result = welove_page.check_hash_tag_post(wd, warning_texts, post_title)

            # welove 페이지로 복귀
            welove_page.click_hash_tag_back_btn(wd)

            # 포스트 추가 노출 확인
            test_result = welove_page.find_and_save_third_post(wd, warning_texts)

            # Home으로 복귀
            welove_page.click_welove_back_btn(wd)
            navigation_bar.move_to_home(wd)

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
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data
