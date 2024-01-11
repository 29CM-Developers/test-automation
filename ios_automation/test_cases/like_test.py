import os
import sys
import traceback
import com_utils.element_control
import com_utils.cookies_control
import com_utils.deeplink_control
import com_utils.api_control

from time import time
from com_utils import values_control
from com_utils.testrail_api import send_test_result
from ios_automation.page_action import welove_page, like_page, navigation_bar, product_detail_page, context_change


class Like:
    def test_no_like_item(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 딥링크로 LIKE 탭 진입
            com_utils.deeplink_control.move_to_like(self, wd)

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
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '좋아요 존재하지 않는 LIKE 화면 확인')
            return result_data

    def test_like_item(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 딥링크로 LIKE 탭 진입
            com_utils.deeplink_control.move_to_like(self, wd)

            # 추천 리스트의 첫번째 상품명 저장 및 좋아요 선택
            like_product_name = like_page.save_like_product_name(wd)
            like_page.click_product_like_btn(wd)

            # PRODUCT 탭 새로고침
            like_page.refresh_product_like_tab(wd)

            # 좋아요 한 상품의 상품명 비교
            like_page.check_product_like(wd, like_product_name)

            # 좋아요 한 상품의 상품명 선택
            like_page.click_product_name(wd)

            # PDP 상품 이름 저장
            pdp_product_name = product_detail_page.save_product_name(wd)

            # 좋아요 한 상품명과 PDP의 상품명 비교
            product_detail_page.check_product_name(pdp_product_name, like_product_name)

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
            product_detail_page.check_product_name(pdp_product_name, like_product_name)

            # pdp에서 뒤로가기 선택하여 like 탭으로 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # 그리드 뷰 상태에서 이미지 사이즈 저장
            grid_size = like_page.save_grid_image_size(wd)

            # 리스트 뷰 상태로 전환
            like_page.click_change_view_type_to_list(wd)

            # 리스트 뷰 상태에서 이미지 사이즈 저장
            list_size = like_page.save_list_image_size(wd)
            like_page.check_veiw_image_size(grid_size['height'], grid_size['width'], list_size['height'],
                                            list_size['width'])

            # 그리드 뷰로 복귀
            like_page.click_change_view_type_to_grid(wd)

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
            like_page.refresh_post_like_tab(wd)

            # 브랜드 좋아요 해제
            like_page.click_brand_tab(wd)
            like_page.click_to_unlike_brand(wd)
            like_page.refresh_brand_like_tab(wd)

            # 상품 좋아요 해제
            like_page.click_product_tab(wd)
            like_page.click_to_unlike_product(wd)
            like_page.refresh_product_like_tab(wd)

            # 상단 Like 개수 확인
            like_page.check_like_total_count(wd, "0")

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
            context_change.switch_context(wd, 'native')
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            context_change.switch_context(wd, 'native')
            send_test_result(self, test_result, '좋아요 존재하는 LIKE 화면 확인')
            return result_data
