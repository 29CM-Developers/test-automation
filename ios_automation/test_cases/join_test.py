import os
import sys
import traceback

from time import time, sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException

from com_utils import values_control


class Join:
    def test_simple_membership_registration_failure(self, wd, test_result='PASS', error_texts=[], img_src='',
                                                    warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            wd.get(self.conf['deeplink']['my'])
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()
            sleep(3)

            # 간편 회원가입 선택
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeLink[`label == "간편 회원가입하기"`]').click()

            # 필수 약관 선택 후 가입 시도
            terms = wd.find_elements(AppiumBy.XPATH, '//XCUIElementTypeOther[@index="2"]/XCUIElementTypeOther')
            for required_term in terms:
                if '필수' in required_term.text:
                    required_term.click()
                else:
                    pass
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '동의하고 가입하기').click()

            # 기가입된 이메일 입력
            wd.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextField').send_keys(self.pconf['id_29cm'])

            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '동일한 이메일 주소로 가입된 계정이 있습니다. 기존 계정으로 로그인해주세요.')
                print('기가입된 계정으로 회원가입 실패 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('기가입된 계정으로 회원가입 실패 확인 실패')
                print('기가입된 계정으로 회원가입 실패 확인 실패')

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
            wd.get(self.conf['deeplink']['home'])

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data
