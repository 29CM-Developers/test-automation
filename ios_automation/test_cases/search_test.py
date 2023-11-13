import os
import sys
import traceback
import requests
import com_utils.element_control

from com_utils import values_control
from time import time, sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc


def clear_recent_keyword(wd):
    try:
        ial(wd, '//XCUIElementTypeOther[@name="recent_keyword"]')
        ialc(wd, '//XCUIElementTypeButton[@name="모두 지우기"]')
    except NoSuchElementException:
        pass


class Search:

    def test_search_popular_brand(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # SEARCH 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "SEARCH"`]').click()

            first_brand_category_name = ''
            api_1st_brand = ''
            api_30th_brand = ''
            # 전체 기준 인기검색어 리스트 호출
            response = requests.get(
                'https://search-api.29cm.co.kr/api/v4/popular?gender=all&keywordLimit=100&brandLimit=30')
            if response.status_code == 200:
                brand_data = response.json()
                first_brand_category = brand_data['data']['brand']['results'][0]
                first_brand_category_name = first_brand_category['categoryName']
                api_1st_brand = first_brand_category['keywords'][0]['keyword']
                api_30th_brand = first_brand_category['keywords'][29]['keyword']
                print(f'첫번째 브랜드 카테고리 : {first_brand_category_name}')
                print(f'1위 : {api_1st_brand} / 30위 : {api_30th_brand}')
            else:
                print('인기 검색어 API 호출 실패')

            # 첫번째 인기 브랜드 카테고리 확인
            brand_category_name = wd.find_element(AppiumBy.XPATH,
                                                  '//XCUIElementTypeStaticText[@name="first_popular_brand_title"]').text
            if f'지금 많이 찾는 {first_brand_category_name} 브랜드' in brand_category_name:
                print('인기 브랜드 타이틀 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 타이틀 확인 실패')
                print('인기 브랜드 타이틀 확인 실패')

            # 필터가 전체 기준인지 확인
            filter_btn = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'keyword_filter')
            if filter_btn.text == '전체 기준':
                print('필터 : 전체 기준')
                pass
            else:
                print(f'필터 : 전체 기준이 아님 / {filter_btn.text}')
                filter_btn.click()
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'gender_filter_all').click()

            # 인기 브랜드 1위 확인
            brand_1st = wd.find_element(AppiumBy.XPATH,
                                        '(//XCUIElementTypeOther[@name="first_popular_brand_name"])[1]')
            brand_1st_name = brand_1st.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text

            # API 호출한 인기 브랜드 1위와 실제 1위가 동일한 지 확인 후 선택
            if api_1st_brand == brand_1st_name:
                brand_1st.click()
                print('인기 브랜드 1위 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 1위 확인 실패')
                print('인기 브랜드 1위 확인 실패')

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            relate_brand_name = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'releate_brand_name').text
            if brand_1st_name in relate_brand_name:
                print(f'인기 브랜드 검색 확인: {relate_brand_name}')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 확인 실패')
                print('인기 브랜드 검색 확인 실패')

            # 검색 결과 첫번째 상품의 브랜드명과 1위 브랜드명 비교
            product_brand = wd.find_elements(AppiumBy.ACCESSIBILITY_ID, 'brand_name')
            product_brand_name = product_brand[0].text

            if brand_1st_name == product_brand_name:
                print('인기 브랜드 검색 상품 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 상품 확인 실패')
                print(f'인기 브랜드 검색 상품 확인 실패: {brand_1st_name} / {product_brand_name}')

            # 검색 화면으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_back_btn').click()

            # 인기 브랜드 30위 확인
            popular_brand = wd.find_element(AppiumBy.XPATH,
                                            '//XCUIElementTypeCollectionView[@name="first_popular_brand_list"]')
            com_utils.element_control.swipe_control(wd, popular_brand, 'left', 30)
            com_utils.element_control.swipe_control(wd, popular_brand, 'left', 30)
            com_utils.element_control.swipe_control(wd, popular_brand, 'left', 30)
            com_utils.element_control.swipe_control(wd, popular_brand, 'left', 30)

            brand_30th = popular_brand.find_element(AppiumBy.XPATH,
                                                    '(//XCUIElementTypeOther[@name="first_popular_brand_name"])[6]')
            brand_30th_name = brand_30th.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text

            # API 호출한 인기브랜드 30위와 실제 30위가 동일한지 확인 후 선택
            if api_30th_brand == brand_30th_name:
                brand_30th.click()
                print('인기 브랜드 30위 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 30위 확인 실패')
                print(f'인기 브랜드 30위 확인 실패 : {api_30th_brand} / {brand_30th_name}')

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            relate_brand_name = wd.find_elements(AppiumBy.XPATH,
                                                 '//XCUIElementTypeStaticText[@name="releate_brand_name"]')
            brand_find = False
            for brand_name in relate_brand_name:
                relate_name = brand_name.text
                print(relate_name)
                if brand_30th_name in relate_name:
                    brand_find = True
                    print('인기 브랜드 검색 확인')
                    break
                else:
                    pass
            if not brand_find:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 확인 실패')
                print(f'인기 브랜드 검색 확인 실패')

            # 검색 화면으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_back_btn').click()

            # 최근 검색어 모두 지우기
            clear_recent_keyword(wd)

            # 필터 영역 선택하여 필터 변경 -> 여성 기준으로 변경
            brand_filter = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'keyword_filter')
            brand_filter.click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'gender_filter_female').click()

            # 변경된 필터 기준
            response = requests.get(
                'https://search-api.29cm.co.kr/api/v4/popular?gender=female&keywordLimit=100&brandLimit=30')
            if response.status_code == 200:
                filter_popular_brand_data = response.json()
                filter_brand_list = filter_popular_brand_data['data']['brand']['results'][0]
                filter_popular_1st_brand = filter_brand_list['keywords'][0]['keyword']

                # 필터 기준 문구 변경 확인
                if brand_filter.text == '여성 기준':
                    print('필터 적용 확인 - 필터 기준 문구')
                else:
                    test_result = 'WARN'
                    warning_texts.append('필터 적용 확인 실패')
                    print(f'필터 적용 확인 실패 : {brand_filter.text}')

                # 변경된 기준의 인기브랜드 1위 확인
                filter_1st_brand = wd.find_element(AppiumBy.XPATH,
                                                   '(//XCUIElementTypeOther[@name="first_popular_brand_name"])[1]')
                filter_1st_brand_name = filter_1st_brand.find_element(AppiumBy.XPATH,
                                                                      '//XCUIElementTypeStaticText').text

                if filter_popular_1st_brand == filter_1st_brand_name:
                    print('필터 적용 확인 - 필터 기준 1위 브랜드')
                else:
                    test_result = 'WARN'
                    warning_texts.append('필터 적용 확인 실패')
                    print(f'필터 적용 확인 실패 : {filter_popular_1st_brand} / {filter_1st_brand_name}')
            else:
                print('인기 검색어 필터 API 호출 실패')

            # 필터를 전체 기준으로 재변경
            brand_filter = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'keyword_filter')
            brand_filter.click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'gender_filter_all').click()

            # 뒤로가기
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_back_btn').click()

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

    def test_search_popular_keyword(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # SEARCH 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "SEARCH"`]').click()

            api_keyword_1st = ''
            api_keyword_25th = ''
            # 전체 기준 인기검색어 리스트 호출
            response = requests.get(
                'https://search-api.29cm.co.kr/api/v4/popular?gender=all&keywordLimit=100&brandLimit=30')
            if response.status_code == 200:
                keyword_data = response.json()
                keyword_list = keyword_data['data']['keyword']['results'][0]
                api_keyword_1st = keyword_list['keywords'][0]['keyword']
                api_keyword_25th = keyword_list['keywords'][24]['keyword']
                print(f'1위: {api_keyword_1st} / 25위: {api_keyword_25th}')
            else:
                print('인기 검색어 API 호출 실패')

            # 인기 브랜드 타이틀 확인
            for i in range(0, 3):
                try:
                    keyword_title = wd.find_element(AppiumBy.ACCESSIBILITY_ID, '지금 많이 찾는 검색어')
                    if keyword_title.is_displayed():
                        print('인기 검색어 타이틀 확인')
                        break
                    else:
                        print('인기 검색어 타이틀 확인 안되어 스크롤')
                        com_utils.element_control.scroll_control(wd, 'D', 50)
                except NoSuchElementException:
                    com_utils.element_control.scroll_control(wd, 'D', 50)
            else:
                test_result = 'WARN'
                warning_texts.append('인기 검색어 타이틀 확인 실패')
                print('인기 검색어 타이틀 확인 실패')

            # 인기 검색어 1위 검색어 선택
            wd.find_element(AppiumBy.XPATH, '////XCUIElementTypeOther[@name="popular_keyword"]').click()

            # 연관 검색어 API 호출
            response = requests.get(
                f'https://search-api.29cm.co.kr/api/v4/keyword/related?keyword={api_keyword_1st}')
            if response.status_code == 200:
                relate_keyword_data = response.json()
                relate_keyword_list = relate_keyword_data['data']['relatedKeywords']

                # 연관 검색어 없을 경우, 검색 필드 확인 / 있을 경우, 첫번째 연관 검색어 확인
                if not relate_keyword_list:
                    print('연관 검색어 없음')
                    search_input_field = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'input_keyword').text
                    if search_input_field == api_keyword_1st:
                        print('인기 검색어 검색 확인 - 입력란')
                    else:
                        test_result = 'WARN'
                        warning_texts.append('인기 브랜드 검색 결과 확인 실패')
                        print(f'인기 브랜드 검색 결과 확인 실패 : {api_keyword_1st} / {search_input_field}')
                else:
                    print('연관 검색어 있음')
                    relate_keyword_api = relate_keyword_list[0]
                    relate_keyword = wd.find_elements(AppiumBy.ACCESSIBILITY_ID, 'related_keyword')[0]
                    relate_keyword_1st = relate_keyword.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text
                    if relate_keyword_api == relate_keyword_1st:
                        print('인기 검색어 검색 확인 - 연관 검색어')
                    else:
                        test_result = 'WARN'
                        warning_texts.append('인기 브랜드 검색 결과 확인 실패')
                        print(f'인기 브랜드 검색 결과 확인 실패 : {relate_keyword_1st} / {relate_keyword_api}')
            else:
                print('연관 검색어 API 호출 실패')

            # 검색 화면으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_back_btn').click()

            for i in range(0, 3):
                try:
                    wd.find_element(AppiumBy.ACCESSIBILITY_ID, '최근 검색어')
                except NoSuchElementException:
                    com_utils.element_control.scroll_control(wd, "U", 50)

            # 최근 검색어에 최근에 선택한 검색어 노출 여부 확인
            recent_keyword = wd.find_element(AppiumBy.XPATH,
                                             '//XCUIElementTypeOther[@name="recent_keyword"]/XCUIElementTypeStaticText')
            if api_keyword_1st == recent_keyword.text:
                print('최근 검색어 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('최근 검색어 노출 확인 실패')
                print('최근 검색어 노출 확인 실패')

            # 최근 검색어 모두 지우기
            clear_recent_keyword(wd)

            # 인기 검색어 25위 확인
            rank_break = False
            for i in range(0, 10):
                try:
                    keyword_rank = wd.find_elements(AppiumBy.XPATH,
                                                    '//XCUIElementTypeOther[@name="popular_keyword_rank"]/XCUIElementTypeStaticText')
                    for rank in keyword_rank:
                        if rank.text == "25":
                            rank_break = True
                            wd.find_element(AppiumBy.ACCESSIBILITY_ID, api_keyword_25th)
                            print('인기 검색어 순위 확인')
                            break
                    if rank_break:
                        break
                    com_utils.element_control.scroll_control(wd, "D", 60)
                except NoSuchElementException:
                    test_result = 'WARN'
                    warning_texts.append('인기 검색어 순위 확인 실패')
                    print('인기 검색어 순위 확인 실패')

            # 뒤로가기
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_back_btn').click()

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

    def test_search_results_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # SEARCH 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "SEARCH"`]').click()

            # 니트 검색
            wd.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextField').send_keys(self.conf["keyword"]["knit"])
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'search_btn').click()

            # 검색 결과 화면의 입력란의 검색어 확인
            search_input_field = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'input_keyword').text
            if search_input_field == self.conf["keyword"]['knit']:
                print('인기 검색어 검색 확인 - 입력란')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 결과 확인 실패')
                print(f'인기 브랜드 검색 결과 확인 실패 : {search_input_field}')

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            relate_brand_name = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'releate_brand_name').text
            if self.conf["keyword"]['knit'] in relate_brand_name:
                print(f'인기 브랜드 검색 확인 - 브랜드명: {relate_brand_name}')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 확인 실패')
                print(f'인기 브랜드 검색 확인 실패 - 브랜드명: {relate_brand_name}')

            # 정렬 판매순으로 변경
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'sort_filter').click()
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            f'**/XCUIElementTypeButton[`label == "{self.conf["sort"]["order"]}"`]').click()
            print('정렬 : 판매순 선택')

            # 색상 필터 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'color_filter').click()

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
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'filter_apply_btn').click()

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
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_back_btn').click()

            # 최근 검색어에 최근에 선택한 검색어 노출 여부 확인
            recent_keyword = wd.find_element(AppiumBy.XPATH,
                                             '//XCUIElementTypeOther[@name="recent_keyword"]/XCUIElementTypeStaticText')
            if self.conf["keyword"]['knit'] == recent_keyword.text:
                print('최근 검색어 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('최근 검색어 노출 확인 실패')
                print('최근 검색어 노출 확인 실패')

            # 최근 검색어 모두 지우기
            clear_recent_keyword(wd)

            # 뒤로가기
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_back_btn').click()

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
