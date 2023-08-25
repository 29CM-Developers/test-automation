import os.path
import sys
import traceback
import logging
import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from com_utils import values_control, element_control
from time import sleep, time
logger = logging.getLogger(name='Log')
logger.setLevel(logging.INFO)  ## 경고 수준 설정
formatter = logging.Formatter('|%(name)s||%(lineno)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler()  ## 스트림 핸들러 생성
stream_handler.setFormatter(formatter)  ## 텍스트 포맷 설정
logger.addHandler(stream_handler)  ## 핸들러 등록
class Like:

    def test_no_like_item(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[좋아요 존재하지 않는 LIKE 화면 확인]CASE 시작")
            sleep(2)
            # like 탭 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'LIKE').click()
            txtHeartCount = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtHeartCount').text
            if txtHeartCount == '0':
                print('상단 LIKE 개수 0개 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('상단 LIKE 개수 확인 실패')
                print('WARN : 상단 LIKE 개수 확인 실패')
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutProduct').click()
            txtInfo = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtInfo').text
            print(f"text info : {txtInfo}")
            if txtInfo in '좋아요한 상품이 없습니다.\n마음에 드는 상품에 하트를 눌러보세요.':
                print('PRODUCT 좋아요 없음 문구 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('PRODUCT 좋아요 없음 문구 노출 확인 실패')
                print('WARN : PRODUCT 좋아요 없음 문구 노출 확인 실패')
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutBrand').click()
            txtInfo = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtInfo').text
            print(f"text info : {txtInfo}")
            if txtInfo in '좋아요한 브랜드가 없습니다.\n마음에 드는 브랜드에 하트를 눌러보세요.':
                print('BRAND 좋아요 없음 문구 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('BRAND 좋아요 없음 문구 노출 확인 실패')
                print('WARN : BRAND 좋아요 없음 문구 노출 확인 실패')
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutPost').click()
            txtInfo = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtInfo').text
            print(f"text info : {txtInfo}")
            if txtInfo in '좋아요한 게시물이 없습니다.\n다시 보고 싶은 게시물에 하트를 눌러보세요.':
                print('POST 좋아요 없음 문구 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('POST 좋아요 없음 문구 노출 확인 실패')
                print('WARN : POST 좋아요 없음 문구 노출 확인 실패')
            # home 탭 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()
            sleep(2)
            print("[좋아요 존재하지 않는 LIKE 화면 확인]CASE 종료")

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
    def test_like_item(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print("[좋아요 존재하는 LIKE 화면 확인]CASE 시작")
            sleep(2)
            # like 탭 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'LIKE').click()
            like_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/likeRecyclerView')
            productItem = like_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[2]/android.widget.TextView[@resource-id="com.the29cm.app29cm:id/contentsDescription"]').text
            print(f"productItem : {productItem}")
            like_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[2]/android.widget.ImageView[@resource-id="com.the29cm.app29cm:id/contentsHeart"]').click()
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutShowProduct').click()
            like_productItem = like_layer.find_element(AppiumBy.ID,'com.the29cm.app29cm:id/txtBody').text
            print(f"productItem : {like_productItem}")
            if productItem in like_productItem:
                print('좋아요 상품 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('좋아요 상품 노출 확인 실패')
                print('WARN : 좋아요 상품 노출 확인 실패')

            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutBrand').click()
            like_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/likeRecyclerView')
            BrandName = like_layer.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtBrandName').text
            print(f"BrandName : {BrandName}")
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutHeart').click()
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutShowBrand').click()
            like_BrandName = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtBrandName').text
            print(f"like_BrandName : {like_BrandName}")
            if BrandName in like_BrandName:
                print('좋아요 브랜드 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('좋아요 브랜드 노출 확인 실패')
                print('WARN : 좋아요 브랜드 노출 확인 실패')
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutPost').click()
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtGuide').click()
            PostTitle = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtPostTitle').text
            print(f"PostTitle : {PostTitle}")
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtPostTitle').click()
            sleep(1)
            rootView = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/rootView')
            like_button = rootView.find_element(AppiumBy.XPATH, '//android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[3]/android.view.View/android.widget.Button')
            like_button.click()

            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            sleep(1)
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()

            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutBrand').click()
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutPost').click()
            like_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/likeRecyclerView')
            like_post_title = like_layer.find_element(AppiumBy.XPATH, f"//*[contains(@text, '{PostTitle}')]").text
            print(f"like_post_title : {like_post_title}")

            # home 탭 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()
            sleep(2)
            print("[좋아요 존재하는 LIKE 화면 확인]CASE 종료")

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