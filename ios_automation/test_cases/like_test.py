import os
import sys
import traceback
import com_utils.element_control
import com_utils.cookies_control
import com_utils.deeplink_control
import com_utils.api_control

from time import time
from com_utils.code_optimization import exception_control, finally_opt
from ios_automation.page_action import welove_page, like_page, product_detail_page, context_change, selection_page, \
    my_page


class Like:
    def test_no_like_item(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 테스트 전 로그인 여부 확인
            my_page.check_login_status(self, wd, self.pconf['id2_29cm'])

            # 딥링크로 LIKE 탭 진입
            com_utils.deeplink_control.move_to_like(self, wd)

            # 상단 탭 영역 미노출 확인하여 앱 재실행
            like_page.check_restart_app(self, wd)

            # 기선택된 좋아요 있을 경우 모두 해제
            like_page.set_like_zero(self, wd)

            # 상단 Like 개수 확인
            like_page.check_like_total_count(wd, '0')

            # Product 선택 및 탭 확인
            like_page.click_product_tab(wd)
            like_page.check_no_product_like(wd)

            # Brand 탭 선택 및 확인
            like_page.click_brand_tab(wd)
            like_page.check_no_brand_like(wd)

            # POST 탭 선택 및 확인
            like_page.click_post_tab(wd)
            like_page.check_no_post_like(wd)

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '좋아요 존재하지 않는 LIKE 화면 확인'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data

    def test_like_item(self, wd, test_result='PASS', error_texts=[], img_src=''):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 테스트 전 로그인 여부 확인
            my_page.check_login_status(self, wd, self.pconf['id2_29cm'])

            # 딥링크로 LIKE 탭 진입
            com_utils.deeplink_control.move_to_like(self, wd)

            # 상단 탭 영역 미노출 확인하여 앱 재실행
            like_page.check_restart_app(self, wd)

            # 기선택된 좋아요 있을 경우 모두 해제
            like_page.set_like_zero(self, wd)

            # 추천 리스트의 첫번째 상품명 저장 및 좋아요 선택
            like_page.click_product_tab(wd)
            like_product_name = like_page.save_like_product_name(wd)
            like_page.click_product_like_btn(wd)
            selection_page.click_close_selection_pop_up(wd)

            # PRODUCT 탭 새로고침
            like_page.refresh_product_like_tab(wd)

            # 좋아요 한 상품의 상품명 비교
            like_page.check_product_like(wd, like_product_name)

            # 좋아요 한 상품의 상품명 선택
            like_page.click_product_name(wd)

            # PDP 상품 이름 저장
            pdp_product_name = product_detail_page.save_product_name(wd)

            # 종아요 한 상품명 API 호출
            liked_product_name = com_utils.api_control.my_heart_item(self.pconf['id2_29cm'],
                                                                     self.pconf['password_29cm'])

            # 좋아요 한 상품명과 PDP의 상품명 비교
            product_detail_page.check_product_name(pdp_product_name, liked_product_name)

            # pdp에서 뒤로가기 선택하여 like 탭으로 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # 좋아요 상품의 [장바구니 담기] 버튼 선택
            like_page.click_liked_product_cart_btn(wd)

            # PDP의 구매하기 모달 확인 후 닫기
            product_detail_page.check_open_to_purchase_modal(wd)
            product_detail_page.close_purchase_modal(wd)

            # PDP 상품 이름 저장
            pdp_product_name = product_detail_page.save_product_name(wd)

            # 좋아요 한 상품명과 PDP의 상품명 비교
            product_detail_page.check_product_name(pdp_product_name, liked_product_name)

            # pdp에서 뒤로가기 선택하여 like 탭으로 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # # 그리드 뷰 상태에서 이미지 사이즈 저장
            # grid_size = like_page.save_grid_image_size(wd)
            #
            # # 리스트 뷰 상태로 전환
            # like_page.click_change_view_type_to_list(wd)
            #
            # # 리스트 뷰 상태에서 이미지 사이즈 저장
            # list_size = like_page.save_list_image_size(wd)
            # like_page.check_veiw_image_size(grid_size['height'], grid_size['width'], list_size['height'],
            #                                 list_size['width'])
            #
            # # 그리드 뷰로 복귀
            # like_page.click_change_view_type_to_grid(wd)

            # Brand 탭 선택
            like_page.click_brand_tab(wd)

            # 추천 리스트의 첫번째 브랜드명 저장 및 좋아요 선택
            like_brand_name = like_page.save_like_brand_name(wd)
            like_page.click_brand_like_btn(wd)

            # BRAND 탭 새로고침
            like_page.refresh_brand_like_tab(wd)

            # 좋아요 한 브랜드명 비교
            like_page.check_brand_like(wd, like_brand_name)

            # 브랜드명 선택
            like_page.click_liked_brand_name(wd)

            # webview 전환
            context_change.switch_context(wd, 'webview')

            # 브랜드 PLP에서 브랜드명 비교 확인
            like_page.check_brand_page_name(wd, like_brand_name)

            # native 전환
            context_change.switch_context(wd, 'native')

            # 브랜드 PLP에서 좋아요 페이지로 복귀
            like_page.click_brand_back_btn(wd)

            # 좋아요 브랜드의 첫번쨰 상품 선택하여 해당 상품 PDP 진입
            liked_brand_product_name = like_page.save_liked_brand_product_name(wd)
            like_page.click_liked_brand_product_name(wd)
            pdp_product_name = product_detail_page.save_product_name(wd)
            product_detail_page.check_product_name(pdp_product_name, liked_brand_product_name)

            # Like 탭으로 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # 포스트 탭 선택
            like_page.click_post_tab(wd)

            # 추천 게시물 페이지로 이동
            like_page.move_to_welove_page(wd)

            context_change.switch_context(wd, 'webview')

            # 첫번째 추천 게시물명 확인 및 선택
            like_post_name = welove_page.save_first_post_title(wd)
            welove_page.click_first_post(wd)

            # post 내 좋아요 버튼 선택
            welove_page.click_post_like_btn(wd)

            # native 전환
            context_change.switch_context(wd, 'native')

            # LIKE 탭으로 복귀
            welove_page.click_post_to_welove_back_btn(wd)
            welove_page.click_welove_back_btn(wd)

            # POST 탭 새로고침
            like_page.refresh_post_like_tab(wd)

            # 좋아요 한 게시물명 확인
            like_page.check_post_like(wd, like_post_name)

            # 상단 Like 개수 확인
            like_page.check_like_total_count(wd, "3")

            # 포스트 좋아요 해제
            like_page.click_to_unlike_post(wd)

            # 브랜드 좋아요 해제
            like_page.click_brand_tab(wd)
            like_page.click_to_unlike_brand(wd)

            # 상품 좋아요 해제
            like_page.click_product_tab(wd)
            like_page.click_to_unlike_product(wd)

            # 상단 Like 개수 확인
            like_page.check_like_total_count(wd, "0")

        except Exception:
            test_result, img_src, error_texts = exception_control(self, wd, sys, os, traceback, error_texts)

        finally:
            testcase_title = '좋아요 존재하는 LIKE 화면 확인'
            result_data = finally_opt(self, start_time, test_result, error_texts, img_src, test_name, testcase_title)
            return result_data
