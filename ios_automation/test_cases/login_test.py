import os.path
import sys
import traceback
import com_utils.deeplink_control

from time import time
from com_utils import values_control
from ios_automation.page_action import login_page, my_page, navigation_bar
from ios_automation.page_action.bottom_sheet import close_bottom_sheet
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
            test_result = my_page.check_nickname(self, wd, warning_texts)

            # Home 으로 복귀
            navigation_bar.move_to_home(wd)

            # 복귀 후, 홈 탭 진입 전 노출 화면 있는지 확인
            test_select_category(wd)
            close_bottom_sheet(wd)

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
            com_utils.deeplink_control.move_to_home(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
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
            test_result = my_page.check_login_btn(wd, warning_texts)

            # Home 으로 복귀
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
            com_utils.deeplink_control.move_to_home(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
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
            test_result = login_page.check_login_error_text(self, wd, warning_texts)

            # 이메일, 비밀번호 입력값 제거
            login_page.clear_id_password(wd)

            # 올바른 아이디, 올바른 비밀번호 입력
            login_page.input_id_password(wd, self.pconf['id2_29cm'], self.pconf['password_29cm'])

            # 프로필 이름 확인
            test_result = my_page.check_nickname(self, wd, warning_texts)

            # Home 으로 복귀
            navigation_bar.move_to_home(wd)

            # 복귀 후, 홈 탭 진입 전 노출 화면 있는지 확인
            test_select_category(wd)
            close_bottom_sheet(wd)

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
            com_utils.deeplink_control.move_to_home(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data




