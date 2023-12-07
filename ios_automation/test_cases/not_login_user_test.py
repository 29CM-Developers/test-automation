import logging
import os
import sys
import traceback
import com_utils

from time import time, sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from com_utils import values_control, deeplink_control
from com_utils.testrail_api import send_test_result
from ios_automation.page_action import navigation_bar, login_page, home_page, product_detail_page, \
    best_product_list_page, my_page

logger = logging.getLogger(name='log')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('|%(lineno)s||%(levelname)s| %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class NotLoginUserTest:

    def test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            logger.info(f'[{test_name}] 테스트 시작')

            sleep(1)
            # 카테고리 탭에서 의류>상의 카테고리 선택하여 PLP 진입 > PLP에서 좋아요 버튼 선택
            deeplink_control.move_to_category(self, wd)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '상의').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_btn').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="확인"]').click()

            # 로그인 페이지 진입 및 확인
            test_result = login_page.check_login_page(wd, test_result, warning_texts)

            # Home 탭으로 복귀
            navigation_bar.move_to_home(wd)

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
            send_test_result(self, test_result, '비로그인 유저가 사용 불가한 기능 사용 시도 시, 로그인 페이지에 진입')
            return result_data

    def test_not_login_user_possible(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            logger.info(f'[{test_name}] 테스트 시작')

            # 라이프 선택 닫기
            home_page.click_close_life_tab(wd)

            # Home > 베스트 탭 선택하여 베스트 PLP 진입
            home_page.click_tab_name(wd, '베스트')

            # 베스트 탭에서 첫번째 상품명 저장하고 PDP 진입
            plp_name = best_product_list_page.save_best_first_product_name(wd)
            best_product_list_page.click_best_first_product(wd)

            # 선택한 상품의 PDP에서 상품 이름 비교
            pdp_name = product_detail_page.save_product_name(wd)
            test_result = product_detail_page.check_product_name(test_result, warning_texts, pdp_name, plp_name)

            # PDP 상단 네비게이션의 Home 아이콘 선택하여 Home 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # Home > 추천 탭 상단의 타이틀 비교 (비로그인 유저 : 당신)
            home_page.click_tab_name(wd, '추천')
            test_result = home_page.check_not_login_user_recommended_tab(wd, test_result, warning_texts)

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
            deeplink_control.move_to_my(self, wd)
            test_result = my_page.check_login_btn(wd, warning_texts)

            # Home 탭으로 복귀
            navigation_bar.move_to_home(wd)

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
            send_test_result(self, test_result, '비로그인 유저가 사용 가능한 기능 확인')
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
            login_page.check_login_page(wd, test_result, warning_texts)

            # 상단 네비게이션 장바구니 버튼 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarCartWhite').click()
            login_page.check_login_page(wd, test_result, warning_texts)

            # LIKE 탭 선택
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="LIKE"]').click()
            login_page.check_login_page(wd, test_result, warning_texts)

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
            login_page.check_login_page(wd, test_result, warning_texts)

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
