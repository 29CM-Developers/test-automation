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
from com_utils import values_control, element_control
from time import sleep, time
logger = logging.getLogger(name='Log')
logger.setLevel(logging.INFO)  ## 경고 수준 설정
formatter = logging.Formatter('|%(name)s||%(lineno)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler()  ## 스트림 핸들러 생성
stream_handler.setFormatter(formatter)  ## 텍스트 포맷 설정
logger.addHandler(stream_handler)  ## 핸들러 등록
class Plp:

    def test_product_listing_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[PLP 확인]CASE 시작")
            sleep(2)
            # 홈 > 카테고리 PLP 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'CATEGORY').click()
            # category_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/shopComposeView')
            # category_layer.find_element(AppiumBy.XPATH, '//android.view.View/android.view.View[3]/android.view.View[4]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'best_title').click()
            print("홈 > 카테고리 > 의류 > 베스트 선택")
            best_page_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtPageTitle')
            if best_page_title.text == '베스트':
                print("베스트 페이지 진입 확인")
            else:
                print("베스트 페이지 진입 확인 실패")
                test_result = 'WARN'
                warning_texts.append("베스트 페이지 진입 확인 실패")
            print(f"타이틀 문구 : {best_page_title.text} ")

            # products_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/products')

            # before_like_count = products_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.TextView').text

            # 하트 이미 선택되었는지 확인
            heart_element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'best_item_like')
            is_selected = heart_element.is_selected()
            if is_selected:
                print("하트 선택된 상태입니다.")
                heart_element.click()
                print("하트 선택 해제")
            else:
                print("하트 선택되지 않은 상태입니다.")

            before_like_count = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'best_item_like_count').text
            # 쉼표를 제거한 문자열 생성
            before_like_count = before_like_count.replace(',', '')
            # 문자열을 정수로 변환
            before_like_count = int(before_like_count)
            # products_layer.find_element(AppiumBy.XPATH,
            #                             '//android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.TextView').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'best_item_like').click()
            sleep(2)
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

            # after_like_count = products_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.TextView').text
            after_like_count = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'best_item_like_count').text
            # 좋아요 누른  좋아요 갯수 확인
            # 쉼표를 제거한 문자열 생성
            after_like_count = after_like_count.replace(',', '')
            # 문자열을 정수로 변환
            after_like_count = int(after_like_count)
            sleep(2)
            if after_like_count == before_like_count + 1:
                print(f"갯수 확인 성공 : 좋아요 누르기 전 갯수 -  {before_like_count}, 좋아요 누른 후 갯수 - {after_like_count}")
            else:
                print(f"갯수 확인 실패 : 좋아요 누르기 전 갯수 -  {before_like_count}, 좋아요 누른 후 갯수 - {after_like_count}")
                test_result = 'WARN'
                warning_texts.append("피드 아이템 좋아요 개수 증가 확인 실패")

            before_like_count = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'best_item_like_count').text

            # 좋아요 취소 누르기 전 좋아요 갯수 확인
            # 쉼표를 제거한 문자열 생성
            before_like_count = before_like_count.replace(',', '')
            # 문자열을 정수로 변환
            before_like_count = int(before_like_count)
            # products_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.TextView').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'best_item_like').click()
            # 좋아요 선택
            after_like_count = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'best_item_like_count').text
            # 좋아요 취소 누른  좋아요 갯수 확인
            # 쉼표를 제거한 문자열 생성
            after_like_count = after_like_count.replace(',', '')
            # 문자열을 정수로 변환
            after_like_count = int(after_like_count)
            sleep(2)
            if after_like_count == before_like_count - 1:
                print(f"갯수 확인 성공 : 좋아요 취소 누르기 전 갯수 -  {before_like_count}, 좋아요 취소 누른 후 갯수 - {after_like_count}")
            else:
                print(f"갯수 확인 실패 : 좋아요 취소 누르기 전 갯수 -  {before_like_count}, 좋아요 취소 누른 후 갯수 - {after_like_count}")
                test_result = 'WARN'
                warning_texts.append("피드 아이템 좋아요 개수 차감 확인 실패")
            sleep(3)

            # API 호출
            response = requests.get("https://recommend-api.29cm.co.kr/api/v4/best/items?categoryList=268100100&limit=100&offset=0&periodSort=NOW")
            if response.status_code == 200:
                api_data = response.json()
                api_data = api_data['data']['content'][9]['itemName']
                print(f"api_data :{api_data}")

                best_item_10th = element_control.scroll_to_element_with_text(wd,api_data)
                if api_data in best_item_10th.text :
                    print(" API 호출해서 불러온 상품명과 10위의 상품명이 동일한지 확인")
                else :
                    print(" API 호출해서 불러온 상품명과 10위의 상품명이 동일한지 확인 실패")
                    test_result = 'WARN'
                    warning_texts.append("API 호출해서 불러온 상품명과 10위의 상품명이 동일한지 확인 실패")
                print(f"api호출 10번째 아이템명 : {api_data} , 베스트 10위 아이템명 : {best_item_10th.text}")

                best_product_title = best_item_10th.text
                print(f"베스트 상품명 : {best_product_title} ")
                best_item_10th.click()
                sleep(2)
                PDP_title_elements = wd.find_elements(By.XPATH, f"//*[contains(@text, '{api_data}')]")
                for PDP_title in PDP_title_elements:
                    print(PDP_title.text)
                    if PDP_title.text in api_data:
                        break
                PDP_product_titile = PDP_title.text
                print(f"PDP_product_titile : {PDP_product_titile} ")
                if api_data in PDP_product_titile:
                    print("API 호출해서 불러온 상품명과 PDP 상품명이 동일한지 확인")
                else:
                    print("API 호출해서 불러온 상품명과 PDP 상품명이 동일한지 확인 실패")
                    test_result = 'WARN'
                    warning_texts.append("API 호출해서 불러온 상품명과 PDP 상품명이 동일한지 확인 실패")
                print(f"PDP 상품명 : {PDP_product_titile} ")
                # 뒤로가기로 베스트 PLP 진입 확인
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
                print("뒤로가기 선택")
                sleep(2)
                # 뒤로가기로 카테고리 진입 확인
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
                print("뒤로가기 선택")
                sleep(2)
            else:
                print("API 호출에 실패했습니다.")
            print("[PLP 확인]CASE 종료")

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