import os.path
import sys
import traceback

from time import sleep, time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from com_utils import values_control


class UserLoginTest:

    def input_id_password(self, wd, id, password):

        wd.find_element(AppiumBy.IOS_PREDICATE, 'value=="아이디 (이메일)"').send_keys(id)
        wd.find_element(AppiumBy.IOS_PREDICATE, 'value=="비밀번호"').send_keys(password)
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인하기').click()

    def test_email_login_error(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            # 로그인 페이지 진입
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()
            sleep(3)

            # 올바른 이메일, 잘못된 비밀번호 입력하여 에러 문구 확인
            UserLoginTest.input_id_password(self, wd, self.pconf['id_29cm'], self.pconf['error_password_29cm'])
            sleep(1)
            error = wd.find_element(AppiumBy.XPATH,
                                    '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText').text
            error_login_text = "5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다."

            if error_login_text in error:
                print("이메일 로그인 실패 확인")
            else:
                print("이메일 로그인 실패 확인 불가")

            # Home으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="HOME"]').click()

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
            wd.get('app29cm://home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data

    def test_email_login_success(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            # 로그인 페이지 진입
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()
            sleep(3)

            # 올바른 아이디, 올바른 비밀번호 입력
            UserLoginTest.input_id_password(self, wd, self.pconf['id_29cm'], self.pconf['password_29cm'])
            sleep(1)

            # 프로필 이름 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '정다정')
                print("로그인 성공")
            except:
                print("로그인 실패")

            # Home 으로 복귀
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="HOME"]').click()

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
            wd.get('app29cm://home')

        finally:
            run_time = f"{time() - start_time:.2f}"
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data

    def test_logout(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            # My 탭 진입
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '정다정')
                print("로그인 유저")
            except:
                print("비로그인 유저")

            # 로그아웃 버튼 선택
            wd.execute_script('mobile:swipe', {'direction': 'up'})
            wd.execute_script('mobile:swipe', {'direction': 'up'})
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="LOGOUT"]').click()

            # 로그아웃 완료 후 문구 확인
            wd.execute_script('mobile:swipe', {'direction': 'down'})
            wd.execute_script('mobile:swipe', {'direction': 'down'})
            try:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="로그인·회원가입"]')
                print('로그아웃 완료')
            except NoSuchElementException:
                print('로그아웃 실패')

            # Home 으로 복귀
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="HOME"]').click()

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
            wd.get('app29cm://home')

        finally:
            run_time = f"{time() - start_time:.2f}"
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data


