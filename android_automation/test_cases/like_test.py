import os.path
import sys
import traceback
import logging
import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
import com_utils
from android_automation.page_action import like_page, navigation_bar, product_detail_page, context_change
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from android_automation.page_action.context_change import change_webview_contexts, change_native_contexts
from android_automation.page_action.home_page import check_app_evaluation_popup
from com_utils import values_control, cookies_control, deeplink_control
from time import sleep, time
from com_utils.element_control import aal, aalk, aalc, scroll_control, \
    swipe_control, swipe_control, element_scroll_control
from com_utils.testrail_api import send_test_result


class Like:
    def set_like_zero(self, wd):

        wd.get(self.conf['deeplink']['like'])

        # 화면 진입 시, 브랜드 추천 페이지 노출 여부 확인
        # 관심 브랜드 선택 화면 발생
        brands_of_interest = wd.find_elements(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutMyLikeAndOrderBrand')
        print(brands_of_interest)
        if len(brands_of_interest) == 0:
            print('관심브랜드 화면 미노출')
            pass
        else:
            print('관심브랜드 화면 노출')
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/iconClose').click()

        print(
            f"self.pconf['id_29cm']: {self.pconf['id_29cm']}, self.pconf['password_29cm']:{self.pconf['password_29cm']}")
        cookies = cookies_control.cookie_29cm(self.pconf['id_29cm'], self.pconf['password_29cm'])

        like_response = requests.get('https://front-api.29cm.co.kr/api/v4/heart/my-heart/count/', cookies=cookies)
        like = like_response.json()
        product_count = int(like['data']['product_count'])
        brand_count = int(like['data']['brand_count'])
        post_count = int(like['data']['post_count'])

        if product_count != 0:
            print(f'좋아요 상품 수 : {product_count}')
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtProduct').click()
            # 좋아요 해제 후 새로고침
            # 상품 탭 선택
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutProduct').click()
            product_like_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/likeRecyclerView')
            product_like_layer.find_element(AppiumBy.XPATH,
                                            '//android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.ImageView[2]').click()
            txtProductCount = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtProductCount').text
            print(txtProductCount)
            if txtProductCount == '(0)':
                print('Product Count 감소 확인')
            else:
                print('Product Count 감소 확인 실패')
                print(f'Product Count : {txtHeartCount} ')

        if brand_count != 0:
            print(f'좋아요 브랜드 수 : {brand_count}')
            # 브랜드 탭 선택
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutBrand').click()
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutHeart').click()
            txtBrandCount = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtBrandCount').text
            if txtBrandCount == '(0)':
                print('Brand Count 감소 확인')
            else:
                print('Brand Count 감소 확인 실패')
                print(f'Brand Count : {txtBrandCount} ')

    def test_no_like_item(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # 딥링크로 LIKE 탭 진입
            com_utils.deeplink_control.move_to_like_Android(wd)

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

            # # POST 탭 선택 및 확인
            # like_page.click_post_tab(wd)
            # like_page.check_no_post_like(wd)

            navigation_bar.move_to_home(wd)
            print(f'[{test_name}] 테스트 종료')

            # print("[좋아요 존재하지 않는 LIKE 화면 확인]CASE 시작")
            # wd.get('app29cm://like')
            # # like 탭 선택
            # Like.set_like_zero(self, self.wd)
            # sleep(2)
            # # 관심 브랜드 선택 화면 발생
            # brands_of_interest = wd.find_elements(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutMyLikeAndOrderBrand')
            # print(brands_of_interest)
            # if len(brands_of_interest) == 0:
            #     print('관심브랜드 화면 노출 안됨')
            #     pass
            # else:
            #     print('관심브랜드 화면 노출')
            #     wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/iconClose').click()
            #
            # txtHeartCount = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtHeartCount').text
            # if txtHeartCount == '0':
            #     print('상단 LIKE 개수 0개 확인')
            # else:
            #     test_result = 'WARN'
            #     warning_texts.append('상단 LIKE 개수 확인 실패')
            #     print('WARN : 상단 LIKE 개수 확인 실패')
            # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutProduct').click()
            # txtInfo = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtInfo').text
            # print(f"text info : {txtInfo}")
            # if txtInfo in '좋아요한 상품이 없습니다.\n마음에 드는 상품에 하트를 눌러보세요.':
            #     print('PRODUCT 좋아요 없음 문구 노출 확인')
            # else:
            #     test_result = 'WARN'
            #     warning_texts.append('PRODUCT 좋아요 없음 문구 노출 확인 실패')
            #     print('WARN : PRODUCT 좋아요 없음 문구 노출 확인 실패')
            # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutBrand').click()
            #
            # # 관심 브랜드 선택 화면 발생
            # brands_of_interest = aal(wd, 'com.the29cm.app29cm:id/layoutMyLikeAndOrderBrand')
            # if brands_of_interest == None:
            #     print('관심브랜드 화면 노출 안됨')
            #     pass
            # else:
            #     print('관심브랜드 화면 노출')
            #     wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/iconClose').click()
            #
            # txtBrandCount = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtBrandCount').text
            # print(f"text info : {txtBrandCount}")
            # txtInfo = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtInfo').text
            # if txtInfo in '좋아요한 브랜드가 없습니다.\n마음에 드는 브랜드에 하트를 눌러보세요.':
            #     print('BRAND 좋아요 없음 문구 노출 확인')
            # else:
            #     test_result = 'WARN'
            #     warning_texts.append('BRAND 좋아요 없음 문구 노출 확인 실패')
            #     print('WARN : BRAND 좋아요 없음 문구 노출 확인 실패')
            # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutPost').click()
            # txtInfo = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtInfo').text
            # print(f"text info : {txtInfo}")
            # if txtInfo in '좋아요한 게시물이 없습니다.\n다시 보고 싶은 게시물에 하트를 눌러보세요.':
            #     print('POST 좋아요 없음 문구 노출 확인')
            # else:
            #     test_result = 'WARN'
            #     warning_texts.append('POST 좋아요 없음 문구 노출 확인 실패')
            #     print('WARN : POST 좋아요 없음 문구 노출 확인 실패')
            # # home 탭 선택
            # wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()
            # sleep(2)
            # print("[좋아요 존재하지 않는 LIKE 화면 확인]CASE 종료")

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
            send_test_result(self, test_result, '좋아요 존재하지 않는 LIKE 화면 확인')
            return result_data
    def test_like_item(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        # slack noti에 사용되는 test_result, error_texts, ims_src를 매개변수로 받는다
        # 현재 함수명 저장 - slack noti에 사용
        test_name = self.dconf[sys._getframe().f_code.co_name]
        # slack noti에 사용하는 테스트 소요시간을 위해 함수 시작 시 시간 체크
        start_time = time()
        try:
            print(f'[{test_name}] 테스트 시작')

            # 딥링크로 LIKE 탭 진입
            com_utils.deeplink_control.move_to_like_Android(wd)
            like_page.close_brand_recommended_page(wd)

            # 추천 리스트의 첫번째 상품명 저장 및 좋아요 선택
            like_product_name = like_page.save_like_product_name_in_like(wd)
            like_page.click_product_like_btn(wd)

            # 앱평가 팝업 확인
            check_app_evaluation_popup(wd)

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
            like_page.check_open_to_purchase_modal(wd, pdp_product_name)
            like_page.close_purchase_modal(wd)

            # # PDP 상품 이름 저장
            # pdp_product_name = product_detail_page.save_product_name(wd)
            #
            # # 좋아요 한 상품명과 PDP의 상품명 비교
            # product_detail_page.check_product_name(pdp_product_name, like_product_name)
            #
            # # pdp에서 뒤로가기 선택하여 like 탭으로 복귀
            # product_detail_page.click_pdp_back_btn(wd)

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
            change_webview_contexts(wd)
            # context_change.switch_context(wd, 'webview')

            # 브랜드 PLP에서 브랜드명 비교 확인
            like_page.check_brand_page_name(wd, like_brand_name)

            # native 전환
            # context_change.switch_context(wd, 'native')
            change_native_contexts(wd)

            # 브랜드 PLP에서 좋아요 페이지로 복귀
            like_page.click_brand_back_btn(wd)

            # 좋아요 브랜드의 첫번쨰 상품 선택하여 해당 상품 PDP 진입
            liked_brand_product_name = like_page.save_liked_brand_product_name(wd)
            like_page.click_liked_brand_product_name(wd)
            pdp_product_name = product_detail_page.save_product_name(wd)
            product_detail_page.check_product_name(pdp_product_name, liked_brand_product_name)

            # Like 탭으로 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # # 포스트 탭 선택
            # like_page.click_post_tab(wd)
            #
            # # 추천 게시물 페이지로 이동
            # like_page.move_to_welove_page(wd)
            #
            # # 첫번째 추천 게시물명 확인 및 선택
            # like_post_name = welove_page.save_first_post_title(wd)
            # welove_page.click_first_post(wd)
            #
            # # webview 전환
            # context_change.switch_context(wd, 'webview')
            #
            # # post 내 좋아요 버튼 선택
            # welove_page.click_post_like_btn(wd)
            #
            # # native 전환
            # context_change.switch_context(wd, 'native')
            #
            # # LIKE 탭으로 복귀
            # welove_page.click_post_to_welove_back_btn(wd)
            # welove_page.click_welove_back_btn(wd)
            #
            # # POST 탭 새로고침
            # like_page.refresh_post_like_tab(wd)
            #
            # # 좋아요 한 게시물명 확인
            # like_page.check_post_like(wd, like_post_name)
            #
            # # 상단 Like 개수 확인
            # like_page.check_like_total_count(wd, "3")
            #
            # # 포스트 좋아요 해제
            # like_page.click_to_unlike_post(wd)
            # like_page.refresh_post_like_tab(wd)

            # 브랜드 좋아요 해제
            like_page.click_brand_tab(wd)
            like_page.click_to_unlike_brand(wd)
            # like_page.refresh_brand_like_tab(wd)

            # 상품 좋아요 해제
            like_page.click_product_tab(wd)
            like_page.click_to_unlike_product(wd)
            # like_page.refresh_product_like_tab(wd)

            # 상단 Like 개수 확인
            like_page.check_like_total_count(wd, "0")

            # Home 탭으로 복귀
            navigation_bar.move_to_home(wd)
            print(f'[{test_name}] 테스트 종료')

            # print("[좋아요 존재하는 LIKE 화면 확인]CASE 시작")
            # wd.get('app29cm://like')
            # # like 탭 선택
            # sleep(1)
            # close_bottom_sheet(wd)
            # like_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/likeRecyclerView')
            # productItem = like_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[2]/android.widget.TextView[@resource-id="com.the29cm.app29cm:id/contentsDescription"]').text
            # print(f"productItem : {productItem}")
            # like_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[2]/android.widget.ImageView[@resource-id="com.the29cm.app29cm:id/contentsHeart"]').click()
            #
            # # 앱평가 발생 시 팝업 제거
            # app_evaluation = wd.find_elements(By.XPATH, "//*[contains(@text, '29CM 앱을 어떻게 생각하시나요?')]")
            # print(app_evaluation)
            # if len(app_evaluation) == 0:
            #     pass
            # else:
            #     wd.find_element(By.XPATH, "//*[contains(@text, '좋아요')]").click()
            #     sleep(1)
            #     wd.find_element(By.XPATH, "//*[contains(@text, '나중에 하기')]").click()
            #
            # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutShowProduct').click()
            # like_productItem = like_layer.find_element(AppiumBy.ID,'com.the29cm.app29cm:id/txtBody').text
            # print(f"like_productItem : {like_productItem}")
            # if like_productItem in productItem:
            #     print('좋아요 상품 노출 확인')
            # else:
            #     test_result = 'WARN'
            #     warning_texts.append('좋아요 상품 노출 확인 실패')
            #     print('WARN : 좋아요 상품 노출 확인 실패')
            # print(f"productItem : {productItem}, like_productItem : {like_productItem}")
            # # 장바구니 버튼 선택하여 PDP 진입 확인 (바텀시트 확인, 상품명 확인)
            # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtCart').click()
            # item_name = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtItemName').text
            # if item_name in like_productItem:
            #     print('좋아요 상품 PDP 진입 확인')
            # else:
            #     test_result = 'WARN'
            #     warning_texts.append('좋아요 상품 PDP 진입 확인 실패')
            #     print('WARN : 좋아요 상품 PDP 진입 확인 실패')
            # wd.find_element(AppiumBy.ID, 'android:id/content').click()
            #
            # # 그리드 뷰 상태에서 이미지 사이즈 저장
            # # image_size_layer = aal(wd,'com.the29cm.app29cm:id/likeRecyclerView')
            # sleep(1)
            # grid_size = aal(wd, '//android.widget.ImageView[@resource-id="com.the29cm.app29cm:id/imageThumbnail"]').size
            # print(f'grid_size : {grid_size["height"]} / {grid_size["width"]}')
            # aalc(wd, 'com.the29cm.app29cm:id/imageGrid')
            # sleep(1)
            # list_size = aal(wd, '//android.widget.ImageView[@resource-id="com.the29cm.app29cm:id/imageThumbnail"]').size
            # print(f'grid_size : {list_size["height"]} / {list_size["width"]}')
            # if grid_size['height'] != list_size['height'] and grid_size['width'] != list_size['width']:
            #     test_result = 'PASS'
            #     print("좋아요 상품 탭의 뷰 정렬 변경 확인")
            # else:
            #     test_result = 'WARN'
            #     warning_texts.append('좋아요 상품 탭의 뷰 정렬 변경 확인 실패')
            #     print("좋아요 상품 탭의 뷰 정렬 변경 확인 실패")
            # aalc(wd, 'com.the29cm.app29cm:id/imageGrid')
            #
            # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutBrand').click()
            # like_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/likeRecyclerView')
            # BrandName = like_layer.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtBrandName').text
            # print(f"BrandName : {BrandName}")
            # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutHeart').click()
            # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutShowBrand').click()
            # like_BrandName = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtBrandName')
            # print(f"like_BrandName : {like_BrandName.text}")
            # if BrandName in like_BrandName.text:
            #     print('좋아요 브랜드 노출 확인')
            # else:
            #     test_result = 'WARN'
            #     warning_texts.append('좋아요 브랜드 노출 확인 실패')
            #     print('WARN : 좋아요 브랜드 노출 확인 실패')
            # like_BrandName.click()
            # sleep(4)
            # change_webview_contexts(wd)
            # original_string = BrandName
            # uppercase_string = original_string.upper()
            # brand_name = aal(wd, '//*[@id="__next"]/section[1]/div[1]/div[1]/h3')
            # print(f'brand_name : {brand_name.text}')
            # if uppercase_string in brand_name.text:
            #     print('좋아요 브랜드 노출 확인')
            # else:
            #     test_result = 'WARN'
            #     warning_texts.append('좋아요 브랜드 노출 확인 실패')
            #     print('WARN : 좋아요 브랜드 노출 확인 실패')
            #
            # sleep(1)
            # change_native_contexts(wd)
            # aalc(wd, 'com.the29cm.app29cm:id/imgBack')
            # print("뒤로가기 선택")
            # sleep(2)
            #
            # # post 버그 확인 후 제거 예정
            # # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutPost').click()
            # # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtGuide').click()
            # # PostTitle = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtPostTitle').text
            # # print(f"PostTitle : {PostTitle}")
            # # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtPostTitle').click()
            # # sleep(3)
            # # rootView = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/rootView')
            # # like_button = rootView.find_element(AppiumBy.XPATH, '//android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[3]/android.view.View/android.widget.Button')
            # # like_button.click()
            # # sleep(1)
            # # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            # # sleep(1)
            # # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/imgBack').click()
            # # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutBrand').click()
            # # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutPost').click()
            # # like_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/likeRecyclerView')
            # # like_post_title = like_layer.find_element(AppiumBy.XPATH, f"//*[contains(@text, '{PostTitle}')]").text
            # # print(f"like_post_title : {like_post_title}")
            # # like 갯수 3개 확인
            # txtHeartCount = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtHeartCount').text
            # if txtHeartCount == '2':
            #     print(f'상단 LIKE 개수 {txtHeartCount}개 확인')
            #     # 상품 탭 선택
            #     wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutProduct').click()
            #     product_like_layer = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/likeRecyclerView')
            #     product_like_layer.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.ImageView[2]').click()
            #     txtProductCount = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtProductCount').text
            #     print(txtProductCount)
            #     if txtProductCount == '(0)' :
            #         print('Product Count 감소 확인')
            #     else :
            #         test_result = 'WARN'
            #         warning_texts.append('Product Count 감소 확인 실패')
            #         print(f'Product Count : {txtHeartCount} ')
            #     # 브랜드 탭 선택
            #     wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutBrand').click()
            #     wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutHeart').click()
            #     txtBrandCount = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtBrandCount').text
            #     if txtBrandCount == '(0)':
            #         print('Brand Count 감소 확인')
            #     else:
            #         test_result = 'WARN'
            #         warning_texts.append('Brand Count 감소 확인 실패')
            #         print(f'Brand Count : {txtBrandCount} ')
            #     # 포스트 탭 선택 -> 현재 기존 버그 이슈 있어 처리 후 주석 제거 예정
            #     # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutPost').click()
            #     # wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutHeart').click()
            #     # txtPostCount = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtPostCount').text
            #     # if txtPostCount == '(0)':
            #     #     print('Post Count 감소 확인')
            #     # else:
            #     #     test_result = 'WARN'
            #     #     warning_texts.append('Post Count 감소 확인 실패')
            #     #     print(f'Post Count : {txtPostCount} ')
            # else:
            #     test_result = 'WARN'
            #     warning_texts.append('상단 LIKE 개수 확인 실패')
            #     print(f'WARN : 상단 LIKE 개수 {txtHeartCount} 개로 3개 확인 실패')
            # # like 해제
            #
            # # home 탭 선택
            # wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'HOME').click()
            # sleep(2)
            # print("[좋아요 존재하는 LIKE 화면 확인]CASE 종료")

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
            send_test_result(self, test_result, '좋아요 존재하는 LIKE 화면 확인')
            return result_data