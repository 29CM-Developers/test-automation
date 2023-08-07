import json
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
from time import sleep, time, strftime, localtime

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

            response = requests.get("https://content-api.29cm.co.kr/api/v4/banners?bannerDivision=HOME_MOBILE&gender="+self.pconf['GENDER'])
            if response.status_code == 200:
                api_data = response.json()
                sleep(3)
                # 첫 번째 "feedTitle" 데이터 가져오기
                if api_data["data"]["bannerList"]:
                    fifth_banner_title = api_data["data"]["bannerList"][4]["bannerTitle"]
                    print(f"홈 상단 배너 api 호출 하여 다섯번째 bannerTitle 저장: {fifth_banner_title}")
                else:
                    print("데이터가 없습니다.")

                found_element = None
                for _ in range(20):
                    try:
                        # 다섯번째 배너 타이틀과 일치하는 요소 찾기
                        element = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtFeedBannerTitle')
                        if element.text == fifth_banner_title:
                            found_element = element
                            print(f"다섯번째 bannerTitle 발견 : {element.text}")
                            print(f"배너타이틀 노출 확인 : {element.text}")
                            break
                    except NoSuchElementException:
                        pass
                    # 스와이프 액션 수행
                    element_control.swipe_right_to_left(wd,element)
                if found_element is None:
                    test_result = 'WARN'
                    warning_texts.append("홈화면 상단 배너 좌우 슬라이드 확인 실패")

            else:
                print("API 호출에 실패했습니다.")

            home_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtShowAll').text
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtShowAll').click()
            print("모아보기 화면 진입")
            next_layer_title = wd.find_element(AppiumBy.XPATH,'//*[@resource-id="__next"]/android.widget.TextView[@index=0]').text
            if next_layer_title == home_title:
                print(f"모아보기 진입 확인 : {next_layer_title} 노출 확인")
                print("모아보기 버튼 선택하여 모아보기 페이지 진입 확인")
            else:
                print(f"모아보기 진입 확인 실패 : {next_layer_title} 노출")
                test_result = 'WARN'
                warning_texts.append("모아보기 페이지 진입 확인 실패")
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

            if gift_title == dynamic_button_title :
                print(f"선물하기 타이틀 확인 : {gift_title}")
            else :
                print(f"선물하기 타이틀 확인 실패 : {gift_title}")
                test_result = 'WARN'
                warning_texts.append("다이나믹 게이트 타이틀 확인 실패")

            # 뒤로가기로 홈화면 진입 확인
            gift_layer.find_element(AppiumBy.XPATH,'//android.view.View[1]/android.view.View/android.view.View/android.widget.Button').click()
            print("뒤로가기 선택")
            sleep(3)
            print("[홈화면 배너 확인]CASE 종료")

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
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def test_home_contents(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):

        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[홈화면 컨텐츠 확인]CASE 시작")
            sleep(5)
            tab_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/tabLayout')
            # 2. 홈 > 피드 > 추천 탭선택
            tab_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[4]/android.view.ViewGroup/android.widget.TextView').click()
            print('홈 > 피드 > 추천 탭선택 ')
            guide_text = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/textRecommend')

            if guide_text.text == self.pconf['NAME']+'님을 위한 추천 상품':
                print(f"'{self.pconf['NAME']}님을 위한 추천 상품’ 가이드 문구 노출 확인")
            else:
                print(f"'{self.pconf['NAME']}님을 위한 추천 상품’ 가이드 문구 노출 실패")
                test_result = 'WARN'
                warning_texts.append("홈화면 추천 탭 타이틀 확인 실패")
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
            sleep(1)
            #좋아요 선택
            after_like_count = products_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.TextView').text
            # 좋아요 누른  좋아요 갯수 확인
            # 쉼표를 제거한 문자열 생성
            after_like_count = after_like_count.replace(',', '')
            # 문자열을 정수로 변환
            after_like_count = int(after_like_count)
            sleep(3)
            if after_like_count == before_like_count+1 :
                print(f"갯수 확인 성공 : 좋아요 누르기 전 갯수 -  {before_like_count}, 좋아요 누른 후 갯수 - {after_like_count}")
            else :
                print(f"갯수 확인 실패 : 좋아요 누르기 전 갯수 -  {before_like_count}, 좋아요 누른 후 갯수 - {after_like_count}")
                test_result = 'WARN'
                warning_texts.append("피드 아이템 좋아요 개수 증가 확인 실패")

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
                print(f"갯수 확인 성공 : 좋아요 취소 누르기 전 갯수 -  {before_like_count}, 좋아요 취소 누른 후 갯수 - {after_like_count}")
            else:
                print(f"갯수 확인 실패 : 좋아요 취소 누르기 전 갯수 -  {before_like_count}, 좋아요 취소 누른 후 갯수 - {after_like_count}")
                test_result = 'WARN'
                warning_texts.append("피드 아이템 좋아요 개수 차감 확인 실패")
            sleep(5)
            # API 호출
            response = requests.get("https://content-api.29cm.co.kr/api/v5/feeds?experiment=&feed_sort=WOMEN&home_type=APP_HOME&limit=10&offset=0")
            if response.status_code == 200:
                api_data = response.json()
                sleep(3)
                # "results" 배열을 가져옵니다.

                index = None
                count = 0
                for i, result in enumerate(api_data['data']['results']):
                    if result['feedType'] == 'contents':
                        if index is None :
                            print(f'{result["feedTitle"]}, {i}')
                            count += 1
                            if count == 2:
                                print(f" count : {count}, {result['feedTitle']}, {i}, {index}")
                                second_feed_title = api_data['data']['results'][i]['feedTitle']
                                break
                        else:
                            index == i
                            break

                second_feed_title = api_data['data']['results'][i]['feedTitle']
                print(f"second_feed_title : {second_feed_title}")
                found_element = None
                for _ in range(10):
                    try:
                        # 두번째 피드 타이틀와 일치하는 요소 찾기
                        element = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtFeedTitle')
                        if element.text == second_feed_title:
                            found_element = element
                            print(f"두번째 feedTitle 발견 : {second_feed_title}")
                            print(f"피드 컨텐츠 추가 노출 확인 : {second_feed_title}")
                            break
                    except NoSuchElementException:
                        pass
                    # 스크롤 액션 수행
                    element_control.scroll(wd)

                if found_element is None:
                    test_result = 'WARN'
                    warning_texts.append("피드 컨텐츠 추가 노출 확인 실패")

            else:
                print("API 호출에 실패했습니다.")
            sleep(2)
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
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data