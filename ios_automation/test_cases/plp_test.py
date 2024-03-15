import os
import sys
import traceback

from time import time
from com_utils import api_control
from com_utils.code_optimization import exception_control, finally_opt
from com_utils.deeplink_control import move_to_category
from ios_automation.page_action import category_page, best_product_list_page, product_detail_page, selection_page


class Plp:
    def test_product_listing_page(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        print(f'[{test_name}] 테스트 시작')

        try:
            # 카테고리 탭 > 여성 의류 BEST
            move_to_category(self, wd)
            category_page.click_best_category(wd)

            # 베스트 PLP 진입 확인
            best_product_list_page.check_entry_best_plp(wd)

            # 일간 필터 선택
            best_product_list_page.click_period_sort(wd, '일간')

            # api로 호출한 1위 상품명과 노출되는 1위 상품명 비교
            api_oneday_product = api_control.best_plp_women_clothes(1, 'ONE_DAY')['item_name']
            oneday_product = best_product_list_page.save_best_first_product_name(wd)
            best_product_list_page.check_best_product_name(api_oneday_product, oneday_product)

            # 주간 필터 선택
            best_product_list_page.click_period_sort(wd, '주간')

            # api로 호출한 1위 상품명과 노출되는 1위 상품명 비교
            api_oneweek_product = api_control.best_plp_women_clothes(1, 'ONE_WEEK')['item_name']
            oneweek_product = best_product_list_page.save_best_first_product_name(wd)
            best_product_list_page.check_best_product_name(api_oneweek_product, oneweek_product)

            # 월간 필터 선택
            best_product_list_page.click_period_sort(wd, '월간')

            # api로 호출한 1위 상품명과 노출되는 1위 상품명 비교
            api_onemonth_product = api_control.best_plp_women_clothes(1, 'ONE_MONTH')['item_name']
            onemonth_product = best_product_list_page.save_best_first_product_name(wd)
            best_product_list_page.check_best_product_name(api_onemonth_product, onemonth_product)

            # 실시간 필터로 복귀
            best_product_list_page.click_period_sort(wd, '실시간')

            # 좋아요 버튼 선택 전, 좋아요 수 저장
            heart_count = best_product_list_page.save_best_product_like_count(wd)

            # 좋아요 버튼 선택 -> 찜하기 등록
            best_product_list_page.click_best_product_like_btn(wd)
            selection_page.click_close_selection_pop_up(wd)
            heart_select = best_product_list_page.save_best_product_like_count(wd)

            # 좋아요 수 증가 확인
            best_product_list_page.check_increase_like_count(heart_count, heart_select)

            # 좋아요 버튼 선택 -> 찜하기 해제
            best_product_list_page.click_best_product_like_btn(wd)
            heart_deselect = best_product_list_page.save_best_product_like_count(wd)

            # 좋아요 수 차감 확인
            best_product_list_page.check_decrease_like_count(heart_count, heart_deselect)

            # 실시간 여성 의류 베스트 1위 상품명과 금액 저장 및 선택
            now_1st_product = api_control.best_plp_women_clothes(1, 'NOW')['item_name']
            now_1st_product_price = best_product_list_page.save_plp_price(wd)
            best_product_list_page.click_best_first_product(wd)

            # PDP 상품명 비교
            pdp_name = product_detail_page.save_product_name(wd)
            product_detail_page.check_product_name(pdp_name, now_1st_product)

            # PDP 상품가격 비교
            pdp_price = product_detail_page.save_product_price(wd)
            product_detail_page.check_product_price(pdp_price, now_1st_product_price)

            # 베스트 PLP로 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # API에서 호출한 상품명 저장
            now_10th_product_name = api_control.best_plp_women_clothes(10, 'NOW')['item_name']

            # 실시간 10위 상품 노출 확인
            best_product_list_page.find_scroll_and_find_product_rank(wd, '10')
            best_product_list_page.check_additional_product(wd, now_10th_product_name)

            # Home으로 복귀
            best_product_list_page.click_back_btn(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = 'PLP 기능 확인'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data
