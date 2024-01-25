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
from com_utils.api_control import large_category_list, large_categories_info, medium_categories_code, \
    category_plp_product
from com_utils.element_control import aal, aalk, aalc, scroll_control, \
    swipe_control, swipe_control, element_scroll_control
from android_automation.page_action import category_page, welove_page, navigation_bar, product_detail_page, \
    context_change
from com_utils.testrail_api import send_test_result
from com_utils.code_optimization import finally_opt, exception_control

class Category:

    def test_category_page(self, wd, test_result='PASS', error_texts=[], img_src=''):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')
            # 딥링크로 카테고리 탭 이동
            navigation_bar.move_to_category(wd)

            # API 호출하여 대 카테고리 리스트 저장
            api_large_categoty_list = large_category_list()

            # api에서 호출한 리스트 길이와 비교하여 노출되는 대 카테고리 리스트 저장
            category_page.check_large_category_list(wd, api_large_categoty_list)

            # 대 카테고리 리스트 상단으로 스크롤
            # category_page.scroll_up_large_category(wd)

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
            category_page.click_category(wd,
                                         f'//android.view.View/android.view.View[2]/android.widget.TextView[@text="{select_large_category}"]')
            category_page.click_category(wd,
                                         f'//android.view.View/android.view.View[3]/android.widget.TextView[@text="{select_category_group}"]')
            category_page.click_category(wd, 'all_title')

            # 타이틀명으로 카테고리 전체 페이지 진입 확인
            # API (large_categories_info)에서 받아온 카테고리명으로 확인
            category_page.check_category_page_shose_title(wd, large_category_name)

            # 신발 전체 상품 중 1위 상품명 저장
            api_name = category_plp_product(large_category_code, '', 1, '')['item_name']
            print(f'api_name : {api_name}')

            # 카테고리 전체 리스트의 첫번째 상품명이 api에서 호출한 상품명과 동일한지 확인
            plp_name = category_page.save_webview_category_product_name(wd, api_name)
            category_page.check_category_product_name(plp_name, api_name)

            # 중 카테고리 : 샌들 선택
            element = category_page.scroll_up_to_category(wd, '샌들')
            element.click()
            sleep(3)

            # 타이틀명으로 중 카테고리 페이지 진입 확인
            category_page.check_category_page_sandal_title(wd)

            # 정렬 신상품 순으로 변경
            category_page.click_filter_by_new(wd)

            # 선택한 대 -> 중 카테고리에 해당하는 PLP API 호출
            api_name = category_plp_product(large_category_code, medium_category_code, 1, 'new')['item_name']

            # 카테고리 페이지에 첫번째 아이템 노출 확인
            plp_name = category_page.save_category_product_name(wd, api_name)
            category_page.check_category_product_name(plp_name, api_name)
            # plp_price = category_page.save_category_product_price(wd)

            # 첫번째 상품 PDP 진입 후, 상품 이름 저장
            category_page.click_category_product(wd, api_name)

            context_change.change_webview_contexts(wd)
            pdp_name = product_detail_page.save_product_name(wd)
            # 네이티브 전환
            context_change.change_native_contexts(wd)

            # 선택한 상품의 PDP에서 상품 이름 비교
            product_detail_page.check_product_name1(pdp_name, plp_name)

            # # pdp 가격 저장 후, 카테고리 plp의 가격과 비교 확인
            # pdp_price = product_detail_page.save_product_price(wd)
            # product_detail_page.check_product_price(pdp_price, plp_price)

            # PDP 상단 네비게이션의 Home 아이콘 선택하여 Home 복귀
            product_detail_page.click_home_btn(wd)

            print(f'[{test_name}] 테스트 종료')
        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      '카테고리를 선택해서 PLP 진입')
            return result_data

    def test_welove(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] CASE 시작')

            # 카테고리 탭 선택
            sleep(2)
            wd.get(self.conf['deeplink']['category'])
            print("카테고리탭 진입")
            close_bottom_sheet(wd)

            # 핀메뉴에서 위러브 페이지 진입
            category_page.click_pin_menu(wd, 'WELOVE')

            # 웹뷰로 변경
            context_change.change_webview_contexts(wd)

            post_title = welove_page.save_first_post_title(wd)
            # post_title = welove_page.save_first_post_title_for_recently_viewed(wd)

            # 첫번째 포스트의 첫번째 해시태그 저장 후 선택
            post_hash_tag = welove_page.save_first_post_hashtag(wd)
            # post_hash_tag = welove_page.save_first_post_hashtag_native(wd)

            print(f'post_hash_tag : {post_hash_tag}')
            welove_page.click_first_post_hashtag(wd, post_hash_tag)
            # welove_page.click_first_post_hashtag_native(wd, post_hash_tag)

            # # 웹뷰로 변경
            # context_change.change_webview_contexts(wd)

            # 해시태그 페이지 타이틀과 저장한 해시태그 비교 확인
            welove_page.check_hash_tag_title(wd, post_hash_tag)
            # 네이티브로 변경
            context_change.change_native_contexts(wd)

            # welove 페이지에서 저장한 포스트가 해시태그 페이지에 노출되는지 확인
            welove_page.check_hash_tag_post(wd, post_title)

            # # 네이티브로 변경
            # context_change.change_native_contexts(wd)

            # welove 페이지로 복귀
            welove_page.click_hash_tag_close_btn(wd)

            # 핀메뉴에서 위러브 페이지 진입
            category_page.click_pin_menu(wd, 'WELOVE')

            # 웹뷰로 변경
            context_change.change_webview_contexts(wd)

            # 포스트 추가 노출 확인
            welove_page.find_and_save_third_post(wd)

            # 네이티브로 변경
            context_change.change_native_contexts(wd)

            # Home으로 복귀
            welove_page.click_welove_back_btn(wd)
            # navigation_bar.move_to_home(wd)

            print(f'[{test_name}] CASE 종료')
        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            deeplink_control.move_to_home(self, wd)
            # 네이티브로 변경
            context_change.change_native_contexts(wd)
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      '카테고리 핀메뉴의 Welove 진입하여 탐색')
            return result_data
