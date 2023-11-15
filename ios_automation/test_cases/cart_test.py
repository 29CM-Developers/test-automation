import os
import sys
import traceback
import com_utils.deeplink_control

from time import time
from com_utils import values_control
from com_utils.api_control import search_popular_keyword, search_result, product_detail
from com_utils.element_control import tap_control
from ios_automation.page_action import product_detail_page
from com_utils.deeplink_control import move_to_home


class Cart:
    def test_cart_list(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 여성의류 베스트 중 품절 상태가 아닌 첫번째 상품의 상품 번호 확인
            product_item_no = product_detail_page.save_no_soldout_product_no()

            # 딥링크로 베스트 상품 PDP 진입
            com_utils.deeplink_control.move_to_pdp(wd, product_item_no)

            # PDP 상세 API 호출하여 상품명 확인
            best_product = product_detail(product_item_no)['item_name']

            # PDP에 노출되는 상품명과 API 호출된 상품명 동일한 지 확인
            pdp_name = product_detail_page.save_product_name(wd)
            test_result = product_detail_page.check_product_name(warning_texts, pdp_name, best_product)

            # 구매하기 버튼 선택
            product_detail_page.click_purchase_btn(wd)

            # 옵션의 존재 여부 확인하여 옵션 선택
            product_detail_page.select_options(wd, product_item_no)

            # 상품 장바구니에 담기
            product_detail_page.click_put_in_cart_btn(wd)

            # 상품 장바구니에 담기 완료 바텀시트 노출 확인
            test_result = product_detail_page.check_add_product_to_cart(wd, warning_texts)

            # 바텀시트 외의 영역 선택하여 바텀시트 닫기
            tap_control(wd)

            # 인기 검색어 1위 저장
            popular_1st_keyword = search_popular_keyword()['api_1st_keyword_name']

            # 1위 인기 검색어 검색 결과의 첫번째 상품 정보 불러오기
            search_product_item_no = search_result(popular_1st_keyword, 1)['product_item_no']

            # 딥링크로 검색 상품 진입
            com_utils.deeplink_control.move_to_pdp(wd, search_product_item_no)

            # PDP 상세 API 호출하여 상품명 확인
            search_product = product_detail(search_product_item_no)['item_name']

            # PDP 상품명과 API 호출된 상품명 동일한 지 확인
            pdp_name = product_detail_page.save_product_name(wd)
            test_result = product_detail_page.check_product_name(warning_texts, pdp_name, search_product)

            # 구매하기 버튼 선택
            product_detail_page.click_purchase_btn(wd)

            # 옵션의 존재 여부 확인하여 옵션 선택
            product_detail_page.select_options(wd, search_product_item_no)

            # 상품 장바구니에 담기
            product_detail_page.click_put_in_cart_btn(wd)

            # 상품 장바구니에 담기 완료 바텀시트 노출 확인
            test_result = product_detail_page.check_add_product_to_cart(wd, warning_texts)

            # 장바구니로 이동
            product_detail_page.click_move_to_cart(wd)

            # Home 탭으로 이동
            move_to_home(self, wd)

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
            wd.get(self.conf['deeplink']['home'])

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data
