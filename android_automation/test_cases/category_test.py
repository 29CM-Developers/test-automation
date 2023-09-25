import os.path
import sys
import traceback
import logging
import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from com_utils import values_control, element_control, api_control
from time import sleep, time
logger = logging.getLogger(name='Log')
logger.setLevel(logging.INFO)  ## 경고 수준 설정
formatter = logging.Formatter('|%(name)s||%(lineno)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler()  ## 스트림 핸들러 생성
stream_handler.setFormatter(formatter)  ## 텍스트 포맷 설정
logger.addHandler(stream_handler)  ## 핸들러 등록
class Category:

    def test_category_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[카테고리 기능 사용]CASE 시작")
            sleep(3)
            # 카테고리 탭 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'CATEGORY').click()
            # 대 카테고리, 중 카테고리 코드 번호 저장
            large_category_info = api_control.large_category_info(self, self.conf['category_group'][0], self.conf['large_category'][0])
            large_category_code = large_category_info[0]
            large_category_name = large_category_info[1]
            medium_category_code = api_control.medium_category_code(self, large_category_code,self.conf['medium_category'][0])
            print(f'{large_category_code}/{large_category_name}/{medium_category_code}')

            # 신발 > 여성 > 전체 순으로 카테고리 선택
            category_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/shopComposeView')

            category_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View[@index=1]/android.widget.TextView[3]').click()
            category_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View[@index=2]/android.widget.TextView[@text="WOMEN"]').click()
            category_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View[@index=2]/android.view.View[2]/android.widget.TextView[@text="전체"]').click()

            # 타이틀명으로 카테고리 전체 페이지 진입 확인
            # API (large_category_info)에서 받아온 카테고리명으로 확인
            try:
                page_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtCategoryName')
                print(f'페이지 타이틀 : {page_title.text}')
                if '신발' in page_title.text :
                    print('카테고리 전체 페이지 진입 확인')
                else :
                    test_result = 'WARN'
                    warning_texts.append('카테고리 전체 페이지 진입 확인 실패')
                    print('WARN : 카테고리 전체 페이지 진입 확인 실패')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('카테고리 전체 페이지 진입 확인 실패')
                print('WARN : 카테고리 전체 페이지 진입 확인 실패')

            # 카테고리 전체 리스트의 첫번째 상품 확인
            response = requests.get('https://search-api.29cm.co.kr/api/v4/products/category?categoryLargeCode=270100100&count=10')
            if response.status_code == 200:
                api_data = response.json()
                products = api_data['data']['products']
                first_product_name = products[0]['itemName']
                print(f"first_product_name : {first_product_name}")
                element = element_control.scroll_to_element_with_text(wd, first_product_name)
                if element.text in first_product_name:
                    print('상품 목록의 1번째 아이템명 일치 확인')
                else :
                    test_result = 'WARN'
                    warning_texts.append('상품 목록의 1번째 아이템명 일치 확인 실패')
                    print('상품 목록의 1번째 아이템명 일치 확인 실패')
            else:
                print('카테고리 그룹 API 호출 실패')
            element = element_control.scroll_up_to_element_id(wd, '샌들')
            element.click()
            sleep(3)
            try:
                page_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/mediumCategory')
                print(f'메뉴 트리 노출 확인 : {page_title.text}')
                if '샌들' in page_title.text:
                    print('중 카테고리 페이지 진입 확인 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('중 카테고리 페이지 진입 확인 실패')
                    print('WARN : 중 카테고리 페이지 진입 확인 실패')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('중 카테고리 페이지 진입 확인 실패')
                print('WARN : 중 카테고리 페이지 진입 확인 실패')
            selector_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/selector')
            selector = selector_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View/android.view.View[1]/android.widget.TextView')
            # 필터링 버튼 선택
            selector.click()
            buttom_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/design_bottom_sheet')
            new_product_order = buttom_layer.find_element(AppiumBy.XPATH, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[2]/android.widget.TextView')
            new_product_order.click()
            sleep(1)
            print(f" 정렬 : {selector.text}")
            if '신상품순' in selector.text :
                print(f"정렬 확인 : {selector.text}")
            else :
                print(f"정렬 확인 실패 : {selector.text}")

            # 선택한 대 -> 중 카테고리에 해당하는 PLP API 호출
            response = requests.get(f'https://search-api.29cm.co.kr/api/v4/products/category?categoryLargeCode={large_category_code}&categoryMediumCode={medium_category_code}&count=50&sort=new')
            if response.status_code == 200:
                api_data = response.json()
                products = api_data['data']['products']
                first_product_name = products[0]['itemName']
                print(f"first_product_name : {first_product_name}")
                element = element_control.scroll_to_element_with_text(wd, first_product_name)
                if element.text in first_product_name :
                    print('상품 목록의 1번째 아이템명 일치 확인')
                else :
                    test_result = 'WARN'
                    warning_texts.append('상품 목록의 1번째 아이템명 일치 확인 실패')
                    print('상품 목록의 1번째 아이템명 일치 확인 실패')

                print(f"api호출 1번째 아이템명 : {first_product_name} , 아이템명 : {element.text}")
                #1번째 상품 선택 PDP진입
                element.click()
                sleep(3)
                PDP_title_elements = wd.find_elements(By.XPATH, f"//*[contains(@text, '{first_product_name}')]")
                for PDP_title in PDP_title_elements:
                    print(PDP_title.text)
                    if PDP_title.text in first_product_name:
                        break
                PDP_product_title = PDP_title.text
                print(f"PDP_product_titile : {PDP_product_title} ")
                if first_product_name in PDP_product_title:
                    print("API 호출해서 불러온 상품명과 PDP 상품명이 동일한지 확인")
                else:
                    print("API 호출해서 불러온 상품명과 PDP 상품명이 동일한지 확인 실패")
                    test_result = 'WARN'
                    warning_texts.append("API 호출해서 불러온 상품명과 PDP 상품명이 동일한지 확인 실패")
                print(f"PDP 상품명 : {PDP_product_title} ")
                # 뒤로가기로 베스트 PLP 진입 확인
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
                print("뒤로가기 선택")
                sleep(2)
                # 뒤로가기로 카테고리 진입 확인
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
                print("뒤로가기 선택")
                sleep(2)
            else:
                print('카테고리 그룹 API 호출 실패')

            print("[카테고리 확인]CASE 종료")

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