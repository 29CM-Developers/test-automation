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
                print('홈화면 추천 탭 타이틀 확인')
            except NoSuchElementException:
                print('홈화면 추천 탭 타이틀 확인 실패')
                pass

            # 우먼 카테고리 탭 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '우먼').click()

            # 첫번째 피드의 첫번째 상품의 좋아요 xpath와 좋아요 수 xpath
            content_like_xpath = '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeOther[@index="2"]/XCUIElementTypeButton[@index="4"]'
            content_like_count_xpath = f'{content_like_xpath}/XCUIElementTypeStaticText'

            # 좋아요 버튼 선택 전, 좋아요 수 저장
            content_like_count = wd.find_element(AppiumBy.XPATH, content_like_count_xpath).text
            content_like_count = int(content_like_count.replace(',', ''))

            # 좋아요 선택 후, 좋아요 수 비교 확인
            wd.find_element(AppiumBy.XPATH, content_like_xpath).click()
            content_like_select = wd.find_element(AppiumBy.XPATH, content_like_count_xpath).text
            content_like_select = int(content_like_select.replace(',', ''))
            if content_like_select == content_like_count+1:
                print('좋아요 선택 후 카운트 증가 확인')
            else:
                print('좋아요 선택 후 카운트 증가 확인 실패')

            # 좋아요 취소 후, 좋아요 수 비교 확인
            wd.find_element(AppiumBy.XPATH, content_like_xpath).click()
            content_like_select = wd.find_element(AppiumBy.XPATH, content_like_count_xpath).text
            content_like_select = int(content_like_select.replace(',', ''))
            if content_like_select == content_like_count:
                print("좋아요 취소 후 카운트 차감 확인")
            else:
                print("좋아요 취소 후 카운트 차감 확인 실패")

            # 첫번째로 노출되는 컨텐츠의 텍스트 확인
            content = '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeOther[@index="1"]/XCUIElementTypeStaticText'
            content_text = wd.find_element(AppiumBy.XPATH, content).text
            print(content_text)

            # 피드 2번 스크롤
            wd.execute_script('mobile:swipe', {'direction': 'up'})
            wd.execute_script('mobile:swipe', {'direction': 'up'})

            # 피드 정보 불러와서 텍스트 노출 확인 (최대 5번까지 확인, 찾지 못하면 실패)
            # API 확인 후에 시나리오 수정 필요 -> 노출 시켜주는 컨텐츠 불러와서 비교 확인
            i = 0
            while i < 5:
                try:
                    scroll_content = wd.find_element(AppiumBy.XPATH, content)
                    if content_text != scroll_content.text:
                        print(scroll_content.text)
                        print('피드 추가 노출 확인')
                    else:
                        print('피드 추가 노출 확인 실패')
                    break
                except NoSuchElementException:
                    wd.execute_script('mobile:swipe', {'direction': 'up'})
                    print('피드 텍스트 확인 안되어 스크롤')
                    i += 1

            sleep(3)

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
