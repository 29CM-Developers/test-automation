import os
import sys
import traceback
from time import time, sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils import values_control


class Home:

    def test_home_contents(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            # 추천 카테고리 탭 선택
            wd.execute_script('mobile:swipe', {'direction': 'up'})
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '추천').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, f'{self.pconf["nickname"]}님을 위한 추천 상품')
                print("홈화면 추천 탭 타이틀 확인")
            except NoSuchElementException:
                print("홈화면 추천 탭 타이틀 확인 실패")
                pass

            # 우먼 카테고리 탭 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '우먼').click()

            # 첫번째 피드의 첫번째 상품의 좋아요 xpath와 좋아요 수 확인
            feed_like_xpath = '//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther[@index="2"]/XCUIElementTypeButton[@index="4"]'
            feed_like_count_xpath = f'{feed_like_xpath}/XCUIElementTypeStaticText'
            feed_like = wd.find_element(AppiumBy.XPATH, feed_like_xpath)
            feed_like_count = wd.find_element(AppiumBy.XPATH, feed_like_count_xpath).text
            feed_like_count = int(feed_like_count.replace(',', ''))

            # 좋아요 선택 후, 좋아요 수 비교 확인
            feed_like.click()
            feed_like_select = wd.find_element(AppiumBy.XPATH, feed_like_count_xpath).text
            feed_like_select = int(feed_like_select.replace(',', ''))
            if feed_like_select == feed_like_count+1:
                print("좋아요 선택 후 카운트 확인")
            else:
                print("좋아요 선택 후 카운트 확인 실패")

            # 좋아요 취소 후, 좋아요 수 비교 확인
            feed_like.click()
            feed_like_select = wd.find_element(AppiumBy.XPATH, feed_like_count_xpath).text
            feed_like_select = int(feed_like_select.replace(',', ''))
            if feed_like_select == feed_like_count:
                print("좋아요 취소 후 카운트 확인")
            else:
                print("좋아요 취소 후 카운트 확인 실패")

            # 피드 스크롤
            wd.execute_script('mobile:swipe', {'direction': 'up'})

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
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data
