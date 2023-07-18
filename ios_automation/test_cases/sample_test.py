import os.path
import sys
import traceback

from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class AutomationTesting:

    id_29cm = 'dajjeong@29cm.co.kr'
    password_29cm = '29CMdajjeong!'
    error_id_29cm = 'dajeong@29cm.co.kr'
    error_password_29cm = '30CMdajjeong@'

    def login_test(self, wd, error_text=''):

        try:
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()

            sleep(2)

            wd.find_element(AppiumBy.IOS_PREDICATE, 'value=="아이디 (이메일)"').send_keys(AutomationTesting.id_29cm)
            wd.find_element(AppiumBy.IOS_PREDICATE, 'value=="비밀번호"').send_keys(AutomationTesting.password_29cm)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인하기').click()

            sleep(2)

            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="LOGOUT"]').click()

            sleep(3)

        except Exception:
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc()
        finally:
            return error_text

    def id_error_test(self, wd, error_text=''):
        try:
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()

            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()

            sleep(2)

            wd.find_element(AppiumBy.IOS_PREDICATE, 'value=="아이디 (이메일)"').send_keys(AutomationTesting.error_id_29cm)
            wd.find_element(AppiumBy.IOS_PREDICATE, 'value=="비밀번호"').send_keys(AutomationTesting.password_29cm)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인하기').click()

            sleep(2)

            error = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText').text
            error_login_text = "5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다."
            print(error)

            if error_login_text in error:
                print("Pass")
            else:
                print("Fail")

            sleep(3)

        except Exception:
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc()
        finally:
            return error_text




    def scroll_test(self, wd, error_text=''):
        try:
            wd.execute_script('mobile:swipe', {'direction': 'up'})
            wd.execute_script('mobile:swipe', {'direction': 'down'})


        except Exception:
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc()
        finally:
            return error_text
