import os
import sys
import traceback
import com_utils.opencv_control

from time import time
from com_utils.code_optimization import exception_control, finally_opt
from ios_automation.page_action import order_page, delivery_order_page, bottom_sheet
from com_utils import deeplink_control


class Payment:

    def test_pay_with_virtual_account(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        order_no = ''

        try:
            print(f'[{test_name}] 테스트 시작')

            # 주문서에서 결제 수단을 무통장 입금으로 선택
            order_page.click_virtual_account(wd)

            # 주문서의 약관 모두 동의 선택
            order_page.click_all_agreement(wd)

            # 결제 전, 결제 가격 저장
            oder_page_price = order_page.save_purchase_btn_price(wd)

            # 결제하기 버튼 선택
            order_page.click_payment(wd)

            # 이니시스(무통장입금) 페이지 진입 확인
            order_page.check_inipay_page(wd)

            # 무통장 입금 결제 관련 정보 선택 후 결제 버튼 선택
            order_page.click_virtual_account_payment(wd)

            # 바텀시트 노출 여부 확인
            bottom_sheet.close_bottom_sheet(wd)

            # 주문 완료 페이지 확인
            order_page.check_done_payment(wd)

            # 주문 완료 페이지에서 주문 번호 확인
            order_no = order_page.save_order_no(wd)

            # 주문 완료 페이지의 결제방법 확인
            order_page.check_payment_type(wd, '무통장입금 (가상계좌)')

            # 주문 배송 조회 페이지 진입 버튼 선택
            order_page.click_delivery_order_tracking(wd)

            # 주문 배송 조회 페이지에서 주문 번호 확인
            delivery_order_page.check_delivery_order(wd, order_no)

            # 주문 상세 내역의 가격과 주문서 결제 가격 비교
            delivery_order_page.check_order_detail_price(wd, '무통장입금', oder_page_price)

            # 주문 조회 페이지로 뒤로가기
            delivery_order_page.click_back_btn(wd)

            # 주문 취소접수 버튼 선택
            delivery_order_page.click_order_cancel_btn(wd)

            # 주문 취소 확인
            delivery_order_page.check_order_cancel(wd)

            # Home으로 이동
            delivery_order_page.click_move_to_home(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '무통장 입금으로 상품 구매 후, 주문 배송 조회 확인'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_pay_with_credit_card(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        order_no = ''

        try:
            print(f'[{test_name}] 테스트 시작')

            # 주문서에서 결제 수단을 현대카드로 선택
            order_page.click_hyundai_card(wd)

            # 주문서의 약관 모두 동의 선택
            order_page.click_all_agreement(wd)

            # 결제 전, 결제 가격 저장
            oder_page_price = order_page.save_purchase_btn_price(wd)

            # 결제하기 버튼 선택
            order_page.click_payment(wd)

            # 핀페이 버튼 선택 후 페이지 진입 확인
            order_page.check_pinpay_page(wd)
            order_page.click_pinpay_payment(wd)

            # 화면 저장
            com_utils.opencv_control.screenshot_page(wd)

            # 키패드 저장
            com_utils.opencv_control.screenshot_keypad(wd)

            # 결제 비밀번호 선택
            com_utils.opencv_control.click_credit_password(self, wd)

            # 바텀시트 노출 여부 확인
            bottom_sheet.close_bottom_sheet(wd)

            # 주문 완료 페이지 확인
            order_page.check_done_payment(wd)

            # 주문 완료 페이지에서 주문 번호 확인
            order_no = order_page.save_order_no(wd)

            # 주문 완료 페이지의 결제방법 확인
            order_page.check_payment_type(wd, '현대카드')

            # 주문 배송 조회 페이지 진입 버튼 선택
            order_page.click_delivery_order_tracking(wd)

            # 주문 배송 조회 페이지에서 주문 번호 확인
            delivery_order_page.check_delivery_order(wd, order_no)

            # 주문 상세 내역의 가격과 주문서 결제 가격 비교
            delivery_order_page.check_order_detail_price(wd, '현대카드', oder_page_price)

            # 주문 조회 페이지로 뒤로가기
            delivery_order_page.click_back_btn(wd)

            # 주문 상태 확인 후, API로 주문 취소
            order_page.check_api_order_cancel(self, order_no)

            # Home으로 이동
            deeplink_control.move_to_home(self, wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '신용카드로 상품 구매 후, 주문 배송 조회 확인'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data
