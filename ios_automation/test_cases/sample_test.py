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

    def default_test(self, wd, error_text=''):

        id_29cm = 'dajjeong@29cm.co.kr'
        password_29cm = '29CMdajjeong!'

        try:
            sleep(3)

            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()

            sleep(2)
            wd.find_element(AppiumBy.IOS_PREDICATE, 'value=="아이디 (이메일)"').send_keys(id_29cm)
            wd.find_element(AppiumBy.IOS_PREDICATE, 'value=="비밀번호"').send_keys(password_29cm)
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
