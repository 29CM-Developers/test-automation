import os.path
import sys
import traceback

from time import sleep, time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from com_utils import values_control


class UserLoginTest:

    def input_id_password(self, wd, id, password):

        wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeTextField[@index="0"]').send_keys(id)
        wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeSecureTextField[@index="1"]').send_keys(password)
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인하기').click()

    def test_email_login_error(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 로그인 페이지 진입
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()
            sleep(3)

            # 올바른 이메일, 잘못된 비밀번호 입력하여 에러 문구 확인
            UserLoginTest.input_id_password(self, wd, self.pconf['id_29cm'], self.pconf['error_password_29cm'])
            sleep(3)
            error = wd.find_element(AppiumBy.XPATH,
                                    '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText').text

            if self.conf['login_error_text'] in error:
                print("이메일 로그인 실패 확인")
            elif self.conf['login_exceeded_text'] in error:
                print("이메일 로그인 실패 확인")
            else:
                test_result = 'WARN'
                warning_texts.append('이메일 로그인 실패 확인 실패')
                print("이메일 로그인 실패 확인 실패")

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
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def test_email_login_success(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 로그인 페이지 진입
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()
            sleep(3)

            # 올바른 아이디, 올바른 비밀번호 입력
            UserLoginTest.input_id_password(self, wd, self.pconf['id_29cm'], self.pconf['password_29cm'])
            sleep(3)

            # 프로필 이름 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, self.pconf['nickname'])
                print("이메일 로그인 성공 확인")
            except:
                test_result = 'WARN'
                warning_texts.append('이메일 로그인 성공 확인 실패')
                print("이메일 로그인 성공 확인 실패")

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
            wd.get('app29cm://mypage')
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, self.pconf['nickname'])
                print("로그인 유저")
            except:
                pass
                print("비로그인 유저")

            # 로그아웃 버튼 선택
            for i in range(0, 5):
                try:
                    logout_btn = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="LOGOUT"]')
                    logout_btn.click()
                    break
                except NoSuchElementException:
                    wd.execute_script('mobile:swipe', {'direction': 'up'})

            # 로그아웃 완료 후 문구 확인
            for i in range(0, 5):
                try:
                    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="로그인·회원가입"]')
                    break
                except NoSuchElementException:
                    wd.execute_script('mobile:swipe', {'direction': 'down'})
            try:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="로그인·회원가입"]')
                print('로그아웃 성공 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('로그아웃 성공 확인 실패')
                print('로그아웃 성공 확인')

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
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()
            sleep(3)

            # 올바른 이메일, 잘못된 비밀번호 입력하여 에러 문구 확인
            UserLoginTest.input_id_password(self, wd, self.pconf['id_29cm'], self.pconf['error_password_29cm'])
            sleep(3)
            error = wd.find_element(AppiumBy.XPATH,
                                    '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText').text

            if self.conf['login_error_text'] in error:
                print("이메일 로그인 실패 확인")
            elif self.conf['login_exceeded_text'] in error:
                print("이메일 로그인 실패 확인")
            else:
                test_result = 'WARN'
                warning_texts.append('이메일 로그인 실패 확인 실패')
                print("이메일 로그인 실패 확인 실패")

            # 이메일, 비밀번호 입력값 제거
            wd.find_element(AppiumBy.XPATH,
                            '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeTextField[@index="0"]').clear()
            wd.find_element(AppiumBy.XPATH,
                            '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeSecureTextField[@index="1"]').clear()

            # 올바른 아이디, 올바른 비밀번호 입력
            UserLoginTest.input_id_password(self, wd, self.pconf['id2_29cm'], self.pconf['password_29cm'])
            sleep(3)

            # 프로필 이름 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, self.pconf['nickname'])
                print("이메일 로그인 성공 확인")
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('이메일 로그인 성공 확인 실패')
                print("이메일 로그인 성공 확인 실패")

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
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data




