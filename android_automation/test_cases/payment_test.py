import os
import sys
import traceback

from time import time
from com_utils import values_control
from com_utils.testrail_api import send_test_result
from android_automation.page_action import order_page, delivery_order_page


class Payment:
    def test_pay_with_virtual_account(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

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

            # 주문 완료 페이지 확인
            test_result = order_page.check_done_payment(wd, warning_texts)

            # 주문 완료 페이지에서 주문 번호 확인
            order_no = order_page.save_order_no(wd)

            # 주문 완료 페이지의 결제방법 확인
            test_result = order_page.check_payment_type(wd, warning_texts, '무통장입금 (가상계좌)')

            # 주문 배송 조회 페이지 진입 버튼 선택
            order_page.click_delivery_order_tracking(wd)

            # 주문 배송 조회 페이지에서 주문 번호 확인
            test_result = delivery_order_page.check_delivery_order(wd, warning_texts, order_no)

            # 주문 상세 내역의 가격과 주문서 결제 가격 비교
            test_result = delivery_order_page.check_order_detail_price(wd, warning_texts, '무통장입금', oder_page_price)

            # 주문 조회 페이지로 뒤로가기
            delivery_order_page.click_back_btn(wd)

            # 주문 취소접수 버튼 선택
            delivery_order_page.click_order_cancel_btn(wd)

            # 주문 취소 확인
            test_result = delivery_order_page.check_order_cancel(wd, warning_texts)

            # Home으로 이동
            delivery_order_page.click_move_to_home(wd)

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
            send_test_result(self, test_result, '무통장 입금으로 상품 구매 후, 주문 배송 조회 확인')
            return result_data