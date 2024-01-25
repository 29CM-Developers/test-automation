import os
import sys
import traceback
from android_automation.page_action.bottom_sheet import close_bottom_sheet, close_pdp_bottom_sheet, \
    close_like_bottom_sheet
from android_automation.page_action.context_change import change_native_contexts, switch_context, \
    change_webview_contexts
from com_utils import values_control
from com_utils.api_control import product_detail, search_woman_popular_brand_name, search_result, \
    order_product_random_no
from com_utils.testrail_api import send_test_result
from android_automation.page_action import product_detail_page, order_page, like_page, navigation_bar, bottom_sheet, \
    context_change
from com_utils.deeplink_control import move_to_pdp
from time import sleep, time
from com_utils.code_optimization import finally_opt, exception_control

class Pdp:
    def test_gift_on_pdp(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 네이티브 변경
            change_native_contexts(wd)

            # 여성 인기 브랜드 1위 검색 결과 저장
            brand_name = search_woman_popular_brand_name()

            # 1위 인기 검색어 검색 결과의 첫번째 상품 정보 불러오기
            search_product_item_no = search_result(brand_name, 1)['product_item_no']

            # 딥링크로 검색 상품 진입
            move_to_pdp(wd, search_product_item_no)

            # 바텀시트 노출 여부 확인
            bottom_sheet.close_bottom_sheet(wd)

            # PDP 상세 API 호출하여 상품명 확인
            search_product = product_detail(search_product_item_no)['item_name']

            # PDP 상품명과 API 호출된 상품명 동일한 지 확인
            context_change.switch_context(wd, 'webview')

            pdp_name = product_detail_page.save_product_name(wd)
            change_native_contexts(wd)
            product_detail_page.check_product_name(pdp_name, search_product)

            # 선물하기 버튼 선택
            product_detail_page.click_gift_btn(wd)

            # 옵션의 존재 여부 확인하여 옵션 선택
            context_change.switch_context(wd, 'webview')
            product_detail_page.select_options(wd, search_product_item_no)
            change_native_contexts(wd)

            # PDP 내의 가격 저장
            pdp_price = product_detail_page.save_purchase_price(wd)

            # 선물 주문서 진입
            product_detail_page.click_direct_gift_btn(wd)

            # 선물 받는 분 정보 타이틀 확인
            order_page.check_receiver_info(wd)

            # 주문 상품 정보 상품명 확인
            order_page.check_order_product_name(wd, pdp_name)

            # 주문서 가격 비교 확인
            order_page.check_pdp_purchase_price(wd, pdp_price)

            # Home으로 복귀
            order_page.click_back_btn(wd)
            product_detail_page.click_home_btn(wd)
            print(f'[{test_name}] 테스트 종료')

        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            change_native_contexts(wd)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      'PDP에서 선물 주문서 화면으로 이동')
            return result_data

    def test_purchase_on_pdp(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 네이티브 변경
            change_native_contexts(wd)

            # 필터를 건 검색 결과 화면에서 랜덤으로 상품번호 저장
            random_product_no = order_product_random_no()

            # 딥링크로 검색 상품 진입
            move_to_pdp(wd, random_product_no)

            # 바텀시트 노출 여부 확인
            bottom_sheet.close_bottom_sheet(wd)

            # PDP 상세 API 호출하여 상품명 확인
            search_product = product_detail(random_product_no)['item_name']

            # PDP 상품명과 API 호출된 상품명 동일한 지 확인
            context_change.switch_context(wd, 'webview')
            pdp_name = product_detail_page.save_product_name(wd)
            change_native_contexts(wd)
            product_detail_page.check_product_name(pdp_name, search_product)

            # 구매하기 버튼 선택
            product_detail_page.click_purchase_btn(wd)

            # 옵션의 존재 여부 확인하여 옵션 선택
            switch_context(wd, 'webview')
            product_detail_page.select_options(wd, random_product_no)
            change_native_contexts(wd)
            sleep(5)

            # PDP 내의 가격 저장
            pdp_price = product_detail_page.save_purchase_price(wd)

            # 구매 주문서 진입
            product_detail_page.click_direct_purchase_btn(wd)

            # 배송정보 타이틀 확인
            order_page.check_delivery_info(wd)

            # 주문 상품 정보 상품명 확인
            order_page.check_order_product_name(wd, pdp_name)

            # 주문서 가격 비교 확인
            order_page.check_pdp_purchase_price(wd, pdp_price)
            print(f'[{test_name}] 테스트 종료')

        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            change_native_contexts(wd)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      'PDP에서 구매 주문서 화면으로 이동')
            return result_data

    def test_like_on_pdp(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 여성 인기 브랜드 1위 검색 결과 저장
            brand_name = search_woman_popular_brand_name()

            # 1위 인기 검색어 검색 결과의 첫번째 상품 정보 불러오기
            search_product_item_no = search_result(brand_name, 1)['product_item_no']

            # 딥링크로 검색 상품 진입
            move_to_pdp(wd, search_product_item_no)

            close_pdp_bottom_sheet(wd)
            # 바텀시트 노출 여부 확인
            bottom_sheet.close_bottom_sheet(wd)

            # PDP 상세 API 호출하여 상품명 확인
            search_product = product_detail(search_product_item_no)['item_name']

            # PDP 상품명과 API 호출된 상품명 동일한 지 확인
            context_change.switch_context(wd, 'webview')
            pdp_name = product_detail_page.save_product_name(wd)
            context_change.change_native_contexts(wd)
            product_detail_page.check_product_name(pdp_name, search_product)

            close_pdp_bottom_sheet(wd)

            # CTA영역 > 좋아요 아이콘 선택
            product_detail_page.click_like_btn(wd)

            close_pdp_bottom_sheet(wd)
            # 바텀 시트의 함께 보면 좋은 상품 타이틀, 다른고객이 함께 구매한 상품 타이틀 비교 확인
            product_detail_page.check_bottom_sheet_title(wd)

            # 딥링크로 좋아요 상품 탭 이동
            wd.get('app29cm://like')
            like_page.close_brand_recommended_page(wd)
            close_bottom_sheet(wd)
            close_like_bottom_sheet(wd)

            # 좋아요 한 상품 노출 확인
            like_product_name = like_page.save_like_product_name(wd)
            product_detail_page.check_product_name(pdp_name, like_product_name)

            # 좋아요 취소
            like_page.click_to_unlike_product(wd)

            # Home으로 복귀
            navigation_bar.move_to_home(wd)

            print(f'[{test_name}] 테스트 종료')
        except Exception:
            test_result, img_src, error_texts = exception_control(wd, sys, os, traceback, error_texts)
            wd.get('app29cm://home')
        finally:
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name,
                                      'PDP에서 선물 주문서 화면으로 이동')
            return result_data
