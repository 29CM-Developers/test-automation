import os.path
import sys
import traceback
import com_utils.deeplink_control

from time import time
from com_utils.code_optimization import exception_control, finally_opt
from ios_automation.page_action import login_page, my_page, navigation_bar, my_edit_user_info_page, join_page
from ios_automation.page_action.select_category_page import test_select_category


class UserLoginTest:
    def test_email_login_success(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 로그인 페이지 진입
            com_utils.deeplink_control.move_to_my(self, wd)
            my_page.enter_login_page(wd)

            # 올바른 아이디, 올바른 비밀번호 입력
            login_page.input_id_password(wd, self.pconf['id_29cm'], self.pconf['password_29cm'])

            # 프로필 이름 확인
            my_page.check_nickname(self, wd)

            # 회원 정보 수정 페이지 진입
            my_page.click_edit_user_info_menu(wd)

            # 비밀번호 재확인
            my_edit_user_info_page.input_password(wd, self.pconf['password_29cm'])
            my_edit_user_info_page.click_next_btn(wd)

            # 회원 정보 수정 페이지의 타이틀과 닉네임 확인
            my_edit_user_info_page.check_edit_page_title(wd)
            my_edit_user_info_page.check_edit_page_id(wd, self.pconf['masking_id'])

            # Home 으로 복귀
            my_edit_user_info_page.click_back_btn(wd)
            navigation_bar.move_to_home(wd)

            # 복귀 후, 홈 탭 진입 전 노출 화면 있는지 확인
            test_select_category(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '이메일 로그인 성공'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_logout(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭 딥링크로 진입
            com_utils.deeplink_control.move_to_my(self, wd)

            # 로그아웃 버튼 선택
            my_page.find_logout_btn(wd)
            my_page.click_logout_btn(wd)

            # 로그아웃 완료 > 로그인,회원가입 문구 확인
            my_page.find_login_btn(wd)
            my_page.check_login_btn(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '로그아웃'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_email_login_error_success(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 로그인 페이지 진입
            com_utils.deeplink_control.move_to_my(self, wd)
            my_page.enter_login_page(wd)

            # 올바른 이메일, 잘못된 비밀번호 입력하여 에러 문구 확인
            login_page.input_id_password(wd, self.pconf['id_29cm'], self.pconf['error_password_29cm'])
            login_page.check_login_error_text(self, wd)

            # 이메일, 비밀번호 입력값 제거
            login_page.clear_id_password(wd)

            # 올바른 아이디, 올바른 비밀번호 입력
            login_page.input_id_password(wd, self.pconf['id2_29cm'], self.pconf['password_29cm'])

            # 프로필 이름 확인
            my_page.check_nickname(self, wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '이메일 로그인 실패'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_sns_login_logout(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭 진입
            com_utils.deeplink_control.move_to_my(self, wd)

            # 카카오 로그인 페이지 진입
            my_page.enter_login_page(wd)
            login_page.click_sns_login_btn(wd, '카카오')

            # 카카오 로그인
            login_page.kakao_input_id_password(wd, self.pconf['kakao_id'], self.pconf['kakao_password'])

            # 프로필 이름 확인
            my_page.check_nickname(self, wd)

            # 로그아웃 후, 로그인 버튼 확인
            my_page.check_logout_and_login_btn(self, wd)

            # 네이버 로그인 페이지 진입
            my_page.enter_login_page(wd)
            login_page.click_sns_login_btn(wd, '네이버')

            # 네이버 로그인
            login_page.naver_input_id_password(wd, self.pconf['naver_id'], self.pconf['naver_password'])

            # 프로필 이름 확인
            my_page.check_nickname(self, wd)

            # 로그아웃 후, 로그인 버튼 확인
            my_page.check_logout_and_login_btn(self, wd)

            # 페이스북 로그인 페이지 진입
            my_page.enter_login_page(wd)
            login_page.click_sns_login_btn(wd, '페이스북')

            # 페이스북 로그인
            login_page.facebook_login_confirm(wd, self.pconf['facebook_id'], self.pconf['facebook_password'])

            # 프로필 이름 확인
            my_page.check_nickname(self, wd)

            # 로그아웃 후, 로그인 버튼 확인
            my_page.check_logout_and_login_btn(self, wd)

            # 애플 로그인 페이지 진입
            my_page.enter_login_page(wd)
            login_page.click_sns_login_btn(wd, 'Apple')

            # 애플 로그인
            login_page.apple_input_password(wd, self.pconf['apple_password'])

            # 프로필 이름 확인
            my_page.check_nickname(self, wd)

            # 로그아웃 후, 로그인 버튼 확인
            my_page.check_logout_and_login_btn(self, wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = 'SNS 로그인 및 로그아웃'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_enter_the_sns_account_sign_up_page(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭 진입
            com_utils.deeplink_control.move_to_my(self, wd)

            # 카카오 로그인 페이지 진입
            my_page.enter_login_page(wd)
            login_page.click_sns_login_btn(wd, '카카오')

            # 카카오 로그인
            login_page.kakao_input_id_password(wd, self.pconf['kakao_id2'], self.pconf['kakao_password2'])

            # 회원가입 페이지 진입 확인
            join_page.check_auth_page(wd)

            # 마이페이지 > 로그인 버튼 확인
            join_page.click_back_btn(wd)
            login_page.check_login_page(wd)

            # 네이버 로그인 페이지 진입
            my_page.enter_login_page(wd)
            login_page.click_sns_login_btn(wd, '네이버')

            # 네이버 로그인
            login_page.naver_input_id_password(wd, self.pconf['naver_id2'], self.pconf['naver_password2'])

            # 회원가입 페이지 진입 확인
            join_page.check_required_terms_page(wd)

            # 마이페이지 > 로그인 버튼 확인
            join_page.click_back_btn(wd)
            login_page.check_login_page(wd)

            # 페이스북 로그인 페이지 진입
            my_page.enter_login_page(wd)
            login_page.click_sns_login_btn(wd, '페이스북')

            # 페이스북 로그인
            login_page.facebook_login_confirm(wd, self.pconf['facebook_id2'], self.pconf['facebook_password2'])

            # 회원가입 페이지 진입 확인
            join_page.check_required_terms_page(wd)

            # 마이페이지 > 로그인 버튼 확인
            join_page.click_back_btn(wd)
            login_page.check_login_page(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '미가입 SNS 계정 가입 화면 진입'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data
