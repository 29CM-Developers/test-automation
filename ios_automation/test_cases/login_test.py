import os.path
import sys
import traceback
import json

from time import sleep, time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from com_utils import values_control


class UserLoginTest:

    def input_id_password(self, wd, id, password):

        wd.find_element(AppiumBy.IOS_PREDICATE, 'value=="아이디 (이메일)"').send_keys(id)
        wd.find_element(AppiumBy.IOS_PREDICATE, 'value=="비밀번호"').send_keys(password)
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인하기').click()

    def test_login_error(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = sys._getframe().f_code.co_name
        start_time = time()

        try:
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, "닫기").click()
            except NoSuchElementException:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()

            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()

            sleep(1)

            UserLoginTest.input_id_password(self, wd, self.pconf['error_id_29cm'], self.pconf['password_29cm'])

            sleep(1)

            error = wd.find_element(AppiumBy.XPATH,
                                    '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText').text
            error_login_text = "5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다."
            print(error)

            if error_login_text in error:
                print(test_name + ": Pass")
            else:
                print(test_name + ": Fail")

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
            except Exception:
                pass

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data

    def test_login(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = sys._getframe().f_code.co_name
        start_time = time()

        try:
            sleep(1)
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()

            sleep(1)

            UserLoginTest.input_id_password(self, wd, self.pconf['id_29cm'], self.pconf['password_29cm'])

            sleep(1)

            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="LOGOUT"]').click()

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

        finally:
            run_time = f"{time() - start_time:.2f}"
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data

    def full_test_login_error(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = sys._getframe().f_code.co_name
        start_time = time()

        try:
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()

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

        finally:
            run_time = f"{time() - start_time:.2f}"
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data


