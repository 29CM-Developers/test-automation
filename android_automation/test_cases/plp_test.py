import json
import logging
import os.path
import re
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
from android_automation.page_action import navigation_bar, category_page, best_product_list_page, bottom_sheet, \
    product_detail_page
from android_automation.page_action.best_product_list_page import check_best_product_page, \
    check_app_evaluation_pop_up_exposure
from android_automation.page_action.navigation_bar import move_to_category
from com_utils import values_control, element_control, api_control
from time import sleep, time
from com_utils.testrail_api import send_test_result

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
            print(f'[{test_name}] 테스트 시작')
            # 카테고리 탭 > 여성 의류 BEST
            move_to_category(wd)
            category_page.click_best_category(wd)

            # 베스트 PLP 진입 확인
            best_product_list_page.check_best_product_page(wd)

            # 일간 필터 선택
            best_product_list_page.click_period_sort(wd, '일간')

            # api로 호출한 1위 상품명과 노출되는 1위 상품명 비교
            api_oneday_product = api_control.best_plp_women_clothes(1, 'ONE_DAY')['item_name']
            oneday_product = best_product_list_page.save_best_first_product_name(wd)
            best_product_list_page.check_best_product_name(api_oneday_product, oneday_product)

            # 주간 필터 선택
            best_product_list_page.click_period_sort(wd, '주간')

            # api로 호출한 1위 상품명과 노출되는 1위 상품명 비교
            api_oneweek_product = api_control.best_plp_women_clothes(1, 'ONE_WEEK')['item_name']
            oneweek_product = best_product_list_page.save_best_first_product_name(wd)
            best_product_list_page.check_best_product_name(api_oneweek_product, oneweek_product)

            # 월간 필터 선택
            best_product_list_page.click_period_sort(wd, '월간')

            # api로 호출한 1위 상품명과 노출되는 1위 상품명 비교
            api_onemonth_product = api_control.best_plp_women_clothes(1, 'ONE_MONTH')['item_name']
            onemonth_product = best_product_list_page.save_best_first_product_name(wd)
            best_product_list_page.check_best_product_name(api_onemonth_product, onemonth_product)

            # 실시간 필터로 복귀
            best_product_list_page.click_period_sort(wd, '실시간')

            # 좋아요 버튼 선택 전, 좋아요 수 저장
            heart_count = best_product_list_page.save_best_product_like_count(wd)

            # 좋아요 버튼 선택 -> 찜하기 등록
            best_product_list_page.click_best_product_like_btn(wd)
            # 앱평가 팝업 노출 확인
            check_app_evaluation_pop_up_exposure(wd)

            heart_select = best_product_list_page.save_best_product_like_count(wd)

            # 좋아요 수 증가 확인
            best_product_list_page.check_increase_like_count(heart_count, heart_select)

            # 좋아요 버튼 선택 -> 찜하기 해제
            best_product_list_page.click_best_product_like_btn(wd)
            heart_deselect = best_product_list_page.save_best_product_like_count(wd)

            # 좋아요 수 차감 확인
            best_product_list_page.check_decrease_like_count(heart_count, heart_deselect)

            # 실시간 여성 의류 베스트 1위 상품명과 금액 저장 및 선택
            now_1st_product = api_control.best_plp_women_clothes(1, 'NOW')['item_name']
            now_1st_product_price = best_product_list_page.save_plp_price(wd)
            best_product_list_page.click_best_first_product(wd)

            # PDP 상품명 비교
            pdp_name = product_detail_page.save_product_name(wd)
            product_detail_page.check_product_name1(pdp_name, now_1st_product)

            # context_change.switch_context(wd, 'webveiw')
            #
            # # PDP 상품가격 비교
            # pdp_price = product_detail_page.save_product_price(wd)
            # product_detail_page.check_product_price(pdp_price, now_1st_product_price)
            #
            # context_change.switch_context(wd, 'native')

            # 베스트 PLP로 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # API에서 호출한 상품명 저장
            now_10th_product_prefix = api_control.best_plp_women_clothes(10, 'NOW')['item_prefix']
            now_10th_product = api_control.best_plp_women_clothes(10, 'NOW')['item_name']
            now_10th_product_name = best_product_list_page.save_api_product_name(now_10th_product_prefix,
                                                                                 now_10th_product)

            # 실시간 10위 상품 노출 확인
            best_product_list_page.find_scroll_and_find_product_rank(wd, now_10th_product_name)
            best_product_list_page.check_additional_product(wd, now_10th_product_name)

            # Home으로 복귀
            best_product_list_page.click_back_btn(wd)
            navigation_bar.move_to_home(wd)

            print(f'[{test_name}] 테스트 종료')

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
                error_texts.append(values_control.find_next_value(error_text, 'Exception'))
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
            send_test_result(self, test_result, 'PLP 기능 확인')
            wd.get('app29cm://home')
            return result_data