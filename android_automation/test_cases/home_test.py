import json
import logging
import os.path
import subprocess
import sys
import traceback
import logging
import requests
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.mobileby import MobileBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import com_utils
from android_automation.page_action import navigation_bar, category_page, home_page, search_page, bottom_sheet, \
    like_page, my_page, product_detail_page, context_change
from android_automation.page_action.bottom_sheet import close_bottom_sheet, close_like_bottom_sheet
from android_automation.page_action.like_page import close_brand_recommended_page
from com_utils import values_control, deeplink_control
from time import sleep, time
from com_utils.api_control import search_total_popular_brand_name, home_banner_info, feed_contents_info
from com_utils.element_control import aal, aalk, aalc, scroll_control, swipe_control, swipe_control, aals
from com_utils.testrail_api import send_test_result
from com_utils.code_optimization import finally_opt, exception_control


class Home:

    def test_move_tab_from_home(self, wd, test_result='PASS', error_texts=[], img_src=''):

        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # CATEGORY 탭 진입
            navigation_bar.move_to_category(wd)

            # 첫번째 대 카테고리 선택
            category_page.click_first_large_category(wd)

            # 중 카테고리 리스트 중 상단 4개의 카테고리명 확인
            category_page.check_unique_medium_category(self, wd)

            # HOME 탭으로 이동하여 29CM 로고 확인
            navigation_bar.move_to_home(wd)
            home_page.check_home_logo(wd)

            # SEARCH 탭 진입, 최근검색어, 키보드 닫기
            navigation_bar.move_to_search(wd)
            search_page.check_keyboard_clear_recent_keyword(wd)

            # 첫번째 인기 브랜드 카테고리 타이틀 저장
            first_brand_category = search_total_popular_brand_name()['category_name']

            # 첫번째 인기 브랜드 카테고리 확인
            search_page.check_first_popular_brand_category(wd, first_brand_category)

            # 인기 브랜드 타이틀 확인
            search_page.check_popular_keyword_title(wd)

            # HOME으로 이동하여 29CM 로고 확인
            search_page.click_back_btn(wd)
            bottom_sheet.close_bottom_sheet(wd)
            home_page.check_home_logo(wd)

            # LIKE 탭 진입
            navigation_bar.move_to_like(wd)

            # LIKE 탭 상단 문구 확인
            like_page.check_like_phases(wd)

            # HOME 탭으로 이동하여 29CM 로고 확인
            navigation_bar.move_to_home(wd)
            home_page.check_home_logo(wd)

            # MY 탭 진입하여 닉네임 확인
            navigation_bar.move_to_my(wd)
            my_page.check_nickname(self, wd)

            # HOME 탭으로 이동하여 29CM 로고 확인
            navigation_bar.move_to_home(wd)
            home_page.check_home_logo(wd)
            print(f'[{test_name}] 테스트 종료')
        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, '홈화면에서 다른 탭으로 이동')
            return result_data

    def test_home_banner(self, wd, test_result='PASS', error_texts=[], img_src=''):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')
            bottom_sheet.close_bottom_sheet(wd)

            # 라이프 탭 디폴트 선택 여부 확인 및 닫기
            home_page.click_close_life_tab(wd)

            # 라이프 탭 선택
            # home_page.click_tab_name(wd, '라이프')

            # 라이프 선택 시, 노출되는 탭 이름 비교
            # save_tab_names = home_page.save_tab_names(wd)
            home_page.check_tab_names(wd)

            # 라이프 선택 닫기
            # home_page.click_close_life_tab(wd)

            # 기본으로 노출되는 탭 이름 비교
            # save_tab_names = home_page.save_tab_names(wd)
            # home_page.check_tab_names(wd)

            # 우먼 탭 선택
            home_page.click_tab_name(wd, 'women_tab')

            # 홈화면 배너 중복 여부 확인
            home_page.check_for_duplicate_banner_contents(self)

            # 홈화면 배너 타이틀 3개 저장
            home_banner_title = home_page.save_banner_title(wd)

            # 홈화면 배너 api와 저장된 배너 타이틀 비교 확인
            home_page.check_home_banner_title(self, home_banner_title)

            # 다이나믹 게이트 -> 센스있는 선물하기 선택
            dynamic_gate_btn_name = home_page.click_dynamic_gate(wd)

            # 상단 타이틀과 선물하기 페이지 내부 타이틀 확인
            home_page.check_dynamic_gate_gift_page(wd, dynamic_gate_btn_name)

            # 뒤로가기 버튼 동작하지 않아 딥링크 사용하여 Home으로 이동
            deeplink_control.move_to_home_Android(wd)
            print(f'[{test_name}] 테스트 종료')
        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      '홈화면의 배너, 다이나믹 게이트 확인')
            return result_data

    def test_home_contents(self, wd, test_result='PASS', error_texts=[], img_src=''):

        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # 바텀시트 노출 여부 확인
            bottom_sheet.close_bottom_sheet(wd)

            # 라이프 탭 디폴트 선택 여부 확인 및 닫기
            home_page.click_close_life_tab(wd)

            # 맨 카테고리 탭 선택
            home_page.click_tab_name(wd, 'men_tab')

            # 추천 상품 영역 확인
            home_page.check_scroll_to_recommended_contents(wd)

            # 우먼 카테고리 탭 선택
            home_page.click_tab_name(wd, 'women_tab')

            # 피드 정보 불러오기
            feed_title_list = feed_contents_info(self.pconf['LOGIN_SUCCESS_ID'], self.pconf['LOGIN_SUCCESS_PW'])
            feed_title_1st = feed_title_list['first_feed_title']
            feed_contain_item = feed_title_list['first_title_with_item']
            feed_title_2nd = feed_title_list['second_feed_title']

            # 저장한 첫번째 피드 정보와 동일한 피드 정보가 노출 될 때까지 스크롤
            home_page.scroll_to_feed_contents_feed_title_1st(wd, feed_title_1st)

            # 싱픔이 연결된 피드 정보와 동일한 피드 정보가 노출 될 때까지 스크롤
            home_page.scroll_to_feed_contents_feed_contain_item(wd)

            # 하트 이미 선택되었는지 확인
            home_page.check_heartIcon_is_selected(wd)

            # 좋아요 버튼 선택 전, 좋아요 수 저장
            content_like_count = home_page.save_contents_like_count(wd)

            # 좋아요 버튼 선택하여 좋아요 후, 카운트 확인
            home_page.click_contents_like_btn(wd)

            # 앱평가 팝업 확인
            home_page.check_app_evaluation_popup(wd)
            content_like_select = home_page.save_contents_like_count(wd)
            home_page.check_increase_like_count(content_like_count, content_like_select)

            # 좋아요 버튼 선택하여 좋아요 해제 후, 카운트 확인
            home_page.click_contents_like_btn(wd)
            content_like_unselect = home_page.save_contents_like_count(wd)
            home_page.check_decrease_like_count(content_like_count, content_like_unselect)

            # 컨텐츠 상품의 상품명과 상품가격 저장 후, 해당 상품의 상세 페이지 진입
            contents_product_name = home_page.save_contents_product_name(wd)
            contents_product_price = home_page.save_contents_product_price(wd)
            home_page.click_contents_product(wd)

            # 상품명 비교 확인
            context_change.switch_context(wd, 'webview')
            pdp_name = product_detail_page.save_product_name(wd)
            context_change.change_native_contexts(wd)
            product_detail_page.check_product_name(pdp_name, contents_product_name)

            # 상품 가격 비교 확인
            # pdp_price = product_detail_page.save_product_price(wd)
            # product_detail_page.check_product_price(pdp_price, contents_product_price)

            # Home으로 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # 두번째 피드 정보와 동일한 피드 정보가 노출 될 때까지 스크롤
            home_page.scroll_to_feed_contents_feed_title_1st(wd, feed_title_2nd)

            print(f'[{test_name}] 테스트 종료')
        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, '홈화면의 컨텐츠(피드) 탐색')
            return result_data