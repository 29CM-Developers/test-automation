
import os
import sys
import traceback
import com_utils.element_control
import com_utils.deeplink_control

from time import time
from appium.webdriver.common.appiumby import AppiumBy
from com_utils import values_control
from com_utils.testrail_api import send_test_result
from com_utils.api_control import large_category_list, large_categories_info, medium_categories_code, \
    category_plp_product
from ios_automation.page_action import category_page, welove_page, navigation_bar, product_detail_page, context_change


class Category:
    def test_category_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        print(f'[{test_name}] 테스트 시작')

        try:
            # 딥링크로 카테고리 탭 이동
            com_utils.deeplink_control.move_to_category(self, wd)

            # API 호출하여 대 카테고리 리스트 저장
            api_large_categoty_list = large_category_list()

            # api에서 호출한 리스트 길이와 비교하여 노출되는 대 카테고리 리스트 저장
            test_result = category_page.check_large_category_list(wd, warning_texts, api_large_categoty_list)

            # 대 카테고리 리스트 상단으로 스크롤
            category_page.scroll_up_large_category(wd)

            # 확인 카테고리명
            select_category_group = self.conf["category_groups"]['women']
            select_large_category = self.conf["large_categories"]['shoes']
            select_medium_category = self.conf["medium_categories"]['sandals']

            # 대 카테고리, 중 카테고리 코드 번호 저장
            category_info = large_categories_info(select_category_group, select_large_category)
            large_category_code = category_info['large_category_code']
            large_category_name = category_info['large_category_name']
            medium_category_code = medium_categories_code(large_category_code, select_medium_category)

            # 신발 > 여성 > 전체 순으로 카테고리 선택
            category_page.click_category(wd, f'//XCUIElementTypeButton[@name="{select_large_category}"]')
            category_page.click_category(wd, f'//XCUIElementTypeButton[@name="{select_category_group}"]')
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'all').click()

            # 타이틀명으로 카테고리 전체 페이지 진입 확인
            # API (large_categories_info)에서 받아온 카테고리명으로 확인
            test_result = category_page.check_category_page_title(wd, warning_texts, large_category_name)

            # 신발 전체 상품 중 1위 상품명 저장
            api_name = category_plp_product(large_category_code, '', 1, '')['item_name']

            # webview 전환
            context_change.switch_context(wd, 'webview')

            # 카테고리 전체 리스트의 첫번째 상품명이 api에서 호출한 상품명과 동일한지 확인
            plp_name = category_page.save_webview_category_product_name(wd)
            test_result = category_page.check_category_product_name(warning_texts, plp_name, api_name)

            # 중 카테고리 : 샌들 선택
            wd.find_element(AppiumBy.XPATH, f'//a[contains(text(), "{select_medium_category}")]').click()

            # native 전환
            context_change.switch_context(wd, 'native')

            # 타이틀명으로 중 카테고리 페이지 진입 확인
            test_result = category_page.check_category_page_title(wd, warning_texts, select_medium_category)

            # 정렬 신상품 순으로 변경
            category_page.click_filter_by_new(wd)

            # 선택한 대 -> 중 카테고리에 해당하는 PLP API 호출
            api_name = category_plp_product(large_category_code, medium_category_code, 1, 'new')['item_name']

            # 카테고리 페이지에 첫번째 아이템 노출 확인
            plp_name = category_page.save_category_product_name(wd)
            test_result = category_page.check_category_product_name(warning_texts, plp_name, api_name)
            plp_price = category_page.save_category_product_price(wd)

            # 첫번째 상품 PDP 진입 후, 상품 이름 저장
            category_page.click_category_product(wd)
            pdp_name = product_detail_page.save_product_name(wd)

            # 선택한 상품의 PDP에서 상품 이름 비교
            test_result = product_detail_page.check_product_name(warning_texts, pdp_name, plp_name)

            # webview 전환
            context_change.switch_context(wd, 'webview')

            # pdp 가격 저장 후, 카테고리 plp의 가격과 비교 확인
            pdp_price = product_detail_page.save_product_price(wd)
            test_result = product_detail_page.check_product_price(test_result, warning_texts, pdp_price, plp_price)

            # native 전환
            context_change.switch_context(wd, 'native')

            # PDP 상단 네비게이션의 Home 아이콘 선택하여 Home 복귀
            product_detail_page.click_home_btn(wd)

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
            context_change.switch_context(wd, 'native')
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '카테고리를 선택해서 PLP 진입')
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
            send_test_result(self, test_result, '카테고리 핀메뉴의 Welove 진입하여 탐색')
            return result_data
