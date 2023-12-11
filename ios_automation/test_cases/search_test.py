import os
import sys
import traceback
import com_utils.element_control

from com_utils import values_control
from time import time
from com_utils.testrail_api import send_test_result
from ios_automation.page_action import navigation_bar, search_page, search_result_page
from com_utils.api_control import search_total_popular_brand_name, search_woman_popular_brand_name, \
    search_popular_keyword


class Search:

    def test_search_popular_brand(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # SEARCH 탭 진입
            navigation_bar.move_to_search(wd)

            # 전체 기준 인기 브랜드 리스트 API 호출
            first_popular_brand = search_total_popular_brand_name()
            first_brand_category_name = first_popular_brand['category_name']
            api_1st_brand = first_popular_brand['api_1st_brand_name']
            api_30th_brand = first_popular_brand['api_30th_brand_name']

            # 첫번째 인기 브랜드 카테고리 확인
            search_page.check_first_popular_brand_category(wd, first_brand_category_name)

            # 필터가 전체 기준인지 확인
            search_page.change_criteria_to_all(wd)

            # 인기 브랜드 1위 이름 저장
            brand_1st_name = search_page.save_popular_brand_name(wd, '1')

            # 인기 브랜드 1위 확인
            search_page.check_popular_brand_name(api_1st_brand, brand_1st_name)

            # 인기 브랜드 1위 선택
            search_page.click_popular_brand_name(wd, 1)

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            search_result_page.check_relate_brand_name(wd, brand_1st_name)

            # 검색 결과 첫번째 상품의 브랜드명과 1위 브랜드명 비교
            search_result_page.check_product_brand_name(wd, brand_1st_name)

            # 검색 화면으로 복귀
            search_result_page.click_back_btn(wd)

            # 인기 브랜드 30위 확인
            search_page.swipe_brand_area(wd)
            search_page.swipe_brand_area(wd)
            search_page.swipe_brand_area(wd)
            search_page.swipe_brand_area(wd)

            # 인기 브랜드 30위 이름 저장
            brand_30th_name = search_page.save_popular_brand_name(wd, '6')

            # 인기 브랜드 30위 확인
            search_page.check_popular_brand_name(api_30th_brand, brand_30th_name)

            # 인기 브랜드 30위 선택
            search_page.click_popular_brand_name(wd, '6')

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            search_result_page.check_relate_brand_name(wd, brand_30th_name)

            # 검색 화면으로 복귀
            search_result_page.click_back_btn(wd)

            # 최근 검색어 모두 지우기
            search_page.clear_recent_keyword(wd)

            # 필터 영역 선택하여 필터 변경 -> 여성 기준으로 변경
            search_page.change_criteria_to_women(wd)

            # 변경된 기준 문구 확인
            search_page.check_filter_criteria(wd)

            # 변경된 필터 기준
            api_filter_brand_name = search_woman_popular_brand_name()

            # 변경된 기준의 인기브랜드 1위 확인
            filter_brand_name = search_page.save_popular_brand_name(wd, '1')
            search_page.check_popular_brand_name(api_filter_brand_name, filter_brand_name)

            # 필터를 전체 기준으로 재변경
            search_page.change_criteria_to_all(wd)

            # 뒤로가기
            search_page.click_back_btn(wd)

        except Exception:
            test_result = 'FAIL'
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            error_text = traceback.format_exc().split('\n')
            try:
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
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
            send_test_result(self, test_result, '인기 브랜드 검색 결과 화면 진입')
            return result_data

    def test_search_popular_keyword(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # SEARCH 탭 진입
            navigation_bar.move_to_search(wd)

            # 전체 기준 인기검색어 리스트 호출
            popular_keyword = search_popular_keyword()
            api_keyword_1st = popular_keyword['api_1st_keyword_name']
            api_keyword_25th = popular_keyword['api_25th_keyword_name']

            # 인기 검색어 타이틀 확인
            search_page.check_popular_keyword_title(wd)

            # 첫번째 인기 검색어 저장
            keyword_1st = search_page.save_popular_keyword(wd, '1')

            # API에서 호출한 1위 검색어와 노출되는 검색어가 동일한지 비교 확인
            search_page.check_popular_keyword(keyword_1st, api_keyword_1st)

            # 인기 검색어 1위 검색어 선택
            search_page.click_popular_keyword(wd, keyword_1st)

            # 연관 검색어 없을 경우, 검색 필드 확인 / 있을 경우, 첫번째 연관 검색어 확인
            search_result_page.check_relate_keyword(wd, api_keyword_1st)

            # 검색 화면으로 복귀
            search_result_page.click_back_btn(wd)

            # 최근 검색어에 최근에 선택한 검색어 노출 여부 확인
            search_page.find_recent_keyword(wd)
            search_page.check_recent_keyword(wd, api_keyword_1st)

            # 최근 검색어 모두 지우기
            search_page.clear_recent_keyword(wd)

            # 인기 검색어 25위 저장
            keyword_25th = search_page.save_popular_keyword(wd, '25')

            # API에서 호출한 25위 검색어와 노출되는 검색어가 동일한지 비교 확인
            search_page.check_popular_keyword(keyword_25th, api_keyword_25th)

            # 뒤로가기
            search_page.click_back_btn(wd)

        except Exception:
            test_result = 'FAIL'
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            error_text = traceback.format_exc().split('\n')
            try:
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
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
            send_test_result(self, test_result, '인기 검색어 검색 결과 화면 진입')
            return result_data

    def test_search_results_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # SEARCH 탭 진입
            navigation_bar.move_to_search(wd)

            # 테스트 할 검색어
            keyword = self.conf["keyword"]["knit"]

            # 니트 검색
            search_page.enter_keyword_and_click_search_btn(wd, keyword)

            # 검색 결과 화면의 입력란의 검색어 확인
            search_result_page.check_input_field(wd, keyword)

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            search_result_page.check_relate_brand_name(wd, keyword)

            # 선택할 필터 정보 저장
            sort = self.conf["sort"]["order"]
            color = self.conf["search_filter"]["black"]
            category = self.conf["search_filter"]["woman_clothes"]
            product_info = self.conf["search_filter"]["excludingout_of_stock_products"]

            # 정렬 판매순으로 변경
            search_result_page.click_sort_filter_btn(wd, sort)

            # 색상 필터 -> 블랙 선택
            search_result_page.click_color_filter(wd, color)

            # 카테고리 여성의류 선택
            search_result_page.click_category_filter(wd, category)

            # 상품정보 품절상품 제외 선택
            search_result_page.click_product_info_filter(wd, product_info)

            # 필터 적용
            search_result_page.click_apply_filter_btn(wd)

            # 선택한 필터 정보 저장
            filter_list = search_result_page.save_filter_info(wd)

            # 필터 적용 확인
            search_result_page.check_filter_info([color, category, product_info], filter_list)

            # 검색 화면으로 복귀
            search_result_page.click_back_btn(wd)

            # 인기 브랜드 리스트에서 연관 브랜드 1개인 브랜드 검색 필드에 입력 후 검색
            brand_keyword = com_utils.api_control.search_brand_by_related_brand()
            search_page.enter_keyword_and_click_search_btn(wd, brand_keyword)

            # 브랜드 필터링에 카테고리 첫번째 카테고리 (대,중,소) 선택
            search_result_page.click_brand_category(wd, brand_keyword)

            # 선택한 필터링으로 검색 결과 1위 상품명 비교
            api_product_name = com_utils.api_control.filter_brand_search_results_by_category(brand_keyword)['item_name']
            search_result_page.check_search_product_name(wd, api_product_name)

            # 검색 화면으로 복귀
            search_result_page.click_back_btn(wd)

            # 최근 검색어에 최근에 선택한 검색어 노출 여부 확인
            search_page.check_recent_keyword(wd, brand_keyword)

            # 최근 검색어 모두 지우기
            search_page.clear_recent_keyword(wd)

            # 뒤로가기
            search_page.click_back_btn(wd)

        except Exception:
            test_result = 'FAIL'
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            error_text = traceback.format_exc().split('\n')
            try:
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
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
            send_test_result(self, test_result, '검색 결과 화면 확인')
            return result_data
