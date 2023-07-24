import os
import sys
import traceback
from time import time, sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

from com_utils import values_control


class NotLoginUserTest:

    def check_login_page(self, wd):
        test_name = sys._getframe().f_code.co_name

        sleep(2)

        try:
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인하기')
            result = f'{test_name}: Pass'
        except NoSuchElementException:
            result = f'{test_name}: Fail'

        wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()

        return result

    def test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = sys._getframe().f_code.co_name
        start_time = time()

        try:
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="CATEGORY"]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '상의').click()
            wd.find_element(AppiumBy.XPATH, '(//XCUIElementTypeButton[@name="icHeartLine"])[2]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="확인"]').click()
            sleep(2)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()

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

    def test_not_login_user_possible(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = sys._getframe().f_code.co_name
        start_time = time()

        try:
            sleep(1)

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

        finally:
            run_time = f"{time() - start_time:.2f}"
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data

    def full_test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = sys._getframe().f_code.co_name
        start_time = time()

        try:
            sleep(1)

            # 주요 시나리오
            NotLoginUserTest.test_not_login_user_impossible(self, wd)

            # 속도를 위해 MY 탭으로 시작 위치 변경
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()

            # 상단 네비게이션 알림 버튼 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarNotiWhite').click()
            NotLoginUserTest.check_login_page(self, wd)

            # 상단 네비게이션 장바구니 버튼 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarCartWhite').click()
            print(NotLoginUserTest.check_login_page(self, wd))

            # LIKE 탭 선택
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="LIKE"]').click()
            NotLoginUserTest.check_login_page(self, wd)

            # PDP > 구매하기 선택
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="CATEGORY"]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '상의').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]').click()
            sleep(2)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '구매하기').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '바로 구매하기').click()

            try:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="쿠폰"]')
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '닫기').click()
            except NoSuchElementException:
                print("쿠폰 없음")
            print(NotLoginUserTest.check_login_page(self, wd))


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

    def test(self, wd):
        wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="CATEGORY"]').click()
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '상의').click()
        wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]').click()
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '구매하기').click()
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '바로 구매하기').click()

        try:
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="쿠폰"]')
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '닫기').click()
        except NoSuchElementException:
            print("쿠폰 없음")

        print(NotLoginUserTest.check_login_page(self, wd))
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()






