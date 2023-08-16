import os
import sys
import traceback

from time import time, sleep

import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils import values_control

import com_utils.element_control


class Search:
    def test_search_popular_brand(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # SEARCH 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "SEARCH"`]').click()

            # 전체 기준 인기검색어 리스트 호출
            response = requests.get('https://search-api.29cm.co.kr/api/v4/keyword/popular?limit=100&brandLimit=30')
            if response.status_code == 200:
                all_popular_data = response.json()
                all_popular_brand_30th = all_popular_data['data']['popularBrandKeywords'][29]

                # 인기 브랜드 타이틀 확인
                try:
                    wd.find_element(AppiumBy.ACCESSIBILITY_ID, '지금 많이 찾는 브랜드')
                    print('인기 브랜드 타이틀 확인')
                except NoSuchElementException:
                    test_result = 'WARN'
                    warning_texts.append('인기 브랜드 타이틀 확인 실패')
                    print('인기 브랜드 타이틀 확인 실패')

                # 인기 브랜드 30위 확인
                popular_brand = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView[@index="2"]')
                com_utils.element_control.swipe_control(wd, popular_brand, 'left', 30)
                com_utils.element_control.swipe_control(wd, popular_brand, 'left', 30)

                popular_brand_30th = popular_brand.find_element(AppiumBy.XPATH,
                                                                '//XCUIElementTypeCell[@index="9"]/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="1"]')
                popular_brand_30th_name = popular_brand_30th.text

                # API 호출한 인기브랜드 30위와 실제 30위가 동일한지 확인
                if all_popular_brand_30th == popular_brand_30th_name:
                    print('인기 브랜드 순위 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('인기 브랜드 순위 확인 실패')
                    print('인기 브랜드 순위 확인 실패')

                # 인기 브랜드 30위 검색
                popular_brand_30th.click()

                # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
                search_result_brand = wd.find_element(AppiumBy.XPATH,
                                                      '//XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="0"]')
                if popular_brand_30th_name in search_result_brand.text:
                    print('인기 브랜드 검색 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('인기 브랜드 검색 확인 실패')
                    print('인기 브랜드 검색 확인 실패')
            else:
                print('인기 검색어 API 호출 실패')

            # 검색 화면으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()

            # 최근 검색어 모두 지우기
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`label == "모두 지우기"`]').click()

            # 필터 영역 선택하여 필터 변경 -> 여성, 30~34세 기준으로 변경
            brand_filter = wd.find_element(AppiumBy.XPATH,
                                           '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeOther[@index="0"]/XCUIElementTypeButton')
            brand_filter.click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            f'**/XCUIElementTypeButton[`label == "{self.conf["search_filter_gender"][1]}"`]').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            f'**/XCUIElementTypeButton[`label == "{self.conf["search_filter_age"][1]}"`]').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "적용하기"`]').click()

            # 변경된 필터 기준
            response = requests.get('https://search-api.29cm.co.kr/api/v4/keyword/popular?limit=100&brandLimit=30&group=female&ageGroup=30to34')
            if response.status_code == 200:
                filter_popular_data = response.json()
                filter_popular_brand_10th = filter_popular_data['data']['popularBrandKeywords'][9]

                # 필터 기준 문구 변경 확인
                if brand_filter.text == '여성 30~34세 기준':
                    print('필터 적용 확인 - 필터 기준 문구')
                else:
                    test_result = 'WARN'
                    warning_texts.append('필터 적용 확인 실패')
                    print(f'필터 적용 확인 실패 : {brand_filter.text}')

                # 변경된 기준의 인기브랜드 10위 확인
                popular_brand_10th = popular_brand.find_element(AppiumBy.XPATH,
                                                                '//XCUIElementTypeCell[@index="9"]/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="1"]')
                if filter_popular_brand_10th == popular_brand_10th.text:
                    print('필터 적용 확인 - 필터 기준 10위')
                else:
                    test_result = 'WARN'
                    warning_texts.append('필터 적용 확인 실패')
                    print(f'필터 적용 확인 실패 : {filter_popular_brand_10th} / {popular_brand_10th.text}')
            else:
                print('인기 검색어 필터 API 호출 실패')

            # 필터를 전체 기준으로 재변경
            brand_filter.click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            f'**/XCUIElementTypeButton[`label == "{self.conf["search_filter_gender"][0]}"`][1]').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            f'**/XCUIElementTypeButton[`label == "{self.conf["search_filter_age"][0]}"`][2]').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "적용하기"`]').click()

            # 뒤로가기
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()

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