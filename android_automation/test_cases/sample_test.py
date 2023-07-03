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
            sleep(3)

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'MY').click()

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
