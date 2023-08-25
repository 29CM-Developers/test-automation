import os
import sys
import traceback

from time import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils import values_control


class Like:
    def test_no_like_item(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "LIKE"`]').click()

            # 화면 진입 시, 브랜드 추천 페이지 노출 여부 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '관심 브랜드를 선택하세요. 놀라운 추천 경험을 제공할게요.')
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()
                print('브랜드 추천 페이지 노출')
            except NoSuchElementException:
                pass

            # 상단 Like 개수 확인
            like_total_count = wd.find_element(AppiumBy.XPATH,
                                               '//XCUIElementTypeOther[@index="1"]/XCUIElementTypeStaticText[@index="2"]').text
            if like_total_count == '0':
                print('총 LIKE 개수 확인')
            else:
                print('총 LIKE 개수 확인 실패')

            # Product 탭 선택
            # wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="PRODUCT (0)"]').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '좋아요한 상품이 없습니다. 마음에 드는 상품의 하트를 눌러보세요.')
                print('PRODUCT 좋아요 없음 문구 노출 확인')
            except NoSuchElementException:
                print('PRODUCT 좋아요 없음 문구 노출 확인 실패')

            # Brand 탭 선택
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="BRAND (0)"]').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '좋아요한 브랜드가 없어요.')
                print('BRAND 좋아요 없음 문구 노출 확인')
            except NoSuchElementException:
                print('BRAND 좋아요 없음 문구 노출 확인 실패')

            # POST 탭 선택
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="POST (0)"]').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '좋아요한 게시물이 없습니다. 다시 보고 싶은 게시물에 하트를 눌러보세요.')
                print('POST 좋아요 없음 문구 노출 확인')
            except NoSuchElementException:
                print('POST 좋아요 없음 문구 노출 확인')

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
