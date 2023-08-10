import os
import sys
import traceback
import requests

from time import time, sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils import values_control


class Category:
    def test_category_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        print(f'[{test_name}] 테스트 시작')

        try:
            # 카테고리 탭 선택
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="CATEGORY"]').click()

            category_group = 'WOMEN'
            large_category = '신발'
            medium_category = '샌들'

            # 대 카테고리, 중 카테고리 코드 번호 저장
            large_category_list = Category.large_category_list(self, category_group, large_category)
            large_category_code = large_category_list[0]
            large_category_name = large_category_list[1]
            medium_category_code = Category.medium_category_code(self, large_category_code, medium_category)

            # 신발 > 여성 > 전체 순으로 카테고리 선택
            wd.find_element(AppiumBy.XPATH, f'//XCUIElementTypeButton[@name="{large_category}"]').click()
            wd.find_element(AppiumBy.XPATH, f'//XCUIElementTypeButton[@name="{category_group}"]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '전체').click()

            # 타이틀명으로 카테고리 전체 페이지 진입 확인
            # API (large_category_list)에서 받아온 카테고리명으로 확인
            try:
                wd.find_element(AppiumBy.XPATH, f'//XCUIElementTypeButton[@name="{large_category_name}"]')
                print('카테고리 전체 페이지 진입 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('카테고리 전체 페이지 진입 확인 실패')
                print('카테고리 전체 페이지 진입 확인 실패')

            # 카테고리 전체 리스트의 첫번째 상품 확인
            # 해당 영역 WEBVIEW Element 잡히지 않아 추후 업데이트 필요

            # 중 카테고리 : 샌들 선택
            wd.find_element(AppiumBy.XPATH, f'//XCUIElementTypeButton[@name="{large_category_name}"]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, medium_category).click()

            sleep(3)

            # 타이틀명으로 중 카테고리 페이지 진입 확인
            try:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="샌들"]')
                print('중 카테고리 페이지 진입 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('중 카테고리 페이지 진입 확인 실패')
                print('중 카테고리 페이지 진입 확인 실패')

            # 선택한 대 -> 중 카테고리에 해당하는 PLP API 호출
            response = requests.get(
                f'https://search-api.29cm.co.kr/api/v4/products/category?categoryLargeCode={large_category_code}&categoryMediumCode={medium_category_code}&count=50')
            category_1st_item = ''
            if response.status_code == 200:
                category_list_data = response.json()
                category_1st_item = category_list_data['data']['products'][0]['itemName']

                # 카테고리 페이지에 첫번째 아이템 노출 확인
                for i in range(0, 5):
                    try:
                        wd.find_element(AppiumBy.ACCESSIBILITY_ID, category_1st_item)
                        print('카테고리 페이지의 상품 확인')
                        break
                    except NoSuchElementException:
                        wd.execute_script('mobile:swipe', {'direction': 'up'})
                        print('카테고리 페이지의 상품 확인 안되어 스크롤')
            else:
                test_result = 'WARN'
                warning_texts.append('피드 컨텐츠 API 불러오기 실패')
                print('피드 컨텐츠 API 불러오기 실패')

            # 카테고리 페이지의 첫번째 아이템 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, category_1st_item).click()
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
                print(f'PDP 진입 확인 실패 : {category_1st_item} / {pdp_name}')

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
            wd.get('app29cm://home')

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def large_category_list(self, category, large_category_text):
        large_category_code = ''
        large_category_name = ''

        # 카테고리 그룹 API 호출
        response = requests.get('https://recommend-api.29cm.co.kr/api/v4/best/category-groups')
        if response.status_code == 200:
            category_group_data = response.json()
            category_group = category_group_data['data']

            # 찾고자 하는 카테고리 그룹의 아이템 리스트 확인
            for i in range(0, 2):
                category_group_name = category_group[i]['categoryGroupName']
                if category_group_name == category:
                    category_group_item_list = category_group[i]['categoryGroupItemList']
                    # 찾고자 하는 이름의 대 카테고리 코드 번호 저장
                    for v in range(0, 10):
                        category_item_group_name = category_group_item_list[v]['categoryGroupItemName']
                        if category_item_group_name == large_category_text:
                            large_category_code = category_group_item_list[v]['categoryCode']
                            large_category_name = category_group_item_list[v]['categoryName']
                            break
                        else:
                            pass
                else:
                    pass
        else:
            print('카테고리 그룹 API 호출 실패')

        return large_category_code, large_category_name

    def medium_category_code(self, large_category_code, medium_category_name):
        medium_category_code = ''

        # 대 카테고리의 하위 카테고리 API 호출
        response = requests.get(
            f'https://recommend-api.29cm.co.kr/api/v4/best/categories?categoryList={large_category_code}')
        if response.status_code == 200:
            medium_category_data = response.json()

            # 찾고자 하는 이름의 중 카테고리 코드 번호 저장
            for i in range(0, 10):
                category_name = medium_category_data['data'][i]['categoryName']
                if category_name == medium_category_name:
                    medium_category_code = medium_category_data['data'][i]['categoryCode']
                    break
                else:
                    pass
        else:
            print('중 카테고리 리스트 API 호출 실패')

        return medium_category_code
