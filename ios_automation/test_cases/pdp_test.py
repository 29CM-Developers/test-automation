import os
import sys
import traceback
from time import time

from com_utils import values_control
from com_utils.db_connection import connect_db, insert_data, disconnect_db
from com_utils.api_control import product_detail, search_woman_popular_brand_name, search_result, \
    order_product_random_no
from com_utils.testrail_api import send_test_result
from ios_automation.page_action import context_change, product_detail_page, order_page, like_page, navigation_bar
from com_utils.deeplink_control import move_to_pdp_iOS, move_to_like, move_to_home_iOS


class Pdp:
    def test_like_on_pdp(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 여성 인기 브랜드 1위 검색 결과 저장
            brand_name = search_woman_popular_brand_name()

            # 1위 인기 검색어 검색 결과의 첫번째 상품 정보 불러오기
            search_product_item_no = search_result(brand_name, 1)['product_item_no']

            # 딥링크로 검색 상품 진입
            move_to_pdp_iOS(wd, search_product_item_no)

            # PDP의 상품명 저장
            pdp_name = product_detail_page.save_remove_prefix_product_name(wd)

            # CTA의 좋아요 버튼 선택
            product_detail_page.click_like_btn(wd)

            # 바텀시트 최대로 확장하여 바텀시트 내 타이틀 확인 > 바텀 시트 닫기
            product_detail_page.move_like_bottom_sheet(wd, 'D')
            product_detail_page.check_like_bottom_sheet(wd)
            product_detail_page.move_like_bottom_sheet(wd, 'U')
            product_detail_page.move_like_bottom_sheet(wd, 'U')

            # 딥링크로 Like 탭 이동
            move_to_like(self, wd)

            # Like 탭에서 좋아요 한 상품 노출 확인 > 좋아요 해제
            like_page.refresh_product_like_tab(wd)
            like_page.check_product_like(wd, pdp_name)
            like_page.click_to_unlike_product(wd)
            like_page.refresh_product_like_tab(wd)

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
            context_change.switch_context(wd, 'native')
            move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, 'PDP에서 좋아요 선택하기')
            connection, cursor = connect_db(self)
            insert_data(connection, cursor, self, result_data)
            disconnect_db(connection, cursor)
            return result_data

    def test_gift_on_pdp(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 여성 인기 브랜드 1위 검색 결과 저장
            brand_name = search_woman_popular_brand_name()

            # 1위 인기 검색어 검색 결과의 첫번째 상품 정보 불러오기
            search_product_item_no = search_result(brand_name, 1)['product_item_no']

            # 딥링크로 검색 상품 진입
            move_to_pdp_iOS(wd, search_product_item_no)

            # PDP 상세 API 호출하여 상품명 확인
            search_product = product_detail(search_product_item_no)['item_name']

            # PDP 상품명과 API 호출된 상품명 동일한 지 확인
            pdp_name = product_detail_page.save_remove_prefix_product_name(wd)
            product_detail_page.check_product_name(pdp_name, search_product)

            # 선물하기 버튼 선택
            product_detail_page.click_gift_btn(wd)

            # 옵션의 존재 여부 확인하여 옵션 선택
            product_detail_page.select_options(wd, search_product_item_no)

            # PDP 내의 가격 저장
            pdp_price = product_detail_page.save_purchase_price(wd)

            # 선물 주문서 진입
            product_detail_page.click_direct_gift_btn(wd)

            # 선물 받는 분 정보 타이틀 확인
            order_page.check_receiver_info(wd)

            # 주문 상품 정보 상품명 확인
            order_page.check_order_product_name(wd, pdp_name)

            # 주문서 가격 비교 확인
            order_page.check_purchase_price(wd, pdp_price)

            # Home으로 복귀
            order_page.click_back_btn(wd)
            product_detail_page.click_home_btn(wd)

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
            context_change.switch_context(wd, 'native')
            move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, 'PDP에서 선물 주문서 화면으로 이동')
            connection, cursor = connect_db(self)
            insert_data(connection, cursor, self, result_data)
            disconnect_db(connection, cursor)
            return result_data

    def test_purchase_on_pdp(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 필터를 건 검색 결과 화면에서 랜덤으로 상품번호 저장
            random_product_no = order_product_random_no()

            # 딥링크로 검색 상품 진입
            move_to_pdp_iOS(wd, random_product_no)

            # PDP 상세 API 호출하여 상품명 확인
            search_product = product_detail(random_product_no)['item_name']

            # PDP 상품명과 API 호출된 상품명 동일한 지 확인
            pdp_name = product_detail_page.save_remove_prefix_product_name(wd)
            product_detail_page.check_product_name(pdp_name, search_product)

            # 구매하기 버튼 선택
            product_detail_page.click_purchase_btn(wd)

            # 옵션의 존재 여부 확인하여 옵션 선택
            product_detail_page.select_options(wd, random_product_no)

            # PDP 내의 가격 저장
            pdp_price = product_detail_page.save_purchase_price(wd)

            # 구매 주문서 진입
            product_detail_page.click_direct_purchase_btn(wd)

            # 배송정보 타이틀 확인
            order_page.check_delivery_info(wd)

            # 주문 상품 정보 상품명 확인
            order_page.check_order_product_name(wd, pdp_name)

            # 주문서 가격 비교 확인
            order_page.check_purchase_price(wd, pdp_price)

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
            context_change.switch_context(wd, 'native')
            move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, 'PDP에서 구매 주문서 화면으로 이동')
            connection, cursor = connect_db(self)
            insert_data(connection, cursor, self, result_data)
            disconnect_db(connection, cursor)
            return result_data
