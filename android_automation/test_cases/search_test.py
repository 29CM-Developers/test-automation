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
                api_1st_brand_name = brands[0]
                api_30th_brand_name = brands[29]
                print(f"api_1st_brand_name : {api_1st_brand_name}, api 30th_brand_name : {api_30th_brand_name}")
                filter_name = wd.find_elements(By.XPATH, "//*[contains(@text, '내 취향에 맞는 연령대를 설정해보세요')]")
                print(filter_name)
                if len(filter_name) == 0:
                    filter_name = element_control.scroll_to_element_with_text(wd, '전체 기준')
                    # 지금 많이 찾는 브랜드 영역 스와이프 3회
                    brand_layer = search_container.find_element(AppiumBy.XPATH,'//androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.view.View[2]')
                else:
                    # 지금 많이 찾는 브랜드 영역 스와이프 3회
                    brand_layer = search_container.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.view.View[1]')
                for _ in range(0, 2):
                    element_control.swipe_control(wd, brand_layer, 'left', 60)
                    print("스와이프")
                    sleep(1)
                sleep(1)
                brand_1st = brand_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View[1]')
                # 검색 화면 > 인기 브랜드 검색어 30위 선택
                brand_1st_name = brand_1st.find_element(AppiumBy.XPATH, '//android.widget.TextView[2]').text
                print(f"1st 브랜드 : {brand_1st_name}")
                brand_30th = brand_layer.find_element(AppiumBy.XPATH,'//android.view.View[10]')
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
            # 뒤로가기로 카테고리 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            sleep(2)
            #  SEARCH 탭 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'SEARCH').click()
            print("하단 SEARCH탭 선택")
            search_container = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/container')
            sleep(2)
            filter_name = wd.find_elements(By.XPATH, "//*[contains(@text, '내 취향에 맞는 연령대를 설정해보세요')]")
            print(filter_name)
            if len(filter_name) == 0:
                filter_name = element_control.scroll_to_element_with_text(wd, '전체 기준')
                brand_layer = search_container.find_element(AppiumBy.XPATH,'//androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.view.View[2]')
            else:
                brand_layer = search_container.find_element(AppiumBy.XPATH,'//androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.view.View[1]')
            #1위선택
            brand_1st = brand_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View[1]')
            # 검색 화면 > 인기 브랜드 검색어 1위 선택
            brand_1st_name_element = brand_1st.find_element(AppiumBy.XPATH, '//android.widget.TextView[2]')
            brand_1st_name = brand_1st.find_element(AppiumBy.XPATH, '//android.widget.TextView[2]').text
            print(f"1st 브랜드 : {brand_1st_name}")
            if brand_1st_name == api_1st_brand_name:
                print('api 인기 브랜드 1위와 노출되는 1위 동일 여부 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('api 인기 브랜드 1위와 노출되는 1위 동일 여부 확인 실패')
                print('api 인기 브랜드 1위와 노출되는 1위 동일 여부 확인 실패')

            brand_1st_name_element.click()
            print('브랜드 1위 선택')
            sleep(2)
            # 확인: 브랜드 영역에 노출되는 브랜드와 검색한 브랜드명이 동일한지 확인
            brand_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/searchResultBrandComposeView')
            search_brand = brand_layer.find_element(AppiumBy.XPATH,'//android.view.View/android.view.View[1]/android.widget.TextView[1]').text
            if search_brand == brand_1st_name:
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
            # 앱최초 실행 시에 문구 다름
            filter_name = wd.find_elements(By.XPATH, "//*[contains(@text, '내 취향에 맞는 연령대를 설정해보세요')]")
            print(filter_name)
            if len(filter_name) == 0:
                filter_name = element_control.scroll_to_element_with_text(wd, '전체 기준')
                sleep(2)
                filter_name.click()
            else:
                filter_name[0].click()
            sleep(2)
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
            filter_name = element_control.scroll_to_element_with_text(wd, filter_name_tag)
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
    def test_search_popular_keyword(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[검색 화면 인기 검색어 확인]CASE 시작")
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
            # 지금 많이 찾는 검색어 찾기
            element_xpath = '//androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.widget.TextView[2]'
            search_container_title = search_container.find_element(AppiumBy.XPATH, element_xpath)
            if search_container_title.text == '지금 많이 찾는 검색어':
                print("지금 많이 찾는 검색어 타이틀 노출 확인")
                pass
            else:
                print("지금 많이 찾는 검색어 타이틀 노출 실패")
                test_result = 'WARN'
                warning_texts.append("지금 많이 찾는 검색어 타이틀 노출 실패")
            print(f"타이틀 확인 : {search_container_title.text}")

            response = requests.get('https://search-api.29cm.co.kr/api/v4/keyword/popular?limit=100&brandLimit=30')
            if response.status_code == 200:
                api_data = response.json()
                keywords = api_data['data']['popularKeyword']
                api_1st_keyword_name = keywords[0]
                api_25th_keyword_name = keywords[24]
                print(f"api_1st_keyword_name : {api_1st_keyword_name}, api_25th_keyword_name : {api_25th_keyword_name}")
                element = wd.find_element(By.XPATH, f"//*[contains(@text, '{api_1st_keyword_name}')]")
                print(f"element : {element.text}")
                keyword_1st_name = element.text
                print(f"keyword_1st_name : {keyword_1st_name}")

                if keyword_1st_name == api_1st_keyword_name :
                    print('api 인기 검색어 1위와 노출되는 1위 동일 여부 확인')
                    element.click()
                    # 연관 검색어 있을 경우, 첫번째 연관 검색어 확인
                    response = requests.get(f'https://search-api.29cm.co.kr/api/v4/keyword/related?keyword={keyword_1st_name}')
                    if response.status_code == 200:
                        api_data = response.json()
                        if 'data' in api_data and 'relatedKeywords' in api_data['data']:
                            related_keywords = api_data['data']['relatedKeywords']

                            if len(related_keywords) == 0:
                                print("relatedKeywords 배열에 값이 없습니다.")
                            else:
                                print("relatedKeywords 배열에 값이 있습니다.")
                                related_1st_keyword = related_keywords[0]
                                print(f"related_1st_keyword : {related_1st_keyword}")
                                related_keyword_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/relatedKeywordComposeView')
                                related_keyword_1st = related_keyword_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View/android.widget.TextView[1]').text
                                if related_1st_keyword in related_keyword_1st :
                                    print("인기 검색어 검색 확인 - 첫번째 연관 검색어 확인")
                                else :
                                    print("인기 검색어 검색 확인 - 첫번째 연관 검색어 확인 실패")
                                    test_result = 'WARN'
                                    warning_texts.append("인기 검색어 검색 확인 실패")
                                print(f"연관검색어 확인 : {related_1st_keyword}")
                        else:
                            print("응답 데이터에 'data' 키 또는 'relatedKeywords' 키가 없습니다.")
                    else:
                        print('카테고리 그룹 API 호출 실패')
                    # 확인: 선택한 키워드명과 입력란에 작성된 문구가 동일한지 확인
                    search_edit_text = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/searchEditText').text
                    if search_edit_text == keyword_1st_name:
                        print("선택한 키워드명과 입력란에 작성된 문구가 동일 확인")
                    else:
                        print("선택한 키워드명과 입력란에 작성된 문구가 동일 실패")
                        test_result = 'WARN'
                        warning_texts.append("키워드명 비교 실패")
                    print(f"검색어 : {search_edit_text} ")
                    # 뒤로가기로 카테고리 진입 확인
                    wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
                    print("뒤로가기 선택")
                    sleep(2)
                    # element_control.scroll_control(wd,'U',40)
                    delete_all = wd.find_elements(By.XPATH, "//*[contains(@text, '모두 지우기')]")
                    print(delete_all)
                    if len(delete_all) == 0:
                        pass
                    else:
                        recent_searches = wd.find_elements(By.XPATH, f"//*[contains(@text, '{search_edit_text}')]")
                        print(recent_searches)
                        if len(recent_searches) != 0:
                            # 최근 검색어 있는 경우 모두 지우기로 삭제
                            print("최근 검색어 노출 확인")
                        delete_all[0].click()
                    sleep(1)
                else:
                    test_result = 'WARN'
                    warning_texts.append('api 인기 검색어 1위와 노출되는 1위 동일 여부 확인 실패')
                    print('api 인기 검색어 1위와 노출되는 1위 동일 여부 확인 실패')
                # 25위 검색어 발견 스크롤
                keyword_25th_name = element_control.scroll_to_element_with_text(wd, api_25th_keyword_name)

                if keyword_25th_name.text == api_25th_keyword_name :
                    print('api 인기 검색어 25위와 노출되는 25위 동일 여부 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('api 인기 검색어 25위와 노출되는 25위 동일 여부 확인 실패')
                    print('api 인기 검색어 25위와 노출되는 25위 동일 여부 확인 실패')

                # 뒤로가기로 카테고리 진입 확인
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            print("[검색 화면 인기 검색어 확인]CASE 종료")

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
    def test_search_results_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[검색 결과 화면 확인]CASE 시작")
            sleep(2)
            #  SEARCH 탭 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'SEARCH').click()
            print("하단 SEARCH탭 선택")
            # 검색 필드에 [니트] 입력 후 검색
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/searchEditText').send_keys(self.conf['keyword']['knit'])
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/searchImg').click()
            relatedKeyword_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/relatedKeywordComposeView')
            relatedKeyword = relatedKeyword_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View/android.widget.TextView[1]').text
            if self.conf['keyword']['knit'] in relatedKeyword:
                print("검색어 검색 확인 - 확인1. 검색 셀렉트박스에 카테고리 태그 노출 확인")
            else:
                print("검색 셀렉트박스에 카테고리 태그 노출 확인 실패")
                test_result = 'WARN'
                warning_texts.append("검색어 검색 확인 실패")
            print(f"검색어 검색 확인 : {relatedKeyword}")

            # 확인: 브랜드 영역에 노출되는 브랜드와 검색한 브랜드명이 동일한지 확인
            brand_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/searchResultBrandComposeView')
            search_brand = brand_layer.find_element(AppiumBy.XPATH,'//android.view.View/android.view.View[1]/android.widget.TextView[1]').text
            if '니트' in search_brand:
                print("확인2. 브랜드 영역에 해당 브랜드 이름 노출 확인")
            else:
                print("확인2. 브랜드 영역에 해당 브랜드 이름 노출 확인 실패")
                test_result = 'WARN'
                warning_texts.append("검색어 검색 확인 실패")
            print(f"브랜드 이름 : {search_brand} ")

            selector_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/selector')
            selector = selector_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View/android.view.View[1]/android.widget.TextView')
            selector.click()
            bottom_sheet_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/design_bottom_sheet')
            filter_by_sales = bottom_sheet_layer.find_element(AppiumBy.XPATH,'//android.view.View/android.view.View[8]/android.widget.TextView')
            filter_by_sales_name = filter_by_sales.text
            filter_by_sales.click()
            sleep(1)
            if selector.text in filter_by_sales_name :
                print("판매순 정렬 변경 확인")
            else :
                print("판매순 정렬 변경 확인 실패")
                test_result = 'WARN'
                warning_texts.append("필터 적용 확인 실패")
            print(f"selector.text : {selector.text}, filter_by_sales_name : {filter_by_sales_name} , {self.conf['search_filter']['color']}")
            sleep(1)
            element = selector_layer.find_element(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['color']}')]")
            element.click()
            sleep(1)
            element = wd.find_element(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['black']}')]")
            element.click()
            sleep(1)
            element = wd.find_element(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['category']}')]")
            element.click()
            sleep(1)
            element = wd.find_element(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['woman_clothes']}')]")
            element.click()
            sleep(1)
            element = wd.find_element(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['cost']}')]")
            element.click()
            sleep(1)
            element = wd.find_element(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['5to10']}')]")
            element.click()
            sleep(1)
            element = wd.find_element(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['item_info']}')]")
            element.click()
            sleep(0.5)
            element = wd.find_element(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['excludingout_of_stock_products']}')]")
            element.click()
            sleep(0.5)
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/confirm').click()
            selector_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/selector')
            element = selector_layer.find_element(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['black']}')]")
            if '블랙' in element.text :
                print("블랙 필터링 노출 확인")
            else:
                print("블랙 필터링 노출 확인 불가")
                test_result = 'WARN'
                warning_texts.append("필터 적용 확인 실패")
            element = selector_layer.find_element(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['woman_clothes']}')]")
            if '여성의류' in element.text:
                print("여성의류 필터링 노출 확인")
            else:
                print("여성의류 필터링 노출 확인 실패")
                test_result = 'WARN'
                warning_texts.append("필터 적용 확인 실패")
            element_control.swipe_control(wd, selector_layer, 'left', 30)
            element = selector_layer.find_element(By.XPATH, "//*[contains(@text, '50,000원 ~ 100,000원')]")
            if '50,000원 ~ 100,000원' in element.text:
                print("50,000원 ~ 100,000원 필터링 노출 확인")
            else:
                print("50,000원 ~ 100,000원 필터링 노출 확인 실패")
                test_result = 'WARN'
                warning_texts.append("필터 적용 확인 실패")
            element_control.swipe_control(wd, selector_layer, 'left', 40)
            element_control.swipe_control(wd, selector_layer, 'left', 40)
            element = wd.find_elements(By.XPATH, f"//*[contains(@text, '{self.conf['search_filter']['excludingout_of_stock_products']}')]")
            if '품절상품 제외' in element[0].text:
                print("품절상품 제외 필터링 노출 확인")
                element_control.swipe_control(wd, selector_layer, 'left', 30)
            else:
                print("품절상품 제외 필터링 노출 확인 실패")
                test_result = 'WARN'
                warning_texts.append("필터 적용 확인 실패")
            # 뒤로가기로 카테고리 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            sleep(2)
            # 최근 검색어 있는 경우 모두 지우기로 삭제
            delete_all = wd.find_elements(By.XPATH, "//*[contains(@text, '모두 지우기')]")
            if len(delete_all) == 0:
                pass
            else:
                delete_all[0].click()
            # 뒤로가기로 카테고리 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            sleep(2)
            print("[검색 결과 화면 확인]CASE 종료")

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