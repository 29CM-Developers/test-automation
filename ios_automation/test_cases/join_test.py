import os
import sys
import traceback
import com_utils.deeplink_control

from time import time
from com_utils.code_optimization import exception_control, finally_opt
from ios_automation.page_action import login_page, my_page, join_page, context_change, mobile_setting_page


class Join:
    def test_simple_membership_registration_failure(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동하여 로그인 페이지 진입
            com_utils.deeplink_control.move_to_my(self, wd)
            my_page.enter_login_page(wd)

            # 간편 회원가입 선택
            login_page.click_simple_join_btn(wd)

            context_change.switch_context(wd, 'webview')

            # 필수 약관 선택 후 가입 시도
            join_page.click_required_terms(wd)

            # 기가입 이메일 입력
            join_page.input_email(wd, self.pconf['id_29cm'])

            # 기가입 이메일 가입 불가 에러
            join_page.check_same_email_join_error(wd)

            context_change.switch_context(wd, 'native')

            # My 탭으로 복귀
            join_page.click_back_btn(wd)
            login_page.click_back_btn(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '간편 회원가입 실패'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_sns_account_registration_failure(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 설정 앱에서 사파리 데이터 지우기
            mobile_setting_page.click_safari_menu(wd)
            mobile_setting_page.click_safari_clean_data(wd)

            # My 탭 진입
            com_utils.deeplink_control.move_to_my(self, wd)

            # 로그인 페이지 진입
            my_page.enter_login_page(wd)

            # 카카오 로그인 페이지 진입
            login_page.click_sns_login_btn(wd, '카카오')

            # 카카오 로그인
            login_page.kakao_input_id_password(wd, self.pconf['sns_error_id'], self.pconf['sns_error_password'])

            # 중복 계정 팝업 확인 및 이메일 입력란 확인
            login_page.check_duplicate_account(wd)
            login_page.check_id_input_field_test(wd, self.pconf['sns_error_id'])
            login_page.clear_id_password(wd)

            # 페이스북 로그인 페이지 진입
            login_page.click_sns_login_btn(wd, '페이스북')

            # 페이스북 로그인
            login_page.facebook_login_confirm(wd, self.pconf['sns_error_id'], self.pconf['sns_error_password'])

            # 중복 계정 팝업 확인 및 이메일 입력란 확인
            login_page.check_duplicate_account(wd)
            login_page.check_id_input_field_test(wd, self.pconf['sns_error_id'])

            # My 탭으로 복귀
            login_page.click_back_btn(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = 'SNS 계정 회원가입 실패'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data
