import logging
import os.path
import sys
import traceback

import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time
from android_automation.page_action import welove_page, my_page, product_detail_page
import com_utils
from com_utils import values_control, slack_result_notifications, element_control, deeplink_control
from android_automation.page_action import navigation_bar, my_coupon_page, my_page
from com_utils.api_control import my_coupon_list
from com_utils.element_control import aalc, aal, aals
from com_utils.testrail_api import send_test_result
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from android_automation.page_action import my_setting_page


class My:
    def product_name(self, product_item_no):
        response = requests.get(f'https://cache.29cm.co.kr/item/detail/{product_item_no}/')
        if response.status_code == 200:
            product_data = response.json()
            product_name = product_data['item_name']
            print(f"api 호출로 받은 product_name : {product_name}")
            return product_name
        else:
            print('PDP 옵션 정보 API 불러오기 실패')

    # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
    def test_enter_settings_screen(self, wd, test_result='PASS', error_texts=[], img_src='',
                                   warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my_Android(wd)

            # 세팅 페이지 진입
            my_page.enter_setting_page(wd)

            # 세팅 페이지 내 알림 문구 확인
            my_setting_page.check_notification(wd)

            # Home 탭으로 바꾸기
            com_utils.deeplink_control.move_to_home_Android(wd)

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
            send_test_result(self, test_result, '설정화면 진입')
            return result_data

    def test_recently_viewed_content(self, wd, test_result='PASS', error_texts=[], img_src='',
                                     warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # 여성의류 베스트 1위 상품의 itemNo 확인
            product_item_no = com_utils.api_control.best_plp_women_clothes(1, 'NOW')['item_no']

            # 딥링크로 베스트 상품 PDP 진입
            com_utils.deeplink_control.move_to_pdp_Android(wd, product_item_no)

            # PDP 상품 이름 저장 -> 이미지 1개일 경우와 2개 이상일 경우, XPATH index 변경되어 아래와 같이 작성
            product_name = product_detail_page.save_product_name(wd)
            recent_product_name = product_detail_page.save_remove_prefix_product_name(product_name)

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my_Android(wd)

            # 최근 본 상품 영역 확인
            my_page.check_recent_title(wd, '상품', recent_product_name)

            # welove 페이지 이동
            com_utils.deeplink_control.move_to_welove(self, wd)

            # 첫번째 추천 게시물명 확인 및 선택
            post_title = welove_page.save_first_post_title(wd)
            welove_page.click_first_post(wd)

            # My 탭으로 이동
            com_utils.deeplink_control.move_to_my_Android(wd)

            # 최근 본 상품 영역 확인
            my_page.check_recent_title(wd, "컨텐츠", post_title)

            # 최근 본 상품 영역 확장
            my_page.expand_recent_contents(wd, post_title)

            # 최근 본 상품 히스토리 확인
            my_page.check_recent_history(wd, recent_product_name, post_title)

            # 최근 본 상품 영역 축소 후 Home 탭으로 이동
            my_page.close_recent_contents(wd)
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
            send_test_result(self, test_result, '최근 본 컨텐츠 확인')
            return result_data

    def test_track_delivery_without_orders(self, wd, test_result='PASS', error_texts=[], img_src='',
                                           warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[주문 건이 없을 경우, 주문 배송 조회 확인] CASE 시작")
            # 하단 네비게이터에 MY 메뉴 진입
            sleep(2)
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'MY').click()
            sleep(3)
            print("홈 > 마이페이지 화면 진입")
            try:
                wd.find_element(By.XPATH, "//*[contains(@text, '주문배송조회')]").click()
                sleep(3)
                order_delivery_tracking_title = wd.find_elements(By.XPATH, "//*[contains(@text, '주문배송조회')]")
                order_delivery_tracking_guide = wd.find_element(By.XPATH, "//*[contains(@text, '주문내역이 없습니다')]")
                print(f"order_delivery_tracking_title.text : {order_delivery_tracking_title[1].text}")
                print(f"order_delivery_tracking_guide.text : {order_delivery_tracking_guide.text}")
                if order_delivery_tracking_title[
                    1].text == '주문배송조회' and order_delivery_tracking_guide.text == '주문내역이 없습니다':
                    print("주문 건이 없을 경우, 주문 배송 조회 확인")
                else:
                    print("주문 건이 없을 경우, 주문 배송 조회 확인 실패")
                    test_result = 'WARN'
                    warning_texts.append("주문 건이 없을 경우, 주문 배송 조회 확인 실패")
                # 뒤로가기로 마이페이지 진입 확인
                wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()

            except NoSuchElementException:
                print("NoSuchElementException 주문 건이 없을 경우, 주문 배송 조회 확인 실패")
                sleep(1)
            wd.get('app29cm://home')
            print("[주문 건이 없을 경우, 주문 배송 조회 확인] CASE 종료")

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
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '주문 건이 없을 경우, 주문 배송 조회 없음 확인')
            return result_data

    def test_review_without_orders(self, wd, test_result='PASS', error_texts=[], img_src='',
                                   warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[주문 건이 없을 경우, 상품 리뷰 없음 확인] CASE 시작")
            # 하단 네비게이터에 MY 메뉴 진입
            sleep(5)
            navigation_bar.move_to_my(wd)
            sleep(3)
            print("홈 > 마이페이지 화면 진입")
            try:
                aalc(wd, 'c_상품 리뷰')
                sleep(5)
                print("상품 리뷰 선택")
                review_guide = aal(wd, 'c_아직 리뷰를 작성할 수 있는\n주문내역이 없습니다.').text
                print(f"review_guide : {review_guide}")
                aalc(wd, 'c_내 리뷰')
                my_review_guide = aal(wd, 'c_작성한 리뷰가 없습니다.').text
                print(f"my_review_guide : {my_review_guide}")
                if review_guide == '아직 리뷰를 작성할 수 있는\n주문내역이 없습니다.' and my_review_guide == '작성한 리뷰가 없습니다.':
                    print("주문 건이 없을 경우, 상품 리뷰 없음 확인")
                else:
                    print("주문 건이 없을 경우, 상품 리뷰 없음 확인 실패")
                    test_result = 'WARN'
                    warning_texts.append("주문 건이 없을 경우, 상품 리뷰 없음 확인 실패")
                # 뒤로가기로 마이페이지 진입 확인
                aalc(wd, 'com.the29cm.app29cm:id/imgBack')
            except Exception:
                print("Exception 주문 건이 없을 경우, 상품 리뷰 없음 확인 실패")
                sleep(1)
            wd.get('app29cm://home')
            print("[주문 건이 없을 경우, 상품 리뷰 없음 확인] CASE 종료")
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
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # warning texts list를 가독성 좋도록 줄바꿈
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '주문 건이 없을 경우, 상품 리뷰 없음 확인')
            return result_data

    def test_coupons_list(self, wd, test_result='PASS', error_texts=[], img_src='',
                          warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[보유하고 있는 쿠폰 목록 확인] CASE 시작")
            # 하단 네비게이터에 MY 메뉴 진입
            sleep(5)
            # navigation_bar.move_to_my(wd)
            wd.get('app29cm://mypage')
            sleep(3)
            print("홈 > 마이페이지 화면 진입")

            # 쿠폰 메뉴 선택
            my_page.click_coupon_menu(wd)

            # 장바구니 타입 선택
            my_coupon_page.click_coupon_type(wd)
            my_coupon_page.click_option_cart(wd)

            # API 호출 쿠폰 목록과 노출되는 쿠폰 목록 저장
            api_coupon_list = my_coupon_list(self.pconf['LOGIN_SUCCESS_ID'], self.pconf['LOGIN_SUCCESS_PW'], 'CART')
            coupon_list = my_coupon_page.save_my_coupon_list(wd, api_coupon_list)

            test_result = my_coupon_page.check_coupon_list(wd, warning_texts, api_coupon_list, coupon_list, '장바구니')

            # 상품 쿠폰 타입 선택
            my_coupon_page.click_cart_coupon_type(wd)
            my_coupon_page.click_option_product(wd)

            # API 호출 쿠폰 목록과 노출되는 쿠폰 목록 저장
            api_coupon_list = my_coupon_list(self.pconf['LOGIN_SUCCESS_ID'], self.pconf['LOGIN_SUCCESS_PW'],
                                             'PRODUCT')
            coupon_list = my_coupon_page.save_my_coupon_list(wd, api_coupon_list)

            test_result = my_coupon_page.check_coupon_list(wd, warning_texts, api_coupon_list, coupon_list, '상품')

            my_coupon_page.click_back_btn(wd)
            navigation_bar.move_to_home(wd)

            wd.get('app29cm://home')
            print("[보유하고 있는 쿠폰 목록 확인] CASE 종료")
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
            send_test_result(self, test_result, '보유하고 있는 쿠폰 목록 확인')
            return result_data
