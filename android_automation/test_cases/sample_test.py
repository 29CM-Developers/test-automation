import os.path
import sys
import traceback

from difflib import SequenceMatcher
from time import sleep, time
from appium.webdriver.common.appiumby import AppiumBy
from com_utils import values_control
from com_utils.code_optimization import finally_opt, exception_control


class AutomationTesting:
    def default_test(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = sys._getframe().f_code.co_name
        start_time = time()
        try:

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'MY').click()
        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      'PLP 기능 확인')
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
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      '좋아요 존재하는 LIKE 화면 확인')
            return result_data