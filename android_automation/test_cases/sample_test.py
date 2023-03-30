import os.path
import subprocess
import sys
import traceback

from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class AutomationTesting:
    def default_test(self, wd, error_text=''):
        try:
            # 요소 찾기 & 사용
            wd.find_element(AppiumBy.ID, '').click()
            wd.find_element(AppiumBy.XPATH, '').text
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '').send_keys('')
            wd.find_element(AppiumBy.ID, '').screenshot('filename.png')

            # xpath query
            '//*[contains(@text, "찾을단어"]'
            '//*[contains(@content-desc, "찾을단어"]'
            '//*[@text="찾을단어"]'
            # 해당 요소의 부모 요소 찾기
            '//android.widget.TextView/..'

            # 요소 대기
            wait = WebDriverWait(wd, 5)
            wait.until(ec.visibility_of_element_located((AppiumBy.ID, ''))).click()
            wait.until(ec.element_to_be_clickable((AppiumBy.XPATH, ''))).click()
            sleep(1)

            # adb shell 전화 받기
            subprocess.call('adb -s {udid} shell input keyevent 5')

        except Exception:
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc()
        finally:
            return error_text