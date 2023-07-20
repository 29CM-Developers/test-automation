import os.path
import subprocess
import sys
import traceback

from difflib import SequenceMatcher
from time import sleep, time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from com_utils import values_control


class AutomationTesting:
    def default_test(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = sys._getframe().f_code.co_name
        start_time = time()
        try:

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'MY').click()
        except Exception:
            test_result = 'FAIL'
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
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

    def re_search_element(self, button_element):
        # 버튼 텍스트 가져오기
        button_text = button_element.text

        # 유사한 텍스트를 찾기 위한 기준값 설정
        similarity_threshold = 0.8

        # 버튼 요소 주변 요소 찾기
        sibling_elements = self.wd.find_elements_by_xpath('following-sibling::* | preceding-sibling::*')

        # 주변 요소에서 유사한 텍스트 찾기
        similar_text = None
        for sibling_element in sibling_elements:
            sibling_text = sibling_element.text
            if SequenceMatcher(None, button_text, sibling_text).ratio() > similarity_threshold:
                similar_text = sibling_text
                break

        if similar_text:
            print(f"주변 요소에서 '{similar_text}' 텍스트를 찾았습니다.")
        else:
            print("주변 요소에서 유사한 텍스트를 찾을 수 없습니다.")

        return sibling_element

    def default_fail_test(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = sys._getframe().f_code.co_name
        start_time = time()
        try:
            sleep(1)

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'FAIL').click()
        except Exception:
            test_result = 'FAIL'
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
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