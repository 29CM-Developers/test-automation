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
    best_product_list_page, my_page, category_page, search_page, search_result_page


class NotLoginUserTest:

    def test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 카테고리 탭에서 의류>상의 카테고리 선택하여 PLP 진입 > PLP에서 좋아요 버튼 선택
            deeplink_control.move_to_category(self, wd)
            category_page.click_category(wd, '상의')
            category_page.click_not_login_user_product_like_btn(wd)

            # 로그인 페이지 진입 및 확인
            login_page.check_login_page(wd)

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
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
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
            send_test_result(self, test_result, '비로그인 유저가 사용 불가한 기능 사용 시도 시, 로그인 페이지에 진입')
            return result_data

    def test_not_login_user_possible(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            com_utils.deeplink_control.move_to_home_iOS(self, wd)

            # 라이프 선택 닫기
            home_page.click_close_life_tab(wd)

            # Home > 베스트 탭 선택하여 베스트 PLP 진입
            home_page.click_tab_name(wd, '베스트')

            # 베스트 탭에서 첫번째 상품명 저장하고 PDP 진입
            plp_name = best_product_list_page.save_best_first_product_name(wd)
            best_product_list_page.click_best_first_product(wd)

            # 선택한 상품의 PDP에서 상품 이름 비교
            pdp_name = product_detail_page.save_product_name(wd)
            product_detail_page.check_product_name(pdp_name, plp_name)

            # PDP 상단 네비게이션의 Home 아이콘 선택하여 Home 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # 카테고리 탭 진입
            deeplink_control.move_to_category(self, wd)

            # 추천 페이지 진입하여 상단의 타이틀 비교 (비로그인 유저 : 당신)
            category_page.click_for_you_category(wd)
            category_page.check_not_login_user_recommended_tab(wd)

            # 홈 탭으로 복귀
            category_page.click_back_btn(wd)
            navigation_bar.move_to_home(wd)

            # 상단 검색 버튼 선택하여 인기 브랜드 6위 선택
            home_page.click_search_btn(wd)
            search_brand_name = search_page.save_popular_brand_name(wd, '6')
            search_page.click_popular_brand_name(wd, '6')

            # 검색 결과 화면 진입하여 선택한 브랜드명과 입력란의 문구 비교 확인
            search_result_page.check_input_field(wd, search_brand_name)

            # 검색 결과 화면의 브랜드명에 검색어와 연관된 브랜드 확인
            search_result_page.check_relate_brand_name(wd, search_brand_name)

            # My 탭 진입하여 로그인,회원가입 문구 노출 확인
            deeplink_control.move_to_my(self, wd)
            my_page.check_login_btn(wd)

        except Exception:
            test_result = 'FAIL'
            wd.get_screenshot_as_file(sys._getframe().f_code.co_name + '_error.png')
            img_src = os.path.abspath(sys._getframe().f_code.co_name + '_error.png')
            error_text = traceback.format_exc().split('\n')
            try:
                error_texts.append(values_control.find_next_double_value(error_text, 'Traceback'))
                error_texts.append(values_control.find_next_value(error_text, 'Stacktrace'))
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
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
            login_page.check_login_page(wd)

            # 상단 네비게이션 장바구니 버튼 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarCartWhite').click()
            login_page.check_login_page(wd)

            # LIKE 탭 선택
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="LIKE"]').click()
            login_page.check_login_page(wd)

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
            login_page.check_login_page(wd)

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
