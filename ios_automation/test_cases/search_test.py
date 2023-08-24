import os
import sys
import traceback
import requests
import com_utils.element_control

from com_utils import values_control
from time import time, sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


class Search:
    def test_search_popular_brand(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # SEARCH 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "SEARCH"`]').click()

            all_popular_brand_1st = ''
            all_popular_brand_30th = ''
            # 전체 기준 인기검색어 리스트 호출
            response = requests.get('https://search-api.29cm.co.kr/api/v4/keyword/popular?limit=100&brandLimit=30')
            if response.status_code == 200:
                all_popular_data = response.json()
                all_popular_brand_1st = all_popular_data['data']['popularBrandKeywords'][0]
                all_popular_brand_30th = all_popular_data['data']['popularBrandKeywords'][29]
                print(f'1위: {all_popular_brand_1st} / 30위: {all_popular_brand_30th}')
            else:
                print('인기 검색어 API 호출 실패')

            # 인기 브랜드 타이틀 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '지금 많이 찾는 브랜드')
                print('인기 브랜드 타이틀 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 타이틀 확인 실패')
                print('인기 브랜드 타이틀 확인 실패')

            # 인기 브랜드 1위 확인
            popular_brand = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView[@index="2"]')
            popular_brand_1st = popular_brand.find_element(AppiumBy.XPATH,
                                                           '//XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="1"]')
            popular_brand_1st_name = popular_brand_1st.text

            # API 호출한 인기 브랜드 1위와 실제 1위가 동일한 지 확인 후 선택
            if all_popular_brand_1st == popular_brand_1st_name:
                popular_brand_1st.click()
                print('인기 브랜드 1위 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 1위 확인 실패')
                print('인기 브랜드 1위 확인 실패')

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            relate_brand = wd.find_element(AppiumBy.XPATH,
                                           '//XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeCollectionView')
            relate_brand_name = relate_brand.find_element(AppiumBy.XPATH,
                                                          '//XCUIElementTypeStaticText[@index="0"]').text
            if popular_brand_1st_name in relate_brand_name:
                print(f'인기 브랜드 검색 확인: {relate_brand_name}')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 확인 실패')
                print('인기 브랜드 검색 확인 실패')

            # 검색 결과 첫번째 상품의 브랜드명과 1위 브랜드명 비교
            product_1st = wd.find_element(AppiumBy.XPATH,
                                          '//XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView[@index="1"]/XCUIElementTypeCell[@index="3"]')
            product_brand = product_1st.find_element(AppiumBy.XPATH,
                                                     '//XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="0"]').text

            if popular_brand_1st_name == product_brand:
                print('인기 브랜드 검색 상품 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 상품 확인 실패')
                print(f'인기 브랜드 검색 상품 확인 실패: {popular_brand_1st_name} / {product_brand}')

            # 검색 화면으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()

            # 인기 브랜드 30위 확인
            popular_brand = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView[@index="2"]')
            com_utils.element_control.swipe_control(wd, popular_brand, 'left', 30)
            com_utils.element_control.swipe_control(wd, popular_brand, 'left', 30)

            popular_brand_30th = popular_brand.find_element(AppiumBy.XPATH,
                                                            '//XCUIElementTypeCell[@index="9"]/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="1"]')
            popular_brand_30th_name = popular_brand_30th.text

            # API 호출한 인기브랜드 30위와 실제 30위가 동일한지 확인 후 선택
            if all_popular_brand_30th == popular_brand_30th_name:
                popular_brand_30th.click()
                print('인기 브랜드 30위 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 30위 확인 실패')
                print('인기 브랜드 30위 확인 실패')

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            relate_brand = wd.find_element(AppiumBy.XPATH,
                                           '//XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeCollectionView')
            relate_brand_name = relate_brand.find_element(AppiumBy.XPATH,
                                                          '//XCUIElementTypeStaticText[@index="0"]').text
            if popular_brand_30th_name in relate_brand_name:
                print(f'인기 브랜드 검색 확인: {relate_brand_name}')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 확인 실패')
                print('인기 브랜드 검색 확인 실패')

            # 검색 화면으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()

            # 최근 검색어 모두 지우기
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`label == "모두 지우기"`]').click()

            # 필터 영역 선택하여 필터 변경 -> 여성, 30~34세 기준으로 변경
            filter = wd.find_element(AppiumBy.XPATH,
                                     '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="0"]')
            brand_filter = filter.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton')
            brand_filter.click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            f'**/XCUIElementTypeButton[`label == "{self.conf["search_filter_gender"]["WOMEN"]}"`]').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            f'**/XCUIElementTypeButton[`label == "{self.conf["search_filter_age"]["30to34"]}"`]').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "적용하기"`]').click()

            # 변경된 필터 기준
            response = requests.get(
                'https://search-api.29cm.co.kr/api/v4/keyword/popular?limit=100&brandLimit=30&group=female&ageGroup=30to34')
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
                            f'**/XCUIElementTypeButton[`label == "{self.conf["search_filter_gender"]["ALL"]}"`][1]').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            f'**/XCUIElementTypeButton[`label == "{self.conf["search_filter_age"]["ALL"]}"`][2]').click()
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

    def test_search_popular_keyword(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # SEARCH 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "SEARCH"`]').click()

            popluar_keyword_1st = ''
            popluar_keyword_25th = ''
            # 전체 기준 인기검색어 리스트 호출
            response = requests.get('https://search-api.29cm.co.kr/api/v4/keyword/popular?limit=100&brandLimit=30')
            if response.status_code == 200:
                all_popular_data = response.json()
                popluar_keyword_1st = all_popular_data['data']['popularKeyword'][0]
                popluar_keyword_25th = all_popular_data['data']['popularKeyword'][24]
                print(f'1위: {popluar_keyword_1st} / 25위: {popluar_keyword_25th}')
            else:
                print('인기 검색어 API 호출 실패')

            # 인기 브랜드 타이틀 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '지금 많이 찾는 검색어')
                print('인기 검색어 타이틀 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('인기 검색어 타이틀 확인 실패')
                print('인기 검색어 타이틀 확인 실패')

            # 인기 검색어 1위 검색어 선택 / 동일 검색어 2개일 경우와 1개일 경우 분리
            try:
                wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                                f'**/XCUIElementTypeStaticText[`label == "{popluar_keyword_1st}"`][2]').click()
            except NoSuchElementException:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, popluar_keyword_1st).click()

            # 연관 검색어 API 호출
            response = requests.get(
                f'https://search-api.29cm.co.kr/api/v4/keyword/related?keyword={popluar_keyword_1st}')
            if response.status_code == 200:
                relate_keyword_data = response.json()
                relate_keyword_list = relate_keyword_data['data']['relatedKeywords']

                # 연관 검색어 없을 경우, 검색 필드 확인 / 있을 경우, 첫번째 연관 검색어 확인
                if not relate_keyword_list:
                    print('연관 검색어 없음')
                    search_input_field = wd.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextField').text
                    if search_input_field == popluar_keyword_1st:
                        print('인기 검색어 검색 확인 - 입력란')
                    else:
                        test_result = 'WARN'
                        warning_texts.append('인기 브랜드 검색 결과 확인 실패')
                        print(f'인기 브랜드 검색 결과 확인 실패 : {popluar_keyword_1st} / {search_input_field}')
                else:
                    print('연관 검색어 있음')
                    relate_keyword = relate_keyword_list[0]
                    relate = wd.find_element(AppiumBy.XPATH,
                                             '//XCUIElementTypeCollectionView[@index="1"]/XCUIElementTypeCell/XCUIElementTypeCollectionView')
                    relate_1st = relate.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton').get_attribute('name')
                    if relate_keyword == relate_1st:
                        print('인기 검색어 검색 확인 - 연관 검색어')
                    else:
                        test_result = 'WARN'
                        warning_texts.append('인기 브랜드 검색 결과 확인 실패')
                        print(f'인기 브랜드 검색 결과 확인 실패 : {relate_1st} / {relate_keyword}')
            else:
                print('연관 검색어 API 호출 실패')

            # 검색 화면으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()

            # 최근 검색어에 최근에 선택한 검색어 노출 여부 확인
            recent_keyword = wd.find_element(AppiumBy.XPATH,
                                             '//XCUIElementTypeCollectionView[@index="1"]/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="0"]')
            if popluar_keyword_1st == recent_keyword.text:
                print('최근 검색어 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('최근 검색어 노출 확인 실패')
                print('최근 검색어 노출 확인 실패')

            # 최근 검색어 모두 지우기
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            '**/XCUIElementTypeStaticText[`label == "모두 지우기"`]').click()

            # 인기 검색어 25위 확인
            for i in range(0, 10):
                try:
                    wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`label == "25"`]')
                    try:
                        wd.find_element(AppiumBy.ACCESSIBILITY_ID, popluar_keyword_25th)
                        print('인기 검색어 순위 확인')
                        break
                    except NoSuchElementException:
                        test_result = 'WARN'
                        warning_texts.append('인기 검색어 순위 확인 실패')
                        print('인기 검색어 순위 확인 실패')
                except NoSuchElementException:
                    com_utils.element_control.scroll_control(wd, "D", 60)

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

    def test_search_results_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # SEARCH 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "SEARCH"`]').click()

            # 니트 검색
            wd.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextField').send_keys(self.conf["keyword"]["knit"])
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarSearchBlack').click()

            # 검색 결과 화면의 입력란의 검색어 확인
            search_input_field = wd.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextField').text
            if search_input_field == self.conf["keyword"]['knit']:
                print('인기 검색어 검색 확인 - 입력란')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 결과 확인 실패')
                print(f'인기 브랜드 검색 결과 확인 실패 : {search_input_field}')

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            relate_brand = wd.find_element(AppiumBy.XPATH,
                                           '//XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeCollectionView')
            relate_brand_name = relate_brand.find_element(AppiumBy.XPATH,
                                                          '//XCUIElementTypeStaticText[@index="0"]').text
            if self.conf["keyword"]['knit'] in relate_brand_name:
                print(f'인기 브랜드 검색 확인 - 브랜드명: {relate_brand_name}')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 확인 실패')
                print(f'인기 브랜드 검색 확인 실패 - 브랜드명: {relate_brand_name}')

            # 정렬 판매순으로 변경
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '추천순').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            f'**/XCUIElementTypeButton[`label == "{self.conf["sort"]["order"]}"`]').click()
            print('정렬 : 판매순 선택')

            # 색상 필터 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '색상').click()

            # 색상 블랙 선택
            for i in range(0, 3):
                try:
                    wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                                    f'**/XCUIElementTypeButton[`label == "{self.conf["search_filter"]["black"]}"`]').click()
                    print('필터 - 색상 : 블랙 선택')
                    break
                except NoSuchElementException:
                    color_sheet = wd.find_element(AppiumBy.IOS_PREDICATE, 'type == "XCUIElementTypeScrollView"')
                    com_utils.element_control.element_scroll_control(wd, color_sheet, "D", 25)

            # 카테고리 여성의류 선택
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`label == "카테고리"`]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, self.conf["search_filter"]["woman_clothes"]).click()
            print('필터 - 카테고리 : 여성의류 선택')

            # 상품정보 품절상품 제외 선택
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`label == "상품정보"`]').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            f'**/XCUIElementTypeStaticText[`label == "{self.conf["search_filter"]["excludingout_of_stock_products"]}"`]').click()
            print('필터 - 상품정보 : 품절상품 제외 선택')

            # 필터 적용
            bottom_sheet = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWindow/XCUIElementTypeOther[@index="1"]')
            bottom_sheet.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@index="5"]').click()

            sleep(2)

            # 필터 element 확인
            plp_view = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView[@index="1"]')
            filter_view = plp_view.find_element(AppiumBy.XPATH,
                                                '//XCUIElementTypeOther/XCUIElementTypeCollectionView[@index="2"]')

            # 적용된 필터 확인
            filter_list = []
            for i in range(0, 2):
                filters = filter_view.find_elements(AppiumBy.XPATH,
                                                    '//XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeStaticText')
                for filter_text in filters:
                    filter_name = filter_text.text
                    filter_list.append(filter_name)
                com_utils.element_control.swipe_control(wd, filter_view, "left", 30)

            filter_check = [self.conf["search_filter"]["black"], self.conf["search_filter"]["woman_clothes"],
                            self.conf["search_filter"]["excludingout_of_stock_products"]]
            for filter in filter_check:
                if filter in set(filter_list):
                    print(f'{filter} 필터 적용 확인')
                else:
                    print(f'{filter} 필터 적용 확인 실패: {set(filter_list)}')

            sleep(2)

            # 검색 화면으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()

            # 최근 검색어에 최근에 선택한 검색어 노출 여부 확인
            recent_keyword = wd.find_element(AppiumBy.XPATH,
                                             '//XCUIElementTypeCollectionView[@index="1"]/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="0"]')
            if self.conf["keyword"]['knit'] == recent_keyword.text:
                print('최근 검색어 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('최근 검색어 노출 확인 실패')
                print('최근 검색어 노출 확인 실패')

            # 최근 검색어 모두 지우기
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            '**/XCUIElementTypeStaticText[`label == "모두 지우기"`]').click()
            print('최근 검색어 모두 지우기')

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
