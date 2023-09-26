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

    def test_move_tab_from_home(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):

        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[홈화면에서 다른 탭으로 이동 확인]CASE 시작")
            sleep(2)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'CATEGORY').click()
            sleep(2)
            print("카테고리 탭 선택")

            category_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/shopComposeView')
            # 첫번째 대메뉴 선택
            category_layer.find_element(AppiumBy.ACCESSIBILITY_ID, 'category_first_title').click()

            # 중 카테고리 리스트 중 상단 4개의 카테고리명을 리스트로 저장
            category_list = []
            medium_category_list = []
            medium_category_list.append(category_layer.find_element(AppiumBy.XPATH,
                                                                    '//android.view.View/android.view.View[3]/android.view.View[@index=3]/android.widget.TextView').text)
            medium_category_list.append(category_layer.find_element(AppiumBy.XPATH,
                                                                    '//android.view.View/android.view.View[3]/android.view.View[@index=4]/android.widget.TextView').text)
            medium_category_list.append(category_layer.find_element(AppiumBy.XPATH,
                                                                    '//android.view.View/android.view.View[3]/android.view.View[@index=5]/android.widget.TextView').text)
            medium_category_list.append(category_layer.find_element(AppiumBy.XPATH,
                                                                    '//android.view.View/android.view.View[3]/android.view.View[@index=6]/android.widget.TextView').text)
            category_list = self.pconf['compare_category_list']
            print(f"medium_category_list : {medium_category_list}, category_list : {category_list}")
            if category_list == medium_category_list:
                print('HOME 탭에서 CATEGORY 탭 이동 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 CATEGORY 탭 이동 확인 실패')
                print(f'HOME 탭에서 CATEGORY 탭 이동 확인 실패 : {medium_category_list}')

            # HOME 탭으로 이동
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()
            try:
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgLogo')
                print('HOME 탭으로 이동')
            except NoSuchElementException:
                print('HOME 탭으로 이동 실패')

            # SEARCH 탭 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'SEARCH').click()
            sleep(1)
            # 인기 브랜드 타이틀 확인
            try:
                search_container = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/container')
                sleep(2)
                # 지금 많이 찾는 브랜드 찾기
                search_container_title = wd.find_element(AppiumBy.XPATH,
                                                         '//android.widget.TextView[@content-desc="search_popular_brand"]')
                if search_container_title.text == '지금 많이 찾는 브랜드':
                    print("지금 많이 찾는 브랜드 타이틀 노출 확인")
                    pass
                else:
                    print("지금 많이 찾는 브랜드 타이틀 노출 실패")
                    test_result = 'WARN'
                    warning_texts.append("지금 많이 찾는 브랜드 타이틀 노출 실패")
                print(f'HOME 탭에서 SEARCH 탭 이동 확인 - 인기 브랜드 타이틀: {search_container_title}')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 SEARCH 탭 이동 확인')
                print(f'HOME 탭에서 SEARCH 탭 이동 확인 - 인기 브랜드 타이틀: {search_container_title}')

            # 인기 검색어 타이틀 확인
            try:
                # 확인 : 지금 많이 찾는 브랜드 타이틀 노출 확인 - 인기 브랜드 타이틀 확인
                search_container = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/container')
                # 최근 검색어 있는 경우 모두 지우기로 삭제
                delete_all = wd.find_elements(By.XPATH, "//*[contains(@text, '모두 지우기')]")
                print(delete_all)
                if len(delete_all) == 0:
                    pass
                else:
                    delete_all[0].click()
                # 지금 많이 찾는 검색어 찾기
                sleep(2)
                search_container_title = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'search_container_title')
                search_container_title_text = search_container_title.text
                if search_container_title.text == '지금 많이 찾는 검색어':
                    print("지금 많이 찾는 검색어 타이틀 노출 확인")
                    pass
                else:
                    print("지금 많이 찾는 검색어 타이틀 노출 실패")
                    test_result = 'WARN'
                    warning_texts.append("지금 많이 찾는 검색어 타이틀 노출 실패")
                print(f"타이틀 확인 : {search_container_title.text}")
                print('HOME 탭에서 SEARCH 탭 이동 확인 - 인기 검색어 타이틀')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 SEARCH 탭 이동 확인')
                print('HOME 탭에서 SEARCH 탭 이동 확인 실패 - 인기 검색어 타이틀')

            # 뒤로가기로 카테고리 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()

            try:
                # HOME 탭으로 이동
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()
                sleep(1)
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgLogo')
                print('HOME 탭으로 이동')
            except NoSuchElementException:
                print('HOME 탭으로 이동 실패')

            # LIKE 탭 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'LIKE').click()
            # 관심 브랜드 선택 화면 발생 케이스
            try:
                wd.find_elements(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutMyLikeAndOrderBrand')
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/iconClose').click()
            except NoSuchElementException:
                pass

            try:
                like_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtTitle').text
                if like_title == 'LIKE':
                    print('HOME 탭에서 LIKE 탭 이동 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('HOME 탭에서 LIKE 탭 이동 확인 실패')
                    print('HOME 탭에서 LIKE 탭 이동 확인 실패')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 LIKE 탭 이동 확인 실패')
                print('HOME 탭에서 LIKE 탭 이동 확인 실패')

            try:
                # HOME 탭으로 이동
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()
                sleep(1)
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgLogo')
                print('HOME 탭으로 이동')
            except NoSuchElementException:
                print('HOME 탭으로 이동 실패')

            # MY 탭 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'MY').click()
            try:
                # 로그인 성공 진입 확인
                login_name = wd.find_element(By.ID, 'com.the29cm.app29cm:id/txtUserName')
                if login_name.text == self.pconf['NAME']:
                    pass
                else:
                    print("로그인 문구 실패")
                    test_result = 'WARN'
                    warning_texts.append("로그인 문구 확인 실패")
                print("로그인 유저 이름 : %s " % login_name.text)

                print('HOME 탭에서 MY 탭 이동 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 MY 탭 이동 확인 실패')
                print('HOME 탭에서 MY 탭 이동 확인 실패')

            try:
                # HOME 탭으로 이동
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()
                sleep(1)
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgLogo')
                print('HOME 탭으로 이동')
            except NoSuchElementException:
                print('HOME 탭으로 이동 실패')
            print("[홈화면에서 다른 탭으로 이동]CASE 종료")

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

    def test_home_banner(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[홈화면 배너 확인]CASE 시작")
            sleep(1)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()
            print("홈 탭 선택")
            api_banner_title = []
            banner_title_set = []
            api_banner_id = []
            api_banner_contents = []
            response = requests.get(
                f"https://content-api.29cm.co.kr/api/v4/banners?bannerDivision=HOME_MOBILE&gender={self.pconf['GENDER']}")
            if response.status_code == 200:

                api_data = response.json()
                count = int(api_data["data"]["count"])
                print(f"api 배너 갯수  : {count}")
                for i in range(0, count):
                    api_banner_title.append(api_data["data"]["bannerList"][i]["bannerTitle"])
                    api_banner_id.append(api_data["data"]["bannerList"][i]["bannerId"])
                    api_banner_contents.append(api_data["data"]["bannerList"][i]["bannerContents"])
                print(api_banner_title)
                print(api_banner_id)
                print(api_banner_contents)
                set_api_banner_id = set(api_banner_id)
                set_api_banner_contents = set(api_banner_contents)

                # 중복을 확인합니다.
                if len(api_banner_id) != len(set_api_banner_id) or len(api_banner_contents) != len(
                        set_api_banner_contents):
                    print("리스트에 중복 요소가 있습니다.")
                    test_result = 'WARN'
                    warning_texts.append('중복된 홈 배너 없음 확인 실패')
                else:
                    print("리스트에 중복 요소가 없습니다.")

                home_banner_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/bannerImg')
                try:
                    for i in range(0, 3):
                        sleep(2.5)
                        home_banner_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/title').text
                        print(f"home_banner_title : {home_banner_title}")
                        banner_title_set.append(home_banner_title)
                except NoSuchElementException:
                    pass

                banner_title_set = set(banner_title_set)
                api_banner_title = set(api_banner_title)
                # API 호출 배너 리스트와 저장된 홈 배너 리스트 비교 (저장한 홈 배너 리스트 안에 호출한 리스트가 포함되면 pass)
                print(f"api_banner_title : {len(api_banner_title)}, banner_title_set : {len(banner_title_set)}")
                intersection_set = banner_title_set.intersection(api_banner_title)

                if len(intersection_set) > 0:
                    print("교집합 확인")
                    print("홈 배너 확인 성공")
                else:
                    print("교집합 확인 실패")
                    print("홈 배너 확인 실패")
                    print(f"api_banner_title : {len(api_banner_title)}, banner_title_set : {len(banner_title_set)}")
                    print(f"{api_banner_title}")
                    print(f"{banner_title_set}")
                    test_result = 'WARN'
                    warning_texts.append("홈 배너 확인 실패")
            else:
                print("API 호출에 실패했습니다.")

            # 4. 다이나믹 게이트 2번째 줄, 2번째 선택
            sleep(1)
            dynamic_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/dynamicItems')
            dynamic_button_title = wd.find_elements(By.XPATH, "//*[contains(@text, '센스있는 선물하기')]")
            print(dynamic_button_title)
            if len(dynamic_button_title) == 0:
                element_control.swipe_control(wd, dynamic_layer, 'left', 50)
                dynamic_button_title = wd.find_elements(By.XPATH, "//*[contains(@text, '센스있는 선물하기')]")
                print(dynamic_button_title)
            print(dynamic_button_title[0].text)
            button_title = dynamic_button_title[0].text
            dynamic_button_title[0].click()

            sleep(2)
            gift_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/rootView')
            gift_title = gift_layer.find_element(AppiumBy.XPATH, '//android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.widget.TextView').text
            print(gift_title)

            if gift_title == button_title:
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
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'recommend_tab').click()
            print('홈 > 피드 > 추천 탭선택 ')
            guide_text = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/textRecommend')

            if guide_text.text == self.pconf['NAME'] + '님을 위한 추천 상품':
                print(f"'{self.pconf['NAME']}님을 위한 추천 상품’ 가이드 문구 노출 확인")
            else:
                print(f"'{self.pconf['NAME']}님을 위한 추천 상품’ 가이드 문구 노출 실패")
                test_result = 'WARN'
                warning_texts.append("홈화면 추천 탭 타이틀 확인 실패")
            print(f"가이드 문구 : {guide_text.text} ")
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'women_tab').click()
            print('홈 > 피드 > 우먼 탭선택 ')
            sleep(1)

            # API 호출
            response = requests.get(
                "https://content-api.29cm.co.kr/api/v5/feeds?experiment=&feed_sort=WOMEN&home_type=APP_HOME&limit=10&offset=0")
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

                # 하트 이미 선택되었는지 확인
                heart_element = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/heartIcon')
                is_selected = heart_element.is_selected()
                if is_selected:
                    print("하트 선택된 상태입니다.")
                    heart_element.click()
                    print("하트 선택 해제")
                else:
                    print("하트 선택되지 않은 상태입니다.")

                before_like_count = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/heartCount').text
                # 쉼표를 제거한 문자열 생성
                before_like_count = before_like_count.replace(',', '')
                # 문자열을 정수로 변환
                before_like_count = int(before_like_count)
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/heartCount').click()
                sleep(1)
                # 좋아요 선택
                # 앱평가 발생 시 팝업 제거
                app_evaluation = wd.find_elements(By.XPATH, "//*[contains(@text, '29CM 앱을 어떻게 생각하시나요?')]")
                print(app_evaluation)
                if len(app_evaluation) == 0:
                    pass
                else:
                    wd.find_element(By.XPATH, "//*[contains(@text, '좋아요')]").click()
                    sleep(1)
                    wd.find_element(By.XPATH, "//*[contains(@text, '나중에 하기')]").click()

                after_like_count = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/heartCount').text
                # 좋아요 누른  좋아요 갯수 확인
                # 쉼표를 제거한 문자열 생성
                after_like_count = after_like_count.replace(',', '')
                # 문자열을 정수로 변환
                after_like_count = int(after_like_count)
                sleep(3)
                if after_like_count == before_like_count + 1:
                    print(f"갯수 확인 성공 : 좋아요 누르기 전 갯수 -  {before_like_count}, 좋아요 누른 후 갯수 - {after_like_count}")
                else:
                    print(f"갯수 확인 실패 : 좋아요 누르기 전 갯수 -  {before_like_count}, 좋아요 누른 후 갯수 - {after_like_count}")
                    test_result = 'WARN'
                    warning_texts.append("피드 아이템 좋아요 개수 증가 확인 실패")

                before_like_count = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/heartCount').text

                # 좋아요 취소 누르기 전 좋아요 갯수 확인
                # 쉼표를 제거한 문자열 생성
                before_like_count = before_like_count.replace(',', '')
                # 문자열을 정수로 변환
                before_like_count = int(before_like_count)
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/heartCount').click()
                # 좋아요 선택
                after_like_count = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/heartCount').text
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