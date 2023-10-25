import os
import sys
import traceback
import com_utils.deeplink_control
import com_utils.api_control

from time import time
from com_utils import values_control
from ios_automation.page_action import my_page, my_setting_page, navigation_bar, product_detail_page, welove_page, \
    delivery_order_page, product_review_page


class My:
    def test_enter_settings_screen(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            # 세팅 페이지 진입
            my_page.enter_setting_page(wd)

            # 세팅 페이지 내 알림 문구 확인
            my_setting_page.check_notification(wd, warning_texts)

            # Home 탭으로 보구기
            my_setting_page.click_back_btn(wd)
            navigation_bar.move_to_home(wd)

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
            com_utils.deeplink_control.move_to_home(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def test_recently_viewed_content(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # 여성의류 베스트 1위 상품의 itemNo 확인
            product_item_no = com_utils.api_control.best_plp_women_clothes(0)['item_no']

            # 딥링크로 베스트 상품 PDP 진입
            com_utils.deeplink_control.move_to_pdp(wd, product_item_no)

            # PDP 상품 이름 저장 -> 이미지 1개일 경우와 2개 이상일 경우, XPATH index 변경되어 아래와 같이 작성
            product_name = product_detail_page.save_product_name(wd)

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            # 최근 본 상품 영역 확인
            test_result = my_page.check_recent_title(wd, warning_texts, '상품', product_name)

            # welove 페이지 이동
            com_utils.deeplink_control.move_to_welove(self, wd)

            # 첫번째 추천 게시물명 확인 및 선택
            post_title = welove_page.save_first_contents_title(wd)
            welove_page.click_first_contents(wd)

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            # 최근 본 상품 영역 확인
            test_result = my_page.check_recent_title(wd, warning_texts, "컨텐츠", post_title)

            # 최근 본 상품 영역 확장
            my_page.expand_recent_contents(wd)

            # 최근 본 상품 히스토리 확인
            test_result = my_page.check_recent_history(wd, warning_texts, product_name, post_title)

            # 최근 본 상품 영역 축소 후 Home 탭으로 이동
            my_page.close_recent_contents(wd)
            navigation_bar.move_to_home(wd)

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
            com_utils.deeplink_control.move_to_home(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def test_track_delivery_without_orders(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            my_page.click_delivery_order_menu(wd)

            test_result = delivery_order_page.check_no_delivery_order(wd, warning_texts)

            delivery_order_page.click_back_btn(wd)

            navigation_bar.move_to_home(wd)

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
            com_utils.deeplink_control.move_to_home(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def test_review_without_orders(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my(self, wd)

            # 싱픔 리뷰 페이지 진입
            my_page.click_review_menu(wd)

            # 작성 가능한 리뷰 없음 확인
            test_result = product_review_page.check_no_reviews_available(wd, warning_texts)

            # 내 리뷰 탭 진입하여 작성한 리뷰 없음 확인
            product_review_page.click_my_review_tab(wd)
            test_result = product_review_page.check_no_written_reviews(wd, warning_texts)

            # Home 탭으로 복귀
            # product_review_page.click_back_btn(wd)
            # navigation_bar.move_to_home(wd)
            com_utils.deeplink_control.move_to_home(self, wd)

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
            com_utils.deeplink_control.move_to_home(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data
