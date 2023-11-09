import logging
import os.path
import sys
import traceback
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time
from com_utils import values_control, slack_result_notifications, element_control


class Join:

    # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
    def test_simple_membership_registration_failure(self, wd, test_result='PASS', error_texts=[], img_src='',
                                                    warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[간편 회원 가입 실패] CASE 시작")
            # 하단 네비게이터에 MY 메뉴 진입
            sleep(2)
            wd.get('app29cm://mypage')
            sleep(2)
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

            # 간편 회원가입하기 버튼 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '간편 회원가입하기').click()
            print("간편 회원가입하기 버튼 선택")

            # 이용 약관 모두 동의 선택
            try:
                wd.find_element(By.XPATH, "//*[contains(@text, 'all')]").click()
                print('이용 약관 모두 동의 선택')
            except NoSuchElementException:
                wd.find_element(By.XPATH,
                                "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View").click()
                print('이용 약관 모두 동의 선택xpath로')

            # 동의하고 가입하기 선택
            wd.find_element(By.XPATH, "//*[contains(@text, '동의하고 가입하기')]").click()
            print('동의하고 가입하기 선택')
            sleep(2)
            wd.find_element(AppiumBy.CLASS_NAME, 'android.widget.EditText').send_keys(self.pconf['LOGIN_SUCCESS_ID'])
            sleep(1)
            try:
                wd.find_element(By.XPATH, "//*[contains(@text, '동일한 이메일 주소로 가입된 계정이 있습니다. 기존 계정으로 로그인해주세요.')]")
                print("기가입된 계정으로 회원가입 실패 확인 성공")
            except NoSuchElementException:
                print("기가입된 계정으로 회원가입 실패 확인 실패")
                test_result = 'WARN'
                warning_texts.append("기가입된 계정으로 회원가입 실패 확인 실패")

            # 뒤로가기로 홈화면 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            sleep(3)
            wd.get('app29cm://home')
            print("[간편 회원 가입 실패]CASE 종료")

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
