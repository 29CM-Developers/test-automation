import logging
import os.path
import sys
import traceback

import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time
from com_utils import values_control, slack_result_notifications, element_control
from android_automation.page_action import navigation_bar
from com_utils.element_control import aalc, aal, aals


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
            print("[설정 화면 진입] CASE 시작")
            # 하단 네비게이터에 MY 메뉴 진입
            sleep(2)
            wd.get('app29cm://mypage')
            sleep(1)
            print("홈 > 마이페이지 화면 진입")
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgSetting').click()
            sleep(2)
            label_shopping = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtLabelShopping').text
            alarm_label = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtAlarmLabel').text
            if label_shopping == '쇼핑 알림' and alarm_label == '재입고 알림':
                print("설정 화면 진입 확인")
                pass
            else:
                print("설정 화면 진입 확인 실패")
                test_result = 'WARN'
                warning_texts.append("설정 화면 진입 확인 실패")
            print(f"타이틀 확인 : {label_shopping}, {alarm_label}")
            wd.get('app29cm://home')
            print("[설정 화면 진입] CASE 종료")

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
            return result_data

    def test_recently_viewed_content(self, wd, test_result='PASS', error_texts=[], img_src='',
                                     warning_texts=[]):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[최근 본 컨텐츠 확인] CASE 시작")
            # 하단 네비게이터에 MY 메뉴 진입
            sleep(2)
            wd.get('app29cm://mypage')
            sleep(1)
            print("홈 > 마이페이지 화면 진입")
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgSetting').click()

            # API 호출하여 itemNo 저장 > itemNo 사용하여 딥링크로 PDP 직행
            response = requests.get(
                'https://recommend-api.29cm.co.kr/api/v4/best/items?categoryList=268100100&periodSort=NOW&limit=100&offset=0')
            if response.status_code == 200:
                api_data = response.json()
                # content 배열에서 isSoldOut이 false인 첫 번째 아이템 찾기
                for item in api_data["data"]["content"]:
                    if not item["isSoldOut"]:
                        first_available_item_no = item["itemNo"]
                        print(f'first_available_item_no : {first_available_item_no}')
                        wd.get(f'app29cm://product/{first_available_item_no}')
                        print('딥링크 이동')
                        sleep(5)
                        response = requests.get(f'https://cache.29cm.co.kr/item/detail/{first_available_item_no}/')
                        if response.status_code == 200:
                            product_data = response.json()
                            best_product = product_data['item_name']
                            print(f"api 호출로 받은 product_name : {best_product}")
                        else:
                            print('PDP 옵션 정보 API 불러오기 실패')
                        # PDP 상품명과 API 호출된 상품명 동일한 지 확인
                        # 스페셜 오더 상품 확인
                        try:
                            wd.find_element(AppiumBy.XPATH, "//*[contains(@text, 'SPECIAL-ORDER')]")
                            element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=4]'
                            print('SPECIAL-ORDER 상품 발견')
                        except NoSuchElementException:
                            print('SPECIAL-ORDER 상품 미발견')
                            element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=5]'
                            pass

                        PDP_product_title = wd.find_element(AppiumBy.XPATH, element_xpath).text
                        print(f"PDP_product_title : {PDP_product_title} ")
                        if best_product in PDP_product_title:
                            print("pdp 진입 확인 - 베스트 상품")
                        else:
                            print("pdp 진입 확인 실패 - 베스트 상품")
                            test_result = 'WARN'
                            warning_texts.append("베스트 상품 PDP 정상 확인 실패")
                        print(f"베스트 상품명 : {best_product} , PDP 상품명 : {PDP_product_title}  ")
                        sleep(2)
                        wd.get('app29cm://mypage')
                        sleep(1)
                        print("홈 > 마이페이지 화면 진입")
                        txt_history_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtHistoryTitle').text
                        print(f"txt_history_title : {txt_history_title} ")
                        if txt_history_title in best_product:
                            print("recent 영역에 1번의 상품명 노출 확인")
                        else:
                            print("recent 영역에 1번의 상품명 노출 확인 실패")
                            test_result = 'WARN'
                            warning_texts.append("최근 본 상품 확인 실패")
                        print(f"my페이지 history 상품명 : {txt_history_title} , 베스트 상품명 : {best_product}  ")
                        break
            else:
                print("API 호출에 실패했습니다.")
            # 딥링크로 컨텐츠 진입
            # 5. 컨텐츠의 컨텐츠명 저장
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtHistoryTitle').click()
            sleep(1)
            print("최근 검색 펼침")

            # txt_1st_history_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtHistoryTitle').text
            # txt_2nd_history_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtHistoryTitle').text
            # print(f"txt_1st_history_title : {txt_1st_history_title} , txt_2nd_history_title : {txt_2nd_history_title}")
            # if txt_2nd_history_title in best_product and txt_1st_history_title in best_product:
            #     print("recent 영역에 4번, 1번 순으로 노출되는지 확인")
            # else:
            #     print("recent 영역에 4번, 1번 순으로 노출되는지 확인 실패")
            #     test_result = 'WARN'
            #     warning_texts.append("최근 본 컨텐츠 히스토리 확인 실패")

            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/pullUpLayout').click()
            sleep(1)
            print("최근 검색 닫기")
            wd.get('app29cm://home')
            print("[최근 본 컨텐츠 확인] CASE 종료")

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
                aalc(wd, '상품 리뷰')
                sleep(5)
                print("상품 리뷰 선택")
                review_guide = aal(wd, '아직 리뷰를 작성할 수 있는\n주문내역이 없습니다.').text
                print(f"review_guide : {review_guide}")
                aalc(wd, '내 리뷰')
                my_review_guide = aal(wd, '작성한 리뷰가 없습니다.').text
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
            return result_data
