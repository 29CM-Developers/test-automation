
import os
import sys
import traceback
from time import time, sleep

import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException

import com_utils.element_control
from com_utils import values_control


class Home:

    def test_home_banner(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        print(f'{test_name} 테스트 시작')

        try:
            # 홈 배너 API 호출하여 5번째 배너 타이틀 저장
            response = requests.get('https://content-api.29cm.co.kr/api/v4/banners?bannerDivision=HOME_MOBILE')
            if response.status_code == 200:
                banner_api_data = response.json()
                banner_title_api = banner_api_data['data']['bannerList'][4]['bannerTitle']

                # 스와이프하여 동일한 배너 타이틀 탐색
                for i in range(1, 20):
                    try:
                        wd.find_element(AppiumBy.ACCESSIBILITY_ID, banner_title_api)
                        print('홈화면 상단 배너 좌우 슬라이드 확인')
                        break
                    except NoSuchElementException:
                        banner = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView')
                        com_utils.element_control.swipe_right_to_left(wd, banner)
                        print('피드 텍스트 확인 안되어 스와이프')
                        i += 1
            else:
                test_result = 'WARN'
                warning_texts.append('피드 컨텐츠 API 불러오기 실패')
                print('피드 컨텐츠 API 불러오기 실패')

            # 다이나믹 게이트 -> 센스있는 선물하기 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '센스있는 선물하기').click()

            # 웹뷰 요소가 잡히지 않아 비교할 요소값 확인 불가
            # 아래 뒤로가기 동작 안함
            # wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()

            wd.get('app29cm://home')

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

    def test_home_contents(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        print(f'{test_name} 테스트 시작')

        try:
            wd.execute_script('mobile:swipe', {'direction': 'up'})
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '추천').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, f'{self.pconf["nickname"]}님을 위한 추천 상품')
                print('홈화면 추천 탭 타이틀 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('홈화면 추천 탭 타이틀 확인 실패')
                print('홈화면 추천 탭 타이틀 확인 실패')

            # 우먼 카테고리 탭 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '우먼').click()

            # 첫번째 피드의 첫번째 상품의 좋아요 xpath와 좋아요 수 xpath
            content_like_xpath = '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeOther[@index="2"]/XCUIElementTypeButton[@index="4"]'
            content_like_count_xpath = f'{content_like_xpath}/XCUIElementTypeStaticText'

            # 좋아요 버튼 선택 전, 좋아요 수 저장
            content_like_count = wd.find_element(AppiumBy.XPATH, content_like_count_xpath).text
            content_like_count = int(content_like_count.replace(',', ''))

            # 좋아요 버튼 선택 -> 찜하기 등록
            wd.find_element(AppiumBy.XPATH, content_like_xpath).click()
            content_like_select = wd.find_element(AppiumBy.XPATH, content_like_count_xpath).text
            content_like_select = int(content_like_select.replace(',', ''))
            if content_like_select == content_like_count+1:
                print('피드 아이템 좋아요 개수 증가 확인')
                pass
            else:
                test_result = 'WARN'
                warning_texts.append('피드 아이템 좋아요 개수 증가 확인 실패')
                print('피드 아이템 좋아요 개수 증가 확인 실패')

            # 좋아요 버튼 선택 -> 찜하기 해제
            wd.find_element(AppiumBy.XPATH, content_like_xpath).click()
            content_like_select = wd.find_element(AppiumBy.XPATH, content_like_count_xpath).text
            content_like_select = int(content_like_select.replace(',', ''))
            if content_like_select == content_like_count:
                print('피드 아이템 좋아요 개수 차감 확인')
                pass
            else:
                test_result = 'WARN'
                warning_texts.append('피드 아이템 좋아요 개수 차감 확인 실패')
                print('피드 아이템 좋아요 개수 차감 확인 실패')

            # 홈화면 우먼 탭 컨텐츠 API 호출하여 7번째 피드 정보 저장
            response = requests.get(
                'https://content-api.29cm.co.kr/api/v5/feeds?experiment=&feed_sort=WOMEN&home_type=APP_HOME&limit=20&offset=0')
            if response.status_code == 200:
                contents_api_data = response.json()
                feed_item_contents = contents_api_data['data']['results']
                feed_item_contents_text = feed_item_contents[7]['feedContents']
                # 7번째 피드 노출 될 때까지 스크롤
                for i in range(0, 10):
                    try:
                        wd.find_element(AppiumBy.ACCESSIBILITY_ID, feed_item_contents_text)
                        print('피드 컨텐츠 추가 노출 확인')
                        break
                    except NoSuchElementException:
                        wd.execute_script('mobile:swipe', {'direction': 'up'})
                        print('피드 텍스트 확인 안되어 스크롤')
                        i += 1
            else:
                test_result = 'WARN'
                warning_texts.append('피드 컨텐츠 API 불러오기 실패')
                print('피드 컨텐츠 API 불러오기 실패')

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



