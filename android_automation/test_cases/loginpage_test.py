import logging
import os.path
import subprocess
import sys
import traceback
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec, wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import com_utils
from android_automation.page_action import my_page, login_page, navigation_bar, my_edit_user_info_page
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from android_automation.page_action.select_category_page import test_select_category
from time import sleep, time, strftime, localtime
from appium.webdriver.common.touch_action import TouchAction
from com_utils import values_control, slack_result_notifications, deeplink_control
from com_utils.element_control import aal, aalk, aalc, scroll_control
from com_utils.testrail_api import send_test_result
from com_utils.code_optimization import finally_opt, exception_control


class LoginLogout:

    def test_email_login_success(self, wd, test_result='PASS', error_texts=[], img_src=''):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            sleep(4)

            # 로그인 페이지 진입
            com_utils.deeplink_control.move_to_my_Android(wd)
            my_page.enter_login_page(wd)

            # 올바른 아이디, 올바른 비밀번호 입력
            login_page.input_id_password(wd, self.pconf['LOGIN_SUCCESS_ID'], self.pconf['LOGIN_SUCCESS_PW'])

            # 프로필 이름 확인
            my_page.check_nickname(self, wd)

            # 회원 정보 수정 페이지 진입
            my_page.click_edit_user_info_menu(wd)

            # 비밀번호 재확인
            my_edit_user_info_page.input_password(wd, self.pconf['LOGIN_SUCCESS_PW'])
            my_edit_user_info_page.click_next_btn(wd)

            # 회원 정보 수정 페이지의 타이틀과 닉네임 확인
            my_edit_user_info_page.check_edit_page_title(wd)
            my_edit_user_info_page.check_edit_page_id(wd, self.pconf['MASKING_NAME'])

            # Home 으로 복귀
            my_edit_user_info_page.click_back_btn(wd)
            navigation_bar.move_to_home(wd)

            # 복귀 후, 홈 탭 진입 전 노출 화면 있는지 확인
            test_select_category(wd)

            print(f'[{test_name}] 테스트 종료')

        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, '이메일 로그인 성공')
            return result_data

    def test_logout(self, wd, test_result='PASS', error_texts=[], img_src=''):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭 딥링크로 진입
            com_utils.deeplink_control.move_to_my_Android(wd)

            # 로그아웃 버튼 선택
            my_page.find_logout_btn(wd)
            my_page.click_logout_btn(wd)

            # 로그아웃 완료 > 로그인,회원가입 문구 확인
            my_page.find_login_btn(wd)
            my_page.check_login_btn(wd)

            # Home 으로 복귀 후,온보딩 프로그램 확인
            navigation_bar.logout_and_move_to_home(wd)
            print(f'[{test_name}] 테스트 종료')

        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, '로그아웃')
            return result_data

    def test_email_login_error_success(self, wd, test_result='PASS', error_texts=[], img_src=''):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # 로그인 페이지 진입
            com_utils.deeplink_control.move_to_my_Android(wd)
            my_page.enter_login_page(wd)

            # 올바른 이메일, 잘못된 비밀번호 입력하여 에러 문구 확인
            login_page.input_id_password(wd, self.pconf['LOGIN_SUCCESS_ID_1'], self.pconf['LOGIN_FAILED_PW'])
            login_page.check_login_error_text(self, wd)

            # 이메일, 비밀번호 입력값 제거
            login_page.clear_id_password(wd)

            # 올바른 아이디, 올바른 비밀번호 입력
            login_page.input_id_password(wd, self.pconf['LOGIN_SUCCESS_ID_1'], self.pconf['LOGIN_SUCCESS_PW'])

            # 프로필 이름 확인
            my_page.check_nickname(self, wd)

            # Home 으로 복귀
            # navigation_bar.move_to_home(wd)

            # 복귀 후, 홈 탭 진입 전 노출 화면 있는지 확인
            test_select_category(wd)
            close_bottom_sheet(self.wd)

            print(f'[{test_name}] 테스트 종료')

        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, '이메일 로그인 실패')
            return result_data