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
            # api_banner_title = []
            # banner_title_set = []
            # response = requests.get("https://content-api.29cm.co.kr/api/v4/banners?bannerDivision=HOME_MOBILE&gender="+self.pconf['GENDER'])
            # if response.status_code == 200:
            #
            #     api_data = response.json()
            #     count = int(api_data["data"]["count"])
            #     for i in range(count):
            #         api_banner_title.append(api_data["data"]["bannerList"][i]["bannerTitle"])
            #     print(api_banner_title)
            #
            #     for i in range(0,count):
            #         sleep(2.5)
            #         try:
            #             print(5)
            #             # 대기 설정
            #             wait = WebDriverWait(wd, 5)  # 최대 10초까지 대기
            #
            #             element_layer_1 = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/bannerViewContainer')
            #             print(1)
            #             element_layer_2 = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/homeBannerViewPager')
            #             print(2)
            #             element_layer_3 = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/viewPager')
            #             print(3)
            #             # 모든 요소를 선택하는 XPath 쿼리
            #             all_elements = element_layer_3.find_elements(By.XPATH, "//*")
            #             print("all_elements 요소의 개수:", len(all_elements))
            #             # class 속성이 'android.widget.TextView'인 요소를 찾습니다.
            #             text_view_elements = []
            #             for element in all_elements :
            #                 print(f"element:{element}")
            #                 if "android.widget.TextView" in element.get_attribute("class"):
            #                     print(2)
            #                     text_view_elements.append(element.text)
            #                     print(3)
            #
            #             print("android.widget.TextView 요소의 개수:", len(text_view_elements))
            #
            #             # 찾은 요소들에 대한 추가 동작을 수행할 수 있습니다.
            #             for element in text_view_elements:
            #                 print("요소 텍스트:", element.text)
            #                 banner_title_set.append(element.text)
            #             # element_control.mini_swipe(wd, element_layer_3)
            #             # print(4)
            #             # banner_title_text = wd.find_element(AppiumBy.XPATH,
            #             #                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.widget.TextView[1]').text
            #             # print(element_layer_4.text)
            #
            #         except NoSuchElementException:
            #             print("못찾음")
            #             pass
            #         except Exception:
            #             # 에러 발생하여 타이틀 확인 실패 시, 이전 배너로 스와이프하여 타이틀 저장
            #             print("에러")
            #             element_layer_3 = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/viewPager')
            #             print(3)
            #             element_layer_4 = element_layer_3.find_element(By.XPATH, '//*android.widget.TextView[1]')
            #             print(4)
            #
            #             # element_control.mini_swipe(wd, element_layer_3)
            #             # print(4)
            #             # banner_title_text = wd.find_element(AppiumBy.XPATH,
            #             #                                     '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.widget.TextView[1]').text
            #             # print(element_layer_4.text)
            #             banner_title_set.append(element_layer_4.text)
            #         # 스와이프 액션 수행
            #         element_control.swipe_control(wd, element_layer_4,'right',30)
            #         print("스와이프해")
            #
            #
            # else:
            #     print("API 호출에 실패했습니다.")

            # 4. 다이나믹 게이트 2번째 줄, 2번째 선택
            sleep(1)
            dynamic_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/dynamicItems')
            dynamic_button_title = dynamic_layer.find_element(AppiumBy.XPATH, '//android.widget.LinearLayout[2]/androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.widget.TextView').text
            dynamic_layer.find_element(AppiumBy.XPATH, '//android.widget.LinearLayout[2]/androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.widget.TextView').click()
            sleep(2)
            gift_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/rootView')
            gift_title = gift_layer.find_element(AppiumBy.XPATH, '//android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.widget.TextView').text

            if gift_title == dynamic_button_title :
                print(f"선물하기 타이틀 확인 : {gift_title}")
            else :
                print(f"선물하기 타이틀 확인 실패 : {gift_title}")
                test_result = 'WARN'
                warning_texts.append("다이나믹 게이트 타이틀 확인 실패")

            # 뒤로가기로 홈화면 진입 확인
            gift_layer.find_element(AppiumBy.XPATH,'//android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.widget.Button').click()
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
            wd.get('app29cm://home')

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
            tab_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/tabScrollView')
            # 2. 홈 > 피드 > 추천 탭선택
            tab_layer.find_element(AppiumBy.XPATH,'//android.widget.HorizontalScrollView/android.widget.LinearLayout/android.view.ViewGroup[5]').click()
            print('홈 > 피드 > 추천 탭선택 ')
            guide_text = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/textRecommend')

            if guide_text.text == self.pconf['NAME']+'님을 위한 추천 상품':
                print(f"'{self.pconf['NAME']}님을 위한 추천 상품’ 가이드 문구 노출 확인")
            else:
                print(f"'{self.pconf['NAME']}님을 위한 추천 상품’ 가이드 문구 노출 실패")
                test_result = 'WARN'
                warning_texts.append("홈화면 추천 탭 타이틀 확인 실패")
            print(f"가이드 문구 : {guide_text.text} ")

            tab_layer.find_element(AppiumBy.XPATH,'//android.widget.HorizontalScrollView/android.widget.LinearLayout/android.view.ViewGroup[1]').click()
            print('홈 > 피드 > 우먼 탭선택 ')
            sleep(1)

            # API 호출
            response = requests.get("https://content-api.29cm.co.kr/api/v5/feeds?experiment=&feed_sort=WOMEN&home_type=APP_HOME&limit=10&offset=0")
            if response.status_code == 200:
                api_data = response.json()
                # feedType이 contents인 첫번째, 두번째 텍스트 저장

                saved_result = None
                saved_results =[]
                results = api_data["data"]["results"]
                for result in results:
                    if not saved_result and "feedTitle" in result and "feedType" in result and result["feedType"] == "contents" and "relatedFeedItemList" in result:
                        if any("feedItemNo" in item for item in result["relatedFeedItemList"]):
                            print(f"첫번째 저장 result : {result['feedTitle']}")
                            saved_result = result['feedTitle']
                            saved_results.append(result['feedTitle'])
                    elif saved_result and "feedTitle" in result and "feedType" in result and result["feedType"] == "contents":
                        print(f"두번째 저장 result : {result['feedTitle']}")
                        saved_result = result['feedTitle']
                        saved_results.append(result['feedTitle'])
                        break
                print(f"saved_result : {saved_result}, saved_results.append(result['feedTitle']) : {saved_results}")

                found_element = None
                for _ in range(10):
                    try:
                        # 첫번째 피드 타이틀와 일치하는 요소 찾기
                        element = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtFeedTitle')
                        if element.text == saved_results[0]:
                            found_element = element
                            print(f"첫번째 feedTitle 발견 : {saved_results[0]}")
                            print(f"피드 컨텐츠 추가 노출 확인 : {element.text}")
                            break
                    except NoSuchElementException:
                        pass
                    # 스크롤 액션 수행
                    element_control.scroll(wd)

                if found_element is None:
                    test_result = 'WARN'
                    warning_texts.append("첫번째 feedTitle 발견 실패")

                # 스크롤
                element_control.scroll_to_element_id(wd, 'com.the29cm.app29cm:id/products')
                element_control.scroll(wd)
                products_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/products')
                before_like_count = products_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.TextView').text
                # 쉼표를 제거한 문자열 생성
                before_like_count = before_like_count.replace(',', '')
                # 문자열을 정수로 변환
                before_like_count = int(before_like_count)
                products_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.widget.ImageView').click()
                sleep(1)
                #좋아요 선택
                # 앱설치 후 최초 좋아요 선택 시 앱평가 팝업 발생
                app_appraisal_pop_up = wd.find_elements(AppiumBy.ID, "android:id/content")
                print(app_appraisal_pop_up)
                if len(app_appraisal_pop_up) == 0:
                    pass
                else:
                    wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtCancel').click()

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
                sleep(2)
                found_element = None
                for _ in range(20):
                    try:
                        # 두번째 피드 타이틀와 일치하는 요소 찾기
                        element = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtFeedTitle')
                        if element.text == saved_results[1]:
                            found_element = element
                            print(f"두번째 feedTitle 발견 : {saved_results[1]}")
                            print(f"피드 컨텐츠 추가 노출 확인 : {element.text}")
                            break
                    except NoSuchElementException:
                        pass
                    # 스크롤 액션 수행
                    element_control.scroll(wd)

                if found_element is None:
                    print("피드 컨텐츠 추가 노출 확인 실패")
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
            wd.get('app29cm://home')

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