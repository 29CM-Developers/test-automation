import os.path
import sys
import traceback
import com_utils.deeplink_control

from time import time, sleep
from com_utils import values_control
from com_utils.db_connection import connect_db, insert_data, disconnect_db
from com_utils.testrail_api import send_test_result
from ios_automation.page_action import login_page, my_page, navigation_bar, my_edit_user_info_page, context_change
from ios_automation.page_action.select_category_page import test_select_category


class UserLoginTest:
    def test_email_login_success(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
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
            context_change.switch_context(wd, 'native')
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '이메일 로그인 성공')
            if self.user == 'pipeline':
                connection, cursor = connect_db(self)
                insert_data(connection, cursor, self, result_data)
                disconnect_db(connection, cursor)
            return result_data

    def test_logout(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
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
            send_test_result(self, test_result, '로그아웃')
            if self.user == 'pipeline':
                connection, cursor = connect_db(self)
                insert_data(connection, cursor, self, result_data)
                disconnect_db(connection, cursor)
            return result_data

    def test_email_login_error_success(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
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
            context_change.switch_context(wd, 'native')
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '이메일 로그인 실패')
            if self.user == 'pipeline':
                connection, cursor = connect_db(self)
                insert_data(connection, cursor, self, result_data)
                disconnect_db(connection, cursor)
            return result_data
