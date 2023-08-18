import os.path
import sys
import traceback
import logging
import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from com_utils import values_control, element_control
from time import sleep, time
logger = logging.getLogger(name='Log')
logger.setLevel(logging.INFO)  ## 경고 수준 설정
formatter = logging.Formatter('|%(name)s||%(lineno)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler()  ## 스트림 핸들러 생성
stream_handler.setFormatter(formatter)  ## 텍스트 포맷 설정
logger.addHandler(stream_handler)  ## 핸들러 등록
class Search:

    def test_search_popular_brand(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[검색 화면 인기브랜드 확인]CASE 시작")
            sleep(2)
            #  SEARCH 탭 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'SEARCH').click()
            print("하단 SEARCH탭 선택")
            # 확인 : 지금 많이 찾는 브랜드 타이틀 노출 확인 - 인기 브랜드 타이틀 확인
            search_container = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/container')
            # 최근 검색어 있는 경우 모두 지우기로 삭제
            delete_all = wd.find_elements(By.XPATH, "//*[contains(@text, '모두 지우기')]")
            print(delete_all)
            if len(delete_all) == 0:
                pass
            else:
                delete_all[0].click()
            # 지금 많이 찾는 브랜드 찾기
            element_xpath = '//androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.widget.TextView[1]'
            search_container_title = search_container.find_element(AppiumBy.XPATH, element_xpath)
            if search_container_title.text == '지금 많이 찾는 브랜드':
                print("지금 많이 찾는 브랜드 타이틀 노출 확인")
                pass
            else:
                print("지금 많이 찾는 브랜드 타이틀 노출 실패")
                test_result = 'WARN'
                warning_texts.append("지금 많이 찾는 브랜드 타이틀 노출 실패")
            print(f"타이틀 확인 : {search_container_title.text}")

            response = requests.get('https://search-api.29cm.co.kr/api/v4/keyword/popular?limit=100&brandLimit=30')
            if response.status_code == 200:
                api_data = response.json()
                brands = api_data['data']['popularBrandKeywords']
                api_30th_brand_name = brands[29]
                print(f"api 30th_brand_name : {api_30th_brand_name}")
                # 지금 많이 찾는 브랜드 영역 스와이프 3회
                brand_layer = search_container.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.view.View[2]')
                for _ in range(0, 2):
                    element_control.swipe_control(wd, brand_layer, 'left', 60)
                    print("스와이프")
                    sleep(1)
                sleep(1)
                brand_30th = brand_layer.find_element(AppiumBy.XPATH,'//android.view.View/android.view.View[10]')
                # 검색 화면 > 인기 브랜드 검색어 30위 선택
                brand_30th_name = brand_30th.find_element(AppiumBy.XPATH, '//android.widget.TextView[2]').text
                print(f"30위 브랜드 : {brand_30th_name}")
                if brand_30th_name == api_30th_brand_name :
                    print('api 인기 브랜드 30위와 노출되는 30위 동일 여부 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('api 인기 브랜드 30위와 노출되는 30위 동일 여부 확인 실패')
                    print('api 인기 브랜드 30위와 노출되는 30위 동일 여부 확인 실패')
            else:
                print('카테고리 그룹 API 호출 실패')
            brand_30th.click()
            print('브랜드 30위 선택')
            print(brand_30th_name)
            # 확인: 브랜드 영역에 노출되는 브랜드와 검색한 브랜드명이 동일한지 확인
            brand_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/searchResultBrandComposeView')
            search_brand = brand_layer.find_element(AppiumBy.XPATH,'//android.view.View/android.view.View[1]/android.widget.TextView[1]').text
            if search_brand == brand_30th_name:
                print("선택한 브랜드명과 브랜드 영역에 노출된 브랜드 문구가 동일 확인")
            else:
                print("선택한 브랜드명과 브랜드 영역에 노출된 브랜드 문구가 동일 확인 실패")
                test_result = 'WARN'
                warning_texts.append("브랜드 영역에 노출되는 브랜드와 검색한 브랜드명이 동일한지 확인 실패")
            print(f"브랜드 이름 : {search_brand} ")
            # 뒤로가기로 카테고리 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            sleep(2)
            # 최근 검색어 있는 경우 모두 지우기로 삭제
            delete_all = wd.find_elements(By.XPATH, "//*[contains(@text, '모두 지우기')]")
            print(delete_all)
            if len(delete_all) == 0:
                pass
            else:
                delete_all[0].click()
            sleep(2)
            filter_name = element_control.scroll_to_element_with_text(wd, '전체 기준')
            print(3)
            filter_name.click()
            sleep(2)
            # print(f"필터네임 클릭 : {filter_name.text}")
            bottom_sheet_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/design_bottom_sheet')
            gender_filter = bottom_sheet_layer.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[2]/android.widget.TextView')
            gender_filter.click()
            print(f"성별 필터 선택 : {gender_filter.text}")
            age_filter = bottom_sheet_layer.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[8]/android.widget.TextView')
            age_filter.click()
            print(f"연령 필터 선택 : {age_filter.text}")
            bottom_sheet_layer.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[11]').click()
            print("적용하기 버튼 선택")
            filter_name_tag = f"{self.conf['search_filter_gender']['WOMEN']} {self.conf['search_filter_age']['30to34']} 기준"
            print(filter_name_tag)
            if filter_name.text in filter_name_tag :
                print("필터 적용 - 필터링에 여성 30~34세 기준 문구 노출 확인 확인")
                response = requests.get('https://search-api.29cm.co.kr/api/v4/keyword/popular?limit=100&brandLimit=30&group=female&ageGroup=30to34')
                if response.status_code == 200:
                    api_data = response.json()
                    brands = api_data['data']['popularBrandKeywords']
                    api_1st_brand_name = brands[0]
                    print(f"api 1st_brand_name : {api_1st_brand_name}")
                    brand_1st = element_control.scroll_to_element_with_text(wd, api_1st_brand_name)
                    print(f"1위 브랜드 : {brand_1st}")
                    # 검색 화면 > 인기 브랜드 검색어 30위 선택
                    brand_1st_name = brand_1st.text
                    if brand_1st_name == api_1st_brand_name:
                        print('api 인기 브랜드 1위와 노출되는 1위 동일 여부 확인')
                        # 지금 많이 찾는 브랜드 전체기준 선택
                        filter_name = element_control.scroll_to_element_with_text(wd, filter_name_tag)
                        filter_name.click()
                        print(f"필터네임 클릭 : {filter_name}")
                        bottom_sheet_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/design_bottom_sheet')
                        gender_filter = bottom_sheet_layer.find_element(AppiumBy.XPATH,'//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]/android.widget.TextView')
                        gender_filter.click()
                        print(f"성별 필터 선택 : {gender_filter.text}")
                        age_filter = bottom_sheet_layer.find_element(AppiumBy.XPATH,'//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[4]/android.widget.TextView')
                        age_filter.click()
                        print(f"연령 필터 선택 : {age_filter.text}")
                        bottom_sheet_layer.find_element(AppiumBy.XPATH,'//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[11]').click()
                        print("적용하기 버튼 선택")
                        filter_name_tag = f"{self.conf['search_filter_gender']['ALL']} 기준"
                        if filter_name.text in filter_name_tag:
                            print("필터 적용 - 전체 문구 노출 확인")
                        else :
                            print("필터 적용 - 전체 문구 노출 확인 실패")
                        print(f'filter_name_tag : {filter_name_tag}')
                    else:
                        test_result = 'WARN'
                        warning_texts.append('api 인기 브랜드 1위와 노출되는 1위 동일 여부 확인 실패')
                        print('api 인기 브랜드 1위와 노출되는 1위 동일 여부 확인 실패')
                else:
                    print('카테고리 그룹 API 호출 실패')
            else:
                print("필터 적용 확인 - 필터링에 여성 30~34세 기준 문구 노출 확인 실패")
                test_result = 'WARN'
                warning_texts.append("필터 적용 확인 실패")
            print(f"필터 노출 이름 : {filter_name} ")
            # 뒤로가기로 카테고리 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            sleep(2)
            print("[검색 화면 인기브랜드 확인]CASE 종료")

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