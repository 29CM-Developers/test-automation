import os
import sys
import traceback
from time import time, sleep

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
            product_2nd = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView[@index="2"]/XCUIElementTypeCell[@index="2"]')
            product_2nd_heart_btn = product_2nd.find_element(AppiumBy.XPATH, '//XCUIElementTypeOther[@index="3"]/XCUIElementTypeButton')
            product_2nd_heart_text = product_2nd_heart_btn.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText')

            # 좋아요 버튼 선택 전, 좋아요 수 저장
            heart_count = product_2nd_heart_text.text
            heart_count = int(heart_count.replace(',', ''))

            # 좋아요 버튼 선택 -> 찜하기 등록
            product_2nd_heart_btn.click()
            sleep(1)
            heart_select = product_2nd_heart_text.text
            heart_select = int(heart_select.replace(',', ''))
            if heart_select == heart_count + 1:
                print('아이템 좋아요 개수 증가 확인')
                pass
            else:
                test_result = 'WARN'
                warning_texts.append('아이템 좋아요 개수 증가 확인 실패')
                print(f'아이템 좋아요 개수 증가 확인 실패: {heart_count} / {heart_select}')

            # 좋아요 버튼 선택 -> 찜하기 해제
            product_2nd_heart_btn.click()
            sleep(1)
            heart_select = product_2nd_heart_text.text
            heart_select = int(heart_select.replace(',', ''))
            if heart_select == heart_count:
                print('아이템 좋아요 개수 차감 확인')
                pass
            else:
                test_result = 'WARN'
                warning_texts.append('아이템 좋아요 개수 차감 확인 실패')
                print(f'아이템 좋아요 개수 차감 확인 실패: {heart_count} / {heart_select}')

            # 베스트 PLP의 첫번째 상품명 저장 후 선택
            product_1st = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView[@index="2"]/XCUIElementTypeCell[@index="1"]')
            product_1st_name = product_1st.find_element(AppiumBy.XPATH, '//XCUIElementTypeOther[@index="1"]/XCUIElementTypeStaticText[@index="1"]')
            product_1st_name_text = product_1st_name.text
            product_1st_name.click()
            sleep(3)

            # 선택한 상품의 PDP에서 상품 이름 비교
            pdp_web = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView')
            pdp_name = pdp_web.find_element(AppiumBy.XPATH, '//XCUIElementTypeOther[@index="5"]/XCUIElementTypeStaticText').get_attribute('name')

            if pdp_name in product_1st_name_text:
                print('PDP 진입 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('PDP 진입 확인 실패')
                print(f'PDP 진입 확인 실패 : {product_1st_name_text} / {pdp_name}')

            # PDP 상단 네비게이션의 Home 아이콘 선택하여 Home 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common home icon black').click()

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
            wd.get('app29cm://home')

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data
