import logging
import os
import sys
import traceback
import com_utils

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
    def check_login_page(self, wd, warning_texts=[]):

        sleep(2)
        try:
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인하기')
            logger.info('로그인 페이지 진입 확인')
        except NoSuchElementException:
            test_result = 'WARN'
            warning_texts.append('로그인 페이지 진입 확인 실패')
            logger.warning('로그인 페이지 진입 확인 실패')

        wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()

        return ''

    def test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            logger.info(f'[{test_name}] 테스트 시작')

            # 카테고리 탭에서 의류>상의 카테고리 선택하여 PLP 진입 > PLP에서 좋아요 버튼 선택
            wd.get('app29cm://list/shop')
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '상의').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_btn').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="확인"]').click()

            # 로그인 페이지 진입 및 확인
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
            logger.error(f'{test_name} Error')
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def test_not_login_user_possible(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            logger.info(f'[{test_name}] 테스트 시작')

            # Home > 베스트 탭 선택하여 베스트 PLP 진입
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '베스트').click()

            # 베스트 탭에서 첫번째 상품명 저장하고 PDP 진입
            plp_name = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'product_name').text
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'product_info').click()

            # 선택한 상품의 PDP에서 상품 이름 비교
            pdp_name_text = wd.find_element(AppiumBy.XPATH,
                                            '//XCUIElementTypeWebView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther').text
            pdp_name = pdp_name_text.strip(' - 감도 깊은 취향 셀렉트샵 29CM')
            if pdp_name in plp_name:
                logger.info('PDP 진입 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('PDP 진입 확인 실패')
                logger.warning(f'PDP 진입 확인 실패 : {plp_name} / {pdp_name}')

            # PDP 상단 네비게이션의 Home 아이콘 선택하여 Home 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common home icon black').click()

            # Home > 추천 탭 상단의 타이틀 비교 (비로그인 유저 : 당신)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '추천').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '당신을 위한 추천 상품')
                logger.info('비로그인 유저 홈화면 추천 탭 타이틀 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('비로그인 유저 홈화면 추천 탭 타이틀 확인 실패')
                logger.warning('비로그인 유저 홈화면 추천 탭 타이틀 확인 실패')

            # 상단 검색 버튼 선택하여 인기 브랜드 6위 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_search_btn').click()
            search_brand = wd.find_element(AppiumBy.XPATH,
                                           '(//XCUIElementTypeOther[@name="first_popular_brand_name"])[6]')
            search_brand_name = search_brand.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text
            search_brand.click()

            # 검색 결과 화면 진입하여 선택한 브랜드명과 입력란의 문구 비교 확인
            sleep(3)
            search_input_field = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'input_keyword').text
            if search_input_field == search_brand_name:
                logger.info('인기 브랜드 검색 결과 확인 - 입력란')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 결과 확인 실패')
                logger.warning(f'인기 브랜드 검색 결과 확인 실패 : {search_brand_name} / {search_input_field}')

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            search_result_brand = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'releate_brand_name').text
            if search_brand_name in search_result_brand:
                logger.info('인기 브랜드 검색 결과 확인 - 브랜드명')
            else:
                test_result = 'WARN'
                warning_texts.append('인기 브랜드 검색 결과 확인 실패')
                logger.warning(f'인기 브랜드 검색 결과 확인 실패 : {search_brand_name} / {search_result_brand}')

            # My 탭 진입하여 로그인,회원가입 문구 노출 확인
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="MY"]').click()
            try:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="로그인·회원가입"]')
                logger.info('My 탭 로그인 문구 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('My 탭 로그인 문구 확인 실패')
                logger.warning('My 탭 로그인 문구 확인 실패')

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
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def full_test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
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
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data
