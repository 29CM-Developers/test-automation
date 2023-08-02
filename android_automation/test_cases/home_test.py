import logging
import os.path
import subprocess
import sys
import traceback
import logging

import requests
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.mobileby import MobileBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from com_utils import values_control, element_control
from time import sleep, time

logger = logging.getLogger(name='Log')
logger.setLevel(logging.INFO)  ## 경고 수준 설정
formatter = logging.Formatter('|%(name)s||%(lineno)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

stream_handler = logging.StreamHandler()  ## 스트림 핸들러 생성
stream_handler.setFormatter(formatter)  ## 텍스트 포맷 설정
logger.addHandler(stream_handler)  ## 핸들러 등록

class Home:

    def test_home_banner(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[홈화면 배너 확인]CASE 시작")
            sleep(2)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()
            print("홈 탭 선택")
            txtFeedBannerTitle1 = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtFeedBannerTitle').text
            print(f"현재 피드 타이틀 : {txtFeedBannerTitle1} ")
            element_control.swipe_left_to_right(wd)
            print("왼쪽에서 오른쪽으로 스와이프")
            txtFeedBannerTitle2 = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtFeedBannerTitle').text
            print(f"스와이프 후 피드 타이틀 : {txtFeedBannerTitle2} ")
            if txtFeedBannerTitle1 != txtFeedBannerTitle2:
                print("상단 배너 좌우 슬라이드 확인")
            else:
                print("상단 배너 좌우 슬라이드 확인 실패")
            home_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtShowAll').text
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtShowAll').click()
            next_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/rootView')
            print("모아보기 화면 진입")
            next_layer_title = wd.find_element(AppiumBy.XPATH,'//*[@resource-id="__next"]/android.widget.TextView[@index=0]').text
            if next_layer_title == home_title:
                print(f"모아보기 진입 확인 : {next_layer_title} 노출 확인")
                print("모아보기 버튼 선택하여 모아보기 페이지 진입 확인")
            else:
                print(f"모아보기 진입 확인 실패 : {next_layer_title} 노출")
            # 뒤로가기로 홈화면 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            sleep(3)
            # 4. 다이나믹 게이트 2번째 줄, 1번째 선택
            dynamic_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/dynamicItems')
            dynamic_button_title = dynamic_layer.find_element(AppiumBy.XPATH, '//android.widget.LinearLayout[1]/androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.widget.TextView').text
            dynamic_layer.find_element(AppiumBy.XPATH, '//android.widget.LinearLayout[1]/androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.widget.TextView').click()
            sleep(3)
            gift_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/rootView')
            gift_title = gift_layer.find_element(AppiumBy.XPATH, '//android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.widget.TextView').text



            print("[홈화면 배너 확인]CASE 종료")

            # 확인 실패 시, 테스트 종료되지는 않지만 테스트 종료 후 확인이 필요한 경우
            # 테스트 결과 WARN으로 변경 -> 예시
            # 확인이 필요한 지점에 코드 작성
            # test_scenario = '확인할 테스트 시나리오 (ex. 홈화면 피드 상품의 좋아요 버튼 선택)'
            # try:
            #     testcode
            # except NoSuchElementException:
            #     test_result = 'WARN'
            #     warning_texts.append(test_scenario)

        except Exception:
            # 오류 발생 시 테스트 결과를 실패로 한다
            test_result = 'FAIL'
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc().split('\n')
            try:
                # 에러메시지 분류 시 예외처리
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
            except Exception:
                pass
            wd.get('//app29cm.29cm.co.kr/home')

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data

    def test_home_contents(self, wd, test_result='PASS', error_texts=[], img_src=''):

        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[홈화면 컨텐츠 확인]CASE 시작")
            sleep(5)
            tab_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/tabLayout')
            rec_tab_title = tab_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[4]/android.view.ViewGroup/android.widget.TextView').text
            women_tab_title = tab_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.TextView').text
            # 2. 홈 > 피드 > 추천 탭선택
            # tab_title_elements = wd.find_elements(AppiumBy.XPATH, '//*[@resource-id="com.the29cm.app29cm:id/tabTitle"]')
            tab_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[4]/android.view.ViewGroup/android.widget.TextView').click()
            print('홈 > 피드 > 추천 탭선택 ')
            guide_text = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/textRecommend')

            if guide_text.text == self.pconf['NAME']+'님을 위한 추천 상품':
                print(f"'{self.pconf['NAME']}님을 위한 추천 상품’ 가이드 문구 노출 확인")
            else:
                print(f"'{self.pconf['NAME']}님을 위한 추천 상품’ 가이드 문구 노출 실패")
            print(f"가이드 문구 : {guide_text.text} ")

            tab_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.TextView').click()
            print('홈 > 피드 > 우먼 탭선택 ')
            sleep(1)
            # 스크롤
            element_control.scroll_to_element_id(wd, 'com.the29cm.app29cm:id/products')
            products_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/products')
            before_like_count = products_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.TextView').text
            # 쉼표를 제거한 문자열 생성
            before_like_count = before_like_count.replace(',', '')
            # 문자열을 정수로 변환
            before_like_count = int(before_like_count)
            products_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.ImageView').click()
            #좋아요 선택
            after_like_count = products_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.TextView').text
            # 좋아요 누른  좋아요 갯수 확인
            # 쉼표를 제거한 문자열 생성
            after_like_count = after_like_count.replace(',', '')
            # 문자열을 정수로 변환
            after_like_count = int(after_like_count)
            sleep(3)
            if after_like_count == before_like_count+1 :
                print(f"갯수 확인 성공1 : 좋아요 누르기 전 갯수 -  {before_like_count}, 좋아요 누른 후 갯수 - {after_like_count}")
            else :
                print(f"갯수 확인 실패1 : 좋아요 누르기 전 갯수 -  {before_like_count}, 좋아요 누른 후 갯수 - {after_like_count}")

            before_like_count = products_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.TextView').text

            # 좋아요 취소 누르기 전 좋아요 갯수 확인
            # 쉼표를 제거한 문자열 생성
            before_like_count = before_like_count.replace(',', '')
            # 문자열을 정수로 변환
            before_like_count = int(before_like_count)
            products_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.ImageView').click()
            # 좋아요 선택
            after_like_count = products_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.TextView').text
            # 좋아요 취소 누른  좋아요 갯수 확인
            # 쉼표를 제거한 문자열 생성
            after_like_count = after_like_count.replace(',', '')
            # 문자열을 정수로 변환
            after_like_count = int(after_like_count)
            sleep(3)
            if after_like_count == before_like_count - 1:
                print(f"갯수 확인 성공2 : 좋아요 취소 누르기 전 갯수 -  {before_like_count}, 좋아요 취소 누른 후 갯수 - {after_like_count}")
            else:
                print(f"갯수 확인 실패2 : 좋아요 취소 누르기 전 갯수 -  {before_like_count}, 좋아요 취소 누른 후 갯수 - {after_like_count}")
            sleep(5)
            # API 호출
            response = requests.get("https://content-api.29cm.co.kr/api/v5/feeds?experiment=&feed_sort=WOMEN&home_type=APP_HOME&limit=10&offset=0")
            if response.status_code == 200:
                api_data = response.json()
                sleep(3)
                # 첫 번째 "feedTitle" 데이터 가져오기
                if api_data["data"]["results"]:
                    first_feed_title = api_data["data"]["results"][0]["feedTitle"]
                    print(f"우먼탭 api 호출 하여 첫번째 feedTitle 저장")
                else:
                    print("데이터가 없습니다.")
                app_feedTitle = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtFeedTitle').text
                print(f"확인3 : 우먼탭에 첫번째로 노출되는 피드타이틀과 api 호출한 feedTitle 동일한지 확인")
                if app_feedTitle == first_feed_title :
                    print(f"피드 타이틀 동일 확인 : {app_feedTitle}")
                else :
                    print(f"피드 타이틀 동일 확인 실패 : {app_feedTitle}")
            else:
                print("API 호출에 실패했습니다.")
            print("[홈화면 컨텐츠 확인]CASE 종료")



        except Exception:
            # 오류 발생 시 테스트 결과를 실패로 한다
            test_result = 'FAIL'
            # 스크린샷
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            # 스크린샷 경로 추출
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            # 에러 메시지 추출
            error_text = traceback.format_exc().split('\n')
            try:
                # 에러메시지 분류 시 예외처리
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
            except Exception:
                pass

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data