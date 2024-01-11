import logging
import os.path
import subprocess
import sys
import traceback
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec, wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import com_utils
from android_automation.page_action import my_page, login_page, navigation_bar, my_edit_user_info_page
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from android_automation.page_action.select_category_page import test_select_category
from time import sleep, time, strftime, localtime
from appium.webdriver.common.touch_action import TouchAction
from com_utils import values_control, slack_result_notifications, deeplink_control
from com_utils.element_control import aal, aalk, aalc, scroll_control
from com_utils.testrail_api import send_test_result


class LoginLogout:

    # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
    def test_email_login_error(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[이메일 로그인 실패] CASE 시작")
            # 하단 네비게이터에 MY 메뉴 진입
            sleep(1)
            wd.get('app29cm://mypage')
            sleep(1)
            print("홈 > 마이페이지 화면 진입")
            # 로그인 회원가입 버튼 선택
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtLogin').click()
            print("로그인 버튼 선택")
            sleep(3)
            # 로그인 화면 진입 확인
            login_page_title = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.widget.TextView[1]')
            print("홈 > 마이페이지 > 로그인 화면 진입")

            if login_page_title.text == '로그인':
                print("로그인 문구 확인")
            else:
                print("로그인 문구 실패")
                test_result = 'WARN'
                warning_texts.append("로그인 화면 진입 확인 실패")
            print(f"가이드 문구 : {login_page_title.text} ")

            # 잘못된 비밀번호 입력 후 로그인 하기 버튼 선택
            wd.find_element(By.XPATH, '//android.widget.EditText[1]').send_keys(self.pconf['LOGIN_SUCCESS_ID'])
            wd.find_element(By.XPATH, '//android.widget.EditText[2]').send_keys(self.pconf['LOGIN_FAILED_PW'])
            wd.find_element(By.XPATH, '//android.widget.Button').click()
            print("로그인 버튼 선택")
            # 로그인 실패 문구 확인
            guide_text = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.view.View[1]/android.widget.TextView')

            if "5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다." in guide_text.text:
                print("'5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다.’ 가이드 문구 노출 확인")
            else :
                print("'5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다.’ 가이드 문구 노출 실패")
                test_result = 'WARN'
                warning_texts.append("로그인 실패 가이드 문구 확인 실패")
            print(f"가이드 문구 : {guide_text.text} ")
            sleep(1)
            # 뒤로가기로 홈화면 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            sleep(3)
            print("[이메일 로그인 실패]CASE 종료")

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
            wd.get('//app29cm.29cm.co.kr/home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data
    def full_test_email_login_error(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            self.email_login_fail()

            # 하단 네비게이터에 MY 메뉴 진입
            sleep(1)
            wd.get('app29cm://mypage')
            sleep(1)
            print("홈 > 마이페이지 화면 진입")

            # 로그인 회원가입 버튼 선택
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtLogin').click()
            print("로그인 버튼 선택")
            sleep(3)

            # 로그인 화면 진입 확인
            login_page_title = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.widget.TextView[1]')
            print("홈 > 마이페이지 > 로그인 화면 진입")

            if login_page_title.text == '로그인':
                print("로그인 문구 확인")
            else:
                print("로그인 문구 실패")
                test_result = 'WARN'
                warning_texts.append("로그인 문구 확인 실패")
            print("가이드 문구 : %s " % login_page_title.text)

            # 미입력 후 로그인 하기 버튼 선택
            wd.find_element(By.XPATH, '//android.widget.Button').click()
            print("아이디, 비밀번호 미입력 후 로그인 버튼 선택")

            # 가이드 문구 확인 - 아이디를 입력해주세요
            guide_text = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.view.View/android.widget.TextView')

            if guide_text.text == '아이디를 입력하세요.':
                print("‘아이디를 입력하세요.’ 가이드 문구 노출 확인")
            else:
                print("‘아이디를 입력하세요.’ 가이드 문구 노출 실패")
                test_result = 'WARN'
                warning_texts.append("가이드 문구 확인 실패")
            print(f"가이드 문구 : {guide_text.text} ")

            # 비밀번호 입력 후 로그인 하기 버튼 선택
            wd.find_element(By.XPATH, '//android.widget.EditText[2]').send_keys(self.pconf['LOGIN_SUCCESS_PW'])
            print("패스워드 필드 입력")
            wd.find_element(By.XPATH, '//android.widget.Button').click()
            print("로그인 버튼 선택")
            # 가이드 문구 확인 - 아이디를 입력해주세요
            guide_text = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.view.View/android.widget.TextView')
            wd.find_element(By.XPATH, '//android.widget.EditText[2]').send_keys("")

            if guide_text.text == '아이디를 입력하세요.':
                print("‘아이디를 입력하세요.’ 가이드 문구 노출 확인")
            else:
                print("‘아이디를 입력하세요.’ 가이드 문구 노출 실패")
                test_result = 'WARN'
                warning_texts.append("가이드 문구 확인 실패")
            print(f"가이드 문구 : {guide_text.text} ")

            # 아이디 입력 후 로그인 하기 버튼 선택
            wd.find_element(By.XPATH, '//android.widget.EditText[1]').send_keys(self.pconf['LOGIN_SUCCESS_ID'])
            print("아이디 필드 입력")
            wd.find_element(By.XPATH, '//android.widget.Button').click()
            print("로그인 버튼 선택")

            # 가이드 문구 확인 - 비밀번호를 입력하세요
            guide_text = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.view.View/android.widget.TextView')

            if guide_text.text == '비밀번호를 입력하세요.':
                print("‘비밀번호를 입력하세요.’ 가이드 문구 노출 확인")
            else:
                print("'비밀번호를 입력하세요.’ 가이드 문구 노출 실패")
                test_result = 'WARN'
                warning_texts.append("가이드 문구 확인 실패")
            print(f"가이드 문구 : {guide_text.text} ")
            print("[이메일 로그인 실패] CASE 종료")

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
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data
    def test_email_login_success(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            sleep(1)

            # 로그인 페이지 진입
            com_utils.deeplink_control.move_to_my_Android(wd)
            my_page.enter_login_page(wd)

            # 올바른 아이디, 올바른 비밀번호 입력
            login_page.input_id_password(wd, self.pconf['LOGIN_SUCCESS_ID'], self.pconf['LOGIN_SUCCESS_PW'])

            # 프로필 이름 확인
            my_page.check_nickname(self, wd)

            # 회원 정보 수정 페이지 진입
            my_page.click_edit_user_info_menu(wd)

            # 비밀번호 재확인
            my_edit_user_info_page.input_password(wd, self.pconf['LOGIN_SUCCESS_PW'])
            my_edit_user_info_page.click_next_btn(wd)

            # 회원 정보 수정 페이지의 타이틀과 닉네임 확인
            my_edit_user_info_page.check_edit_page_title(wd)
            my_edit_user_info_page.check_edit_page_id(wd, self.pconf['MASKING_NAME'])

            # Home 으로 복귀
            my_edit_user_info_page.click_back_btn(wd)
            navigation_bar.move_to_home(wd)

            # 복귀 후, 홈 탭 진입 전 노출 화면 있는지 확인
            test_select_category(wd)

            print(f'[{test_name}] 테스트 종료')

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
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
            except Exception:
                pass
            wd.get('app29cm://home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '이메일 로그인 성공')
            return result_data
    def test_logout(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭 딥링크로 진입
            com_utils.deeplink_control.move_to_my_Android(wd)

            # 로그아웃 버튼 선택
            my_page.find_logout_btn(wd)
            my_page.click_logout_btn(wd)

            # 로그아웃 완료 > 로그인,회원가입 문구 확인
            my_page.find_login_btn(wd)
            my_page.check_login_btn(wd)

            # Home 으로 복귀 후,온보딩 프로그램 확인
            navigation_bar.logout_and_move_to_home(wd)
            print(f'[{test_name}] 테스트 종료')

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
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
            except Exception:
                pass
            wd.get('app29cm://home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '로그아웃')
            return result_data
    def Login_with_SNS(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("---------6.SNS 로그인 Adroid 에서 apple 계정 케이스 시작")
            sleep(5)

            # SNS 계정으로 로그인하기
            # 카카오톡
            # 네이버
            # 페이스북
            # 애플계정 - 팝업 확인
            wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.widget.Button[4]').click()
            #가이드 문구 확인 - 아이디를 입력해주세요
            guide_text = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.view.View/android.widget.TextView')
            print(f"가이드 문구 : {guide_text.text} ")

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
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def test_email_login_error_success(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # 로그인 페이지 진입
            com_utils.deeplink_control.move_to_my_Android(wd)
            my_page.enter_login_page(wd)

            # 올바른 이메일, 잘못된 비밀번호 입력하여 에러 문구 확인
            login_page.input_id_password(wd, self.pconf['LOGIN_SUCCESS_ID_1'], self.pconf['LOGIN_FAILED_PW'])
            login_page.check_login_error_text(self, wd)

            # 이메일, 비밀번호 입력값 제거
            login_page.clear_id_password(wd)

            # 올바른 아이디, 올바른 비밀번호 입력
            login_page.input_id_password(wd, self.pconf['LOGIN_SUCCESS_ID_1'], self.pconf['LOGIN_SUCCESS_PW'])

            # 프로필 이름 확인
            my_page.check_nickname(self, wd)

            # Home 으로 복귀
            navigation_bar.move_to_home(wd)

            # 복귀 후, 홈 탭 진입 전 노출 화면 있는지 확인
            test_select_category(wd)
            close_bottom_sheet(self.wd)

            print(f'[{test_name}] 테스트 종료')
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
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
            except Exception:
                pass
            wd.get('app29cm://home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '이메일 로그인 실패')
            return result_data