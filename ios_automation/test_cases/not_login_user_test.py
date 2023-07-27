import logging
import os
import sys
import traceback

from time import time, sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from com_utils import values_control

logger = logging.getLogger(name='log')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('|%(lineno)s||%(levelname)s| %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class NotLoginUserTest:

    # 로그인 페이지 진입 확인 메소드. [로그인하기] 버튼의 노출 여부를 판단한다.
    def check_login_page(self, wd):

        sleep(2)

        try:
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인하기')
            logger.info('로그인 페이지 진입 성공')
        except NoSuchElementException:
            logger.warning('로그인 페이지 진입 실패')

        wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()

        return ''

    def test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src=''):
        # 메소드명과 일치하는 정보 받아오기
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            # 카테고리 탭에서 의류>상의 카테고리 선택하여 PLP 진입 > PLP에서 좋아요 버튼 선택
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="CATEGORY"]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '상의').click()
            wd.find_element(AppiumBy.XPATH, '(//XCUIElementTypeButton[@name="icHeartLine"])[2]').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="확인"]').click()

            # 로그인 페이지 진입 및 확인
            NotLoginUserTest.check_login_page(self, wd)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()

            # Home 탭으로 복귀
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="HOME"]').click()

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
            # 실패 시, 딥링크 home 탭으로 이동
            logger.error(f'{test_name} Error')
            wd.get('app29cm://home')

        finally:
            run_time = f"{time() - start_time:.2f}"
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data

    def test_not_login_user_possible(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            # Category 탭으로 이동하여 추천 상품 PLP 진입
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="CATEGORY"]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'FOR YOU').click()
            try:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="당신을 위한 추천상품"]')
                logger.info('추천 카테고리 PLP 진입 성공')
            except NoSuchElementException:
                logger.warning('추천 카테고리 PLP 진입 실패')

            # 추천 상품 PLP에서 첫번째 상품 선택
            plp_product = wd.find_element(AppiumBy.XPATH,
                                          '//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="1"]')
            plp_name = plp_product.text
            plp_product.click()

            # 선택한 상품의 PDP에서 상품 이름 비교
            pdp_name = wd.find_element(AppiumBy.XPATH,
                                       '//XCUIElementTypeWebView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther').text
            if plp_name in pdp_name:
                logger.info('PDP 페이지 진입 성공')
                pass
            else:
                logger.warning(f'PDP 페이지 진입 실패 : {plp_name} / {pdp_name}')

            # 상단 검색 버튼 선택하여 인기 브랜드 10위 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common search icon black').click()
            search_brand = wd.find_element(AppiumBy.XPATH,
                                           '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="9"]/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="1"]')
            search_brand_name = search_brand.text
            search_brand.click()

            sleep(3)
            search_input_field = wd.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextField').text
            if search_input_field == search_brand_name:
                logger.info('검색 결과 화면 진입 성공')
                pass
            else:
                logger.warning(f'검색 결과 화면 진입 실패 : {search_brand_name} / {search_input_field}')

            # My 탭 진입하여 로그인,회원가입 문구 노출 확인
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            try:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="로그인·회원가입"]')
                logger.info('My 탭 로그인 문구 확인')
            except NoSuchElementException:
                logger.warning('My 탭 로그인 문구 확인 불가')

            # Home 탭으로 복귀
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="HOME"]').click()

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
            # 실패 시, 딥링크 home 탭으로 이동
            wd.get('app29cm://home')

        finally:
            run_time = f"{time() - start_time:.2f}"
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data

    def full_test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            sleep(1)

            # 주요 시나리오
            NotLoginUserTest.test_not_login_user_impossible(self, wd)

            # 상단 네비게이션 알림 버튼 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarNotiWhite').click()
            NotLoginUserTest.check_login_page(self, wd)

            # 상단 네비게이션 장바구니 버튼 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarCartWhite').click()
            NotLoginUserTest.check_login_page(self, wd)

            # LIKE 탭 선택
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="LIKE"]').click()
            NotLoginUserTest.check_login_page(self, wd)

            # PDP > 구매하기 선택
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="CATEGORY"]').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '상의').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]').click()
            sleep(2)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '구매하기').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '바로 구매하기').click()

            # 바로 구매하기 버튼 선택 시, 쿠폰 선택 바텀 시트 노출 여부 확인
            # 바텀 시트 노출 시, 바텀 시트의 닫기 버튼 선택하여 로그인 페이지 진입
            try:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="쿠폰"]')
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '닫기').click()
            except NoSuchElementException:
                pass
            NotLoginUserTest.check_login_page(self, wd)

            # Home 탭으로 복귀
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="HOME"]').click()

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
            # 실패 시, 딥링크 home 탭으로 이동
            wd.get('app29cm://home')

        finally:
            run_time = f"{time() - start_time:.2f}"
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data

