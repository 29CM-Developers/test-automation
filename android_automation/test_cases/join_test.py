
import os.path
import sys
import traceback
from time import time
import com_utils
from android_automation.page_action import my_page, login_page, join_page, navigation_bar
from com_utils import values_control
from com_utils.testrail_api import send_test_result
from com_utils.code_optimization import finally_opt, exception_control


class Join:

    # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
    def test_simple_membership_registration_failure(self, wd, test_result='PASS', error_texts=[], img_src=''):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동하여 로그인 페이지 진입
            com_utils.deeplink_control.move_to_my_Android(wd)
            my_page.enter_login_page(wd)

            # 간편 회원가입 선택
            login_page.click_simple_join_btn(wd)

            # 필수 약관 선택 후 가입 시도
            join_page.click_required_terms(wd)

            # 기가입 이메일 입력
            join_page.input_email(wd, self.pconf['LOGIN_SUCCESS_ID'])

            # 기가입 이메일 가입 불가 에러
            join_page.check_same_email_join_error(wd)

            # My 탭으로 복귀
            join_page.click_back_btn(wd)

            # Home 탭으로 이동
            navigation_bar.move_to_home(wd)
            print(f'[{test_name}] 테스트 종료')

        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, '간편 회원가입 실패')
            return result_data
