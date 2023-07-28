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

            # Home 탭으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()
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
            # Home > 베스트 탭 선택하여 베스트 PLP 진입
            wd.execute_script('mobile:swipe', {'direction': 'up'})
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '베스트').click()
            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="전체보기"]').click()

            # 베스트 PLP에서 첫번째 상품명 저장하고 PDP 진입
            plp_product = wd.find_element(AppiumBy.XPATH,
                                          '//XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="1"]')
            plp_name = plp_product.text
            plp_product.click()

            # 선택한 상품의 PDP에서 상품 이름 비교
            pdp_name_text = wd.find_element(AppiumBy.XPATH,
                                       '//XCUIElementTypeWebView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther').text
            pdp_name = pdp_name_text.strip(' - 감도 깊은 취향 셀렉트샵 29CM')
            if pdp_name in plp_name:
                logger.info('PDP 페이지 진입 성공')
            else:
                logger.warning(f'PDP 페이지 진입 실패 : {plp_name} / {pdp_name}')

            # PDP 상단 네비게이션의 Home 아이콘 선택하여 Home 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common home icon black').click()

            # Home > 추천 탭 상단의 타이틀 비교 (비로그인 유저 : 당신)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '추천').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '당신을 위한 추천 상품')
                logger.info('비로그인 유저 추천 탭 진입 확인')
            except NoSuchElementException:
                logger.warning('비로그인 유저 추천 탭 진입 실패')

            # 상단 검색 버튼 선택하여 인기 브랜드 10위 선택
            # 상단 검색 버튼명(색상)이 스크롤 정도에 따라 다르게 노출되어 try-except문으로 확인(하얀색이 아니면 검정색으로)
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarSearchWhite').click()
            except:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarSearchBlack').click()
            search_brand = wd.find_element(AppiumBy.XPATH,
                                           '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="9"]/XCUIElementTypeOther/XCUIElementTypeStaticText[@index="1"]')
            search_brand_name = search_brand.text
            search_brand.click()

            # 검색 결과 화면 진입하여 선택한 브랜드명과 입력란의 문구 비교 확인
            sleep(3)
            search_input_field = wd.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextField').text
            if search_input_field == search_brand_name:
                logger.info('검색 결과 화면 진입 성공')
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

