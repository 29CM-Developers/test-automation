
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
        print(f'[{test_name}] 테스트 시작')

        try:
            # 홈화면 배너 API 호출
            response = requests.get(
                f'https://content-api.29cm.co.kr/api/v4/banners?bannerDivision=HOME_MOBILE&gender={self.pconf["gender"]}')
            if response.status_code == 200:
                # 호출한 API의 모든 배너 타이틀 저장
                banner_api_data = response.json()
                banner_count = int(banner_api_data['data']['count'])

                banner_api = []
                for i in range(0, banner_count):
                    banner_title_api = banner_api_data['data']['bannerList'][i]['bannerTitle']
                    if banner_title_api == 'ㅤ':
                        pass
                    else:
                        banner_api.append(banner_title_api)

                # 홈화면 배너 타이틀 모두 저장
                banner_home = []
                for i in range(0, banner_count):
                    sleep(1.5)
                    try:
                        banner_title = wd.find_element(AppiumBy.XPATH,
                                                            '//XCUIElementTypeCollectionView[@index="4"]/XCUIElementTypeCell[1]/XCUIElementTypeOther')
                        banner_title_text = banner_title.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@index="1"]').text
                        banner_home.append(banner_title_text)
                    except Exception:
                        print('타이틀 확인 실패하여 이전 배너로 스와이프')
                        # 에러 발생하여 타이틀 확인 실패 시, 이전 배너로 스와이프하여 타이틀 저장
                        banner = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView')
                        com_utils.element_control.swipe_left_to_right(wd, banner)
                        banner_title_text = wd.find_element(AppiumBy.XPATH,
                                                        '//XCUIElementTypeCollectionView[@index="4"]/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="1"]').text
                        banner_home.append(banner_title_text)

                # API 호출 배너 리스트와 저장된 홈 배너 리스트 비교 (저장한 홈 배너 리스트 안에 호출한 리스트가 포함되면 pass)
                if set(banner_api).issubset(set(banner_home)):
                    print('홈 배너 확인')
                else:
                    test_result = 'WARN'
                    error_texts = '홈 배너 확인 실패'
                    print(f'홈 배너 확인 실패: {set(banner_api).difference(set(banner_home))} / {set(banner_home).difference(set(banner_api))}')
            else:
                test_result = 'WARN'
                warning_texts.append('피드 컨텐츠 API 불러오기 실패')
                print('피드 컨텐츠 API 불러오기 실패')

            # 다이나믹 게이트 -> 센스있는 선물하기 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '센스있는 선물하기').click()

            sleep(3)
            print("!! 상단 타이틀 비교 진행 필요")

            # 웹뷰 요소가 잡히지 않아 비교할 요소값 확인 불가
            # 아래 뒤로가기 동작 안함
            # wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()

            # 뒤로가기 버튼 동작하지 않아 딥링크 사용하여 Home으로 이동
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
        print(f'[{test_name}] 테스트 시작')

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

            # 홈화면 우먼 탭 컨텐츠 API 호출하여 2번째 contents 피드 정보 저장
            response = requests.get(
                'https://content-api.29cm.co.kr/api/v5/feeds?experiment=&feed_sort=WOMEN&home_type=APP_HOME&limit=20&offset=0')
            if response.status_code == 200:
                contents_api_data = response.json()
                feed_item_contents = contents_api_data['data']['results']

                # feedType이 contents인 두번째 피드 정보 저장
                global feed_contents_api
                for i in range(1, 10):
                    feed_contents_type = feed_item_contents[i]['feedType']
                    if feed_contents_type == 'contents':
                        feed_contents_api = feed_item_contents[i]['feedContents']
                        break
                    else:
                        pass

                # 저장한 피드 정보와 동일한 피드 정보가 노출 될 때까지 스크롤
                for i in range(0, 10):
                    try:
                        feed_contents = wd.find_element(AppiumBy.XPATH,
                                               '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeOther[@index="1"]/XCUIElementTypeStaticText').text
                        if feed_contents_api == feed_contents:
                            print('피드 컨텐츠 추가 노출 확인')
                            break
                        else:
                            wd.execute_script('mobile:swipe', {'direction': 'up'})
                            print('피드 텍스트 확인 안되어 스크롤')
                            i += 1
                    except NoSuchElementException:
                        wd.execute_script('mobile:swipe', {'direction': 'up'})
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











