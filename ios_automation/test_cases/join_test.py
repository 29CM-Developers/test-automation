import os
import sys
import traceback
import com_utils.deeplink_control

from time import time
from com_utils import values_control
from com_utils.testrail_api import send_test_result
from ios_automation.page_action import login_page, my_page, navigation_bar, join_page


class Join:
    def test_simple_membership_registration_failure(self, wd, test_result='PASS', error_texts=[], img_src='',
                                                    warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동하여 로그인 페이지 진입
            com_utils.deeplink_control.move_to_my(self, wd)
            my_page.enter_login_page(wd)

            # 간편 회원가입 선택
            login_page.click_simple_join_btn(wd)

            # 필수 약관 선택 후 가입 시도
            join_page.click_required_terms(wd)

            # 기가입 이메일 입력
            join_page.input_email(wd, self.pconf['id_29cm'])

            # 기가입 이메일 가입 불가 에러
            test_result = join_page.check_same_email_join_error(wd, warning_texts)

            # My 탭으로 복귀
            join_page.click_back_btn(wd)
            login_page.click_back_btn(wd)

            # Home 탭으로 이동
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
            send_test_result(self, test_result, '간편 회원가입 실패')
            return result_data
