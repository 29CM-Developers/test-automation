import logging
import os.path
import subprocess
import sys
import traceback
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec, wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from com_utils import values_control
from time import sleep, time


class NotLogin:

    logging.basicConfig(level=logging.INFO)
    # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
    def test_not_login_user_impossible(self, wd, test_result='PASS', error_texts=[], img_src=''):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = sys._getframe().f_code.co_name
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            logging.info("[사용 불가 기능 사용]CASE 시작")
            sleep(2)
            # 홈 > 우상단 알림 아이콘 선택
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgInboxNotification').click()
            logging.info("홈 > 우상단 알림 아이콘 선택")
            # 로그인 화면 진입 확인
            login_page_title = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.widget.TextView[1]')
            if login_page_title.text == '로그인':
                logging.info("로그인 진입 확인 : 로그인 문구 확인")
            else:
                logging.info("로그인 진입 확인 : 로그인 문구 실패")
            logging.info("가이드 문구 : %s " % login_page_title.text)

            # 뒤로가기로 홈화면 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            logging.info("뒤로가기 선택")
            sleep(2)
            home_title = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtShowAll')
            if home_title.text == '모아보기':
                logging.info("홈 진입 확인 : 모아보기 문구 확인")
            else:
                logging.info("홈 진입 확인 : 모아보기 문구 확인 실패")
            logging.info("발견 문구 : %s " % home_title.text)

            #full test 확장 시나리오
            # 홈 > 우상단 장바구니 아이콘 선택
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgCart').click()
            logging.info("홈 > 우상단 장바구니 아이콘 선택")
            # 로그인 화면 진입 확인
            login_page_title = wd.find_element(By.XPATH, '//*[@resource-id="__next"]/android.widget.TextView[1]')
            if login_page_title.text == '로그인':
                logging.info("로그인 진입 확인 : 로그인 문구 확인")
            else:
                logging.info("로그인 진입 확인 : 로그인 문구 실패")
            logging.info("가이드 문구 : %s " % login_page_title.text)

            # 뒤로가기로 홈화면 진입 확인
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            logging.info("뒤로가기 선택")

            if home_title.text == '모아보기':
                logging.info("홈 진입 확인 : 모아보기 문구 확인")
            else:
                logging.info("홈 진입 확인 : 모아보기 문구 확인 실패")
            logging.info("발견 문구 : %s " % home_title.text)

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

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data

    def test_not_login_user_possible(self, wd, test_result='PASS', error_texts=[], img_src=''):
        # 현재 함수명 저장 - slack noti에 사용
        test_name = sys._getframe().f_code.co_name
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            logging.info("[사용 가능 기능 사용]CASE 시작")
            sleep(5)


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

        finally:
            # 함수 완료 시 시간체크하여 시작시 체크한 시간과의 차이를 테스트 소요시간으로 반환
            run_time = f"{time() - start_time:.2f}"
            # 값 재사용 용이성을 위해 dict로 반환한다
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time}
            return result_data