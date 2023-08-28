import logging
import os.path
import subprocess
import sys
import traceback
import logging
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.mobileby import MobileBy
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

class NotLogin:

    def test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[사용 불가 기능 사용]CASE 시작")
            sleep(3)
            # 홈 > 카테고리 PLP 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'CATEGORY').click()
            category_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/shopComposeView')
            category_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View[3]/android.view.View[6]').click()
            print("홈 > 카테고리 PLP 진입 > 의류 > 상의 선택")
            # 임의의 상품 좋아요 버튼 선택
            plp_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/recyclerview')
            plp_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[1]/android.widget.ImageView[2]').click()
            print("좋아요 선택")
            # 로그인 화면 진입 확인
            login_page_title = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.widget.TextView[1]')
            if login_page_title.text == '로그인':
                print("로그인 진입 확인 : 로그인 문구 확인")
            else:
                print("로그인 진입 확인 : 로그인 문구 실패")
                test_result = 'WARN'
                warning_texts.append("로그인 진입 확인 실패")
            print(f"가이드 문구 : {login_page_title.text} ")

            # 뒤로가기로 카테고리 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            sleep(1)
            # 뒤로가기로 홈화면 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()

            #full test 확장 시나리오
            # 홈 > 우상단 알림 아이콘 선택
            sleep(2)
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgInboxNotification').click()
            print("홈 > 우상단 알림 아이콘 선택")
            # 로그인 화면 진입 확인
            login_page_title = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.widget.TextView[1]')
            if login_page_title.text == '로그인':
                print("로그인 진입 확인 : 로그인 문구 확인")
            else:
                print("로그인 진입 확인 : 로그인 문구 실패")
                test_result = 'WARN'
                warning_texts.append("로그인 진입 확인 실패")
            print(f"가이드 문구 : {login_page_title.text} ")

            # 뒤로가기로 홈화면 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")

            # 홈 > 우상단 장바구니 아이콘 선택
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgCart').click()
            print("홈 > 우상단 장바구니 아이콘 선택")
            # 로그인 화면 진입 확인
            login_page_title = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.widget.TextView[1]')
            if login_page_title.text == '로그인':
                print("로그인 진입 확인 : 로그인 문구 확인")
            else:
                print("로그인 진입 확인 : 로그인 문구 실패")
                test_result = 'WARN'
                warning_texts.append("로그인 진입 확인 실패")
            print(f"가이드 문구 : {login_page_title.text} ")

            # 뒤로가기로 홈화면 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            # 하단 like 아이콘 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'LIKE').click()
            print("하단 like 아이콘 선택")
            # 로그인 화면 진입 확인
            login_page_title = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.widget.TextView[1]')
            if login_page_title.text == '로그인':
                print("로그인 진입 확인 : 로그인 문구 확인")
            else:
                print("로그인 진입 확인 : 로그인 문구 실패")
                test_result = 'WARN'
                warning_texts.append("로그인 진입 확인 실패")
            print("가이드 문구 : %s " % login_page_title.text)

            # 뒤로가기로 홈화면 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            print("[사용 불가 기능 사용]CASE 종료")

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

    def test_not_login_user_possible(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):

        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[사용 가능 기능 사용]CASE 시작")
            sleep(2)
            element_control.scroll(wd)
            tab_title_elements = wd.find_elements(AppiumBy.XPATH, '//*[@resource-id="com.the29cm.app29cm:id/tabTitle"]')

            # "베스트 문구"를 찾을 변수 초기화
            best_tab_title = None

            # tab_title_elements를 반복하면서 "베스트 문구"를 찾기
            for tab_title_element in tab_title_elements:
                # 각 요소의 텍스트를 가져와서 비교
                tab_title_text = tab_title_element.text
                if tab_title_text == "베스트":
                    best_tab_title = tab_title_element
                    break

            # "베스트 문구"가 있는지 확인하고 결과 출력
            if best_tab_title is not None:
                print("베스트탭을 찾았습니다.")
                tab_title_element.click()
                print("베스트 탭 선택")
            else:
                print("베스트 문구 탭을 찾지 못했습니다.")

            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/all').click()
            print("전체보기 버튼 선택")
            sleep(1)
            best_page_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtPageTitle')
            if best_page_title.text == '베스트':
                print("베스트 페이지 진입 확인")
            else:
                print("베스트 페이지 진입 확인 실패")
                test_result = 'WARN'
                warning_texts.append("베스트 페이지 진입 확인 실패")
            print(f"타이틀 문구 : {best_page_title.text} ")
            best_product_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/products')
            best_product_title = best_product_layer.find_element(AppiumBy.XPATH, '//android.widget.TextView[2]').text
            print(f"베스트 상품명 : {best_product_title} ")
            wd.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[1]/android.view.ViewGroup').click()
            element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=3]'
            PDP_product_titile = wd.find_element(AppiumBy.XPATH, element_xpath).text
            print(f"PDP_product_titile : {PDP_product_titile} ")
            if PDP_product_titile in best_product_title:
                print("베스트 상품 PDP 정상 확인")
            else:
                print("베스트 상품 PDP 정상 확인 실패")
                test_result = 'WARN'
                warning_texts.append("베스트 상품 PDP 정상 확인 실패")
            print(f"베스트 상품명 : {best_product_title} , PDP 상품명 : {PDP_product_titile}  ")

            # 상단으로 홈화면 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgHome').click()
            print("상단 홈아이콘 선택")
            # 8. 홈 > 피드 > 추천 탭선택
            sleep(1)
            element_control.scroll(wd)
            sleep(1)
            tab_title_elements = wd.find_elements(AppiumBy.XPATH, '//*[@resource-id="com.the29cm.app29cm:id/tabTitle"]')

            # "추천 문구"를 찾을 변수 초기화
            rec_tab_title = None

            # tab_title_elements를 반복하면서 "추천 문구"를 찾기
            for tab_title_element in tab_title_elements:
                # 각 요소의 텍스트를 가져와서 비교
                tab_title_text = tab_title_element.text
                if tab_title_text == "추천":
                    rec_tab_title = tab_title_element
                    break

            if rec_tab_title is None:
                print("recommend not found swipe")
                element_control.swipe_control(wd, tab_title_element,'left',30)
                # element_control.swipe_right_to_left(wd, tab_title_element)
            # "추천"탭 있는지 확인하고 결과 출력
            # if rec_tab_title is not None:
            else :
                print("추천탭을 찾았습니다.")
                tab_title_element.click()
                print("추천 탭 선택")
                guide_text = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/textRecommend')

                if guide_text.text == '당신을 위한 추천 상품':
                    print("'당신을 위한 추천 상품’ 가이드 문구 노출 확인")
                else:
                    print("'당신을 위한 추천 상품' 가이드 문구 노출 실패")
                    test_result = 'WARN'
                    warning_texts.append("추천 가이드 문구 확인 실패")
                print(f"가이드 문구 : {guide_text.text} ")

            # 6. Home 상단 네비게이션 검색 아이콘 선택
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgSearch').click()
            print("상단 검색 아이콘 선택")
            search_container = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/container')

            # 최근 검색어 있는 경우 모두 지우기로 삭제
            delete_all = wd.find_elements(By.XPATH, "//*[contains(@text, '모두 지우기')]")
            print(delete_all)
            if len(delete_all)==0 :
                pass
            else :
                delete_all[0].click()

            # 지금 많이 찾는 브랜드 찾기
            element_xpath = '//androidx.compose.ui.platform.ComposeView[2]/android.view.View/android.view.View/android.widget.TextView[1]'
            search_container_title = search_container.find_element(AppiumBy.XPATH, element_xpath)
            if search_container_title.text == '지금 많이 찾는 브랜드':
                pass
            else :
                print("지금 많이 찾는 브랜드 타이틀 노출 실패")
                test_result = 'WARN'
                warning_texts.append("지금 많이 찾는 브랜드 타이틀 노출 실패")
            print(f"타이틀 확인 : {search_container_title.text}")

            brand_10th = search_container.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[10]')
            # 7. 검색 화면 > 인기 브랜드 검색어 10위 선택
            brand_10th_name = brand_10th.find_element(AppiumBy.XPATH, '//android.widget.TextView[2]').text
            brand_10th.click()
            print('브랜드 10위 선택')
            print(brand_10th_name)
            # 확인3-1 : 선택한 브랜드명과 입력란에 작성된 문구가 동일한지 확인
            search_edit_text = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/searchEditText').text
            if search_edit_text == brand_10th_name:
                print("선택한 브랜드명과 입력란에 작성된 문구가 동일 확인")
            else:
                print("선택한 브랜드명과 입력란에 작성된 문구가 동일 실패")
                test_result = 'WARN'
                warning_texts.append("브랜드명 비교 실패")
            print(f"검색어 : {search_edit_text} ")
            # 확인3-2 : 브랜드 영역에 노출되는 브랜드와 검색한 브랜드명이 동일한지 확인
            brand_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/searchResultBrandComposeView')
            search_brand = brand_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View[1]/android.widget.TextView[1]').text
            if search_brand == brand_10th_name:
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
            sleep(1)
            # 뒤로가기로 카테고리 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            print("뒤로가기 선택")
            # 8. MY 탭 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'MY').click()
            print("하단 마이페이지 화면 진입")

            # 로그인 회원가입 버튼 선택
            # 확인4 : 프로필 영역의 로그인.회원가입 문구 확인
            not_login = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtLogin').text
            if not_login == '로그인·회원가입':
                print("프로필 영역의 로그인.회원가입 문구 확인")
            else:
                print("프로필 영역의 로그인.회원가입 문구 확인 실패")
                test_result = 'WARN'
                warning_texts.append("프로필 영역의 로그인.회원가입 문구 확인 실패")
            print(f"프로필 영역의 문구 확인 : {not_login} ")
            print("[사용 가능 기능 사용]CASE 종료")



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