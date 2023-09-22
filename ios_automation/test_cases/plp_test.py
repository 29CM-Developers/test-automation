import os
import sys
import traceback
from time import time, sleep

import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException

from com_utils import values_control


class Plp:
    def test_product_listing_page(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        print(f'[{test_name}] 테스트 시작')

        try:
            wd.execute_script('mobile:swipe', {'direction': 'up'})

            # 홈 카테고리의 BEST 탭 > 전체 보기 통해서 베스트 PLP 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '베스트').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="전체보기"]').click()

            try:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="베스트"]')
                print('베스트 PLP 진입 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                error_texts = '베스트 PLP 진입 확인 실패'
                print('베스트 PLP 진입 확인 실패')

            # 베스트 PLP의 두번째 상품 좋아요 버튼과 개수 element 확인
            product_1st = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView[@index="2"]/XCUIElementTypeCell[@index="1"]')
            try:
                product_1st_heart_btn = product_1st.find_element(AppiumBy.XPATH,
                                                                 '//XCUIElementTypeOther[@index="4"]/XCUIElementTypeButton')
                product_1st_heart_text = product_1st_heart_btn.find_element(AppiumBy.XPATH,
                                                                            '//XCUIElementTypeStaticText')
            except NoSuchElementException:
                product_1st_heart_btn = product_1st.find_element(AppiumBy.XPATH,
                                                                 '//XCUIElementTypeOther[@index="3"]/XCUIElementTypeButton')
                product_1st_heart_text = product_1st_heart_btn.find_element(AppiumBy.XPATH,
                                                                            '//XCUIElementTypeStaticText')

            # 좋아요 버튼 선택 전, 좋아요 수 저장
            heart_count = product_1st_heart_text.text
            heart_count = int(heart_count.replace(',', ''))

            # 좋아요 버튼 선택 -> 찜하기 등록
            product_1st_heart_btn.click()
            sleep(1)
            heart_select = product_1st_heart_text.text
            heart_select = int(heart_select.replace(',', ''))
            if heart_select == heart_count + 1:
                print('아이템 좋아요 개수 증가 확인')
                pass
            else:
                test_result = 'WARN'
                warning_texts.append('아이템 좋아요 개수 증가 확인 실패')
                print(f'아이템 좋아요 개수 증가 확인 실패: {heart_count} / {heart_select}')

            # 좋아요 버튼 선택 -> 찜하기 해제
            product_1st_heart_btn.click()
            sleep(1)
            heart_select = product_1st_heart_text.text
            heart_select = int(heart_select.replace(',', ''))
            if heart_select == heart_count:
                print('아이템 좋아요 개수 차감 확인')
                pass
            else:
                test_result = 'WARN'
                warning_texts.append('아이템 좋아요 개수 차감 확인 실패')
                print(f'아이템 좋아요 개수 차감 확인 실패: {heart_count} / {heart_select}')

            # 여성의류 실시간 베스트 API 호출
            response = requests.get('https://recommend-api.29cm.co.kr/api/v4/best/items?categoryList=268100100&periodSort=NOW&limit=100&offset=0')
            if response.status_code == 200:
                best_product_data = response.json()

                # 10번째 상품의 상품명 저장
                best_product_10th_prefix = best_product_data['data']['content'][9]['subjectDescriptions']
                best_product_10th_itemname = best_product_data['data']['content'][9]['itemName']
                if not best_product_10th_prefix:
                    best_product_10th_name = f'{best_product_10th_itemname}'
                else:
                    best_product_10th_name = f'{best_product_10th_prefix[0]} {best_product_10th_itemname}'
                print(best_product_10th_name)

                # 10번째 상품 선택 (화면에 미노출 시, 노출 될때까지 스크롤)
                for i in range(0, 10):
                    try:
                        best_product_10th = wd.find_element(AppiumBy.ACCESSIBILITY_ID, best_product_10th_name)
                        best_product_10th.click()
                        break
                    except NoSuchElementException:
                        wd.execute_script('mobile:swipe', {'direction': 'up'})

                # PDP 상품 이름 저장 -> 이미지 1개일 경우와 2개 이상일 경우, XPATH index 변경되어 아래와 같이 작성
                pdp_web = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView')
                try:
                    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'Select a slide to show')
                    pdp_name = pdp_web.find_element(AppiumBy.XPATH,
                                                    '//XCUIElementTypeOther[@index="5"]/XCUIElementTypeStaticText').get_attribute('name')
                except NoSuchElementException:
                    pdp_name = pdp_web.find_element(AppiumBy.XPATH,
                                                    '//XCUIElementTypeOther[@index="4"]/XCUIElementTypeStaticText').get_attribute('name')

                # 선택한 상품의 PDP에서 상품 이름 비교
                if best_product_10th_itemname.strip() in pdp_name:
                    print('PDP 진입 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('PDP 진입 확인 실패')
                    print(f'PDP 진입 확인 실패 : {best_product_10th_itemname} / {pdp_name}')

                # PDP 상단 네비게이션의 Home 아이콘 선택하여 Home 복귀
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common home icon black').click()

            else:
                test_result = 'WARN'
                warning_texts.append('베스트 PLP API 불러오기 실패')
                print('베스트 PLP API 불러오기 실패')

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
            wd.get(self.conf['deeplink']['home'])

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

