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
from android_automation.page_action import navigation_bar, category_page, login_page, home_page, best_product_list_page, \
    product_detail_page, search_page, search_result_page, my_page, context_change
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from com_utils import values_control, element_control
from time import sleep, time, strftime, localtime
from com_utils.element_control import aal, aalk, aalc, aals, swipe_control, is_keyboard_displayed, close_keyboard
from com_utils.testrail_api import send_test_result

class NotLogin:

    def test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src=''):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            # sleep(3)
            print(f'[{test_name}] 테스트 시작')

            close_bottom_sheet(self.wd)
            # 카테고리 탭에서 의류>상의 카테고리 선택하여 PLP 진입 > PLP에서 좋아요 버튼 선택
            navigation_bar.move_to_category(wd)
            category_page.click_category_top(wd)
            category_page.click_not_login_user_product_like_btn(wd)

            # 로그인 페이지 진입 및 확인
            login_page.check_login_page(wd)

            # Home 탭으로 복귀
            navigation_bar.move_to_back(wd)
            navigation_bar.move_to_back(wd)
            navigation_bar.move_to_home(wd)

            # 우상단 알람 선택
            navigation_bar.move_to_alarm(wd)
            # 로그인 페이지 진입 및 확인
            login_page.check_login_page(wd)
            # Home 탭으로 복귀
            navigation_bar.move_to_back(wd)

            # 홈 > 우상단 장바구니 아이콘 선택
            navigation_bar.move_to_top_cart(wd)
            # Home 탭으로 복귀
            navigation_bar.move_to_back(wd)

            # 하단 like 아이콘 선택
            navigation_bar.move_to_like(wd)
            # Home 탭으로 복귀
            navigation_bar.move_to_back(wd)
            print(f'[{test_name}] 테스트 종료')

        except Exception:
            # 오류 발생 시 테스트 결과를 실패로 한다
            test_result = 'FAIL'
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc().split('\n')
            try:
                # 에러메시지 분류 시 예외처리
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
            except Exception:
                pass
            wd.get('app29cm://home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            send_test_result(self, test_result, '비로그인 유저가 사용 불가한 기능 사용 시도 시, 로그인 페이지에 진입')
            return result_data

    def test_not_login_user_possible(self, wd, test_result='PASS', error_texts=[], img_src=''):

        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # 라이프 선택 닫기
            home_page.click_close_life_tab(wd)

            # Home > 베스트 탭 선택하여 베스트 PLP 진입
            home_page.click_tab_name(wd, 'best_tab')

            # 베스트 탭에서 첫번째 상품명 저장하고 PDP 진입
            plp_name = best_product_list_page.save_best_plp_first_product_name(wd)
            plp_price = best_product_list_page.save_best_first_product_price(wd)
            best_product_list_page.click_home_tap_best_first_product(wd)

            # 웹뷰 전환
            context_change.switch_context(wd, 'webview')
            # 선택한 상품의 PDP에서 상품 이름 비교
            pdp_name = product_detail_page.save_product_name(wd)
            # 네이티브 전환
            context_change.change_native_contexts(wd)

            product_detail_page.check_product_name(pdp_name, plp_name)

            # PDP 상단 네비게이션의 Home 아이콘 선택하여 Home 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # 카테고리 탭 진입
            navigation_bar.move_to_category(wd)

            # 추천 페이지 진입하여 상단의 타이틀 비교 (비로그인 유저 : 당신)
            category_page.click_for_you_category(wd)
            category_page.check_not_login_user_recommended_tab(wd)

            # 홈 탭으로 복귀
            category_page.click_back_btn(wd)
            navigation_bar.move_to_home(wd)

            # 상단 검색 버튼 선택하여 인기 브랜드 6위 선택
            home_page.click_search_btn(wd)
            search_brand_name = search_page.save_popular_brand_name(wd, '6')
            search_page.click_popular_brand_name(wd, '6')

            # 검색 결과 화면 진입하여 선택한 브랜드명과 입력란의 문구 비교 확인
            search_result_page.check_input_field(wd, search_brand_name)

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            search_result_page.check_relate_brand_name(wd, search_brand_name)

            # My 탭 진입하여 로그인,회원가입 문구 노출 확인
            search_result_page.click_back_btn(wd)
            search_result_page.click_back_btn(wd)
            navigation_bar.move_to_my(wd)
            my_page.check_login_btn(wd)

            # Home 탭으로 복귀
            # navigation_bar.move_to_home(wd)

            print(f'[{test_name}] 테스트 종료')

        except Exception:
            # 오류 발생 시 테스트 결과를 실패로 한다
            test_result = 'FAIL'
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc().split('\n')
            try:
                # 에러메시지 분류 시 예외처리
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
            except Exception:
                pass
            wd.get('app29cm://home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            send_test_result(self, test_result, '비로그인 유저가 사용 가능한 기능 확인')
            return result_data
