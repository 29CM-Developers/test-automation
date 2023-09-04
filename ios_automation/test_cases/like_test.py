import os
import sys
import traceback
import com_utils.element_control

from time import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils import values_control


class Like:
    def test_no_like_item(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "LIKE"`]').click()

            # 화면 진입 시, 브랜드 추천 페이지 노출 여부 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'recommended_brand_page')
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()
                print('브랜드 추천 페이지 노출')
            except NoSuchElementException:
                pass

            # 상단 Like 개수 확인
            like_total_count = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_total_count').text
            if like_total_count == '0':
                print('총 LIKE 개수 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('총 LIKE 개수 확인 실패')
                print('총 LIKE 개수 확인 실패')

            # Product 탭 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '좋아요한 상품이 없습니다. 마음에 드는 상품의 하트를 눌러보세요.')
                print('PRODUCT 좋아요 없음 문구 노출 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('PRODUCT 좋아요 없음 문구 노출 확인 실패')
                print('PRODUCT 좋아요 없음 문구 노출 확인 실패')

            # Brand 탭 선택 및 확인
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_brand_tab').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '좋아요한 브랜드가 없어요.')
                print('BRAND 좋아요 없음 문구 노출 확인')
            except NoSuchElementException:
                print('BRAND 좋아요 없음 문구 노출 확인 실패')

            # POST 탭 선택 및 확인
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_post_tab').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '좋아요한 게시물이 없습니다. 다시 보고 싶은 게시물에 하트를 눌러보세요.')
                print('POST 좋아요 없음 문구 노출 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('POST 좋아요 없음 문구 노출 확인')
                print('POST 좋아요 없음 문구 노출 확인')

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
            wd.get('app29cm://home')

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def test_like_item(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # LIKE 탭 딥링크로 이동
            wd.get('app29cm://like')

            # 추천 리스트의 첫번째 상품명 저장 및 좋아요 선택
            recommended_product = wd.find_element(AppiumBy.XPATH,
                                                  '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="2"]')
            like_product_name = recommended_product.find_element(AppiumBy.XPATH,
                                                                 '//XCUIElementTypeStaticText[@index="1"]').text
            print(like_product_name)
            recommended_product.find_element(AppiumBy.IOS_CLASS_CHAIN,
                                             '**/XCUIElementTypeButton[`label == "icHeartLine"`]').click()

            # PRODUCT 탭 새로고침
            product_list = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_product_list')
            com_utils.element_control.element_scroll_control(wd, product_list, 'U', 30)

            liked_product = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_product_item')
            liked_product_name = liked_product.find_element(AppiumBy.XPATH,
                                                            '//XCUIElementTypeStaticText[@index="1"]').text

            if like_product_name == liked_product_name:
                print('좋아요 상품 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('좋아요 상품 노출 확인 실패')
                print(f'좋아요 상품 노출 확인 실패: {like_product_name} / {liked_product_name}')

            # 좋아요 상품의 [장바구니 담기] 버튼 선택
            liked_product.find_element(AppiumBy.IOS_CLASS_CHAIN,
                                       '**/XCUIElementTypeButton[`label == "장바구니 담기"`]').click()

            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니 담기')
                print('좋아요 상품 PDP 진입 확인 - 바텀시트')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('좋아요 상품 PDP 진입 확인 실패')
                print('좋아요 상품 PDP 진입 확인 실패 - 바텀시트')

            wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView').click()

            # PDP 상품 이름 저장
            pdp_web = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView')
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'Select a slide to show')
                pdp_name = pdp_web.find_element(AppiumBy.XPATH,
                                                '//XCUIElementTypeOther[@index="5"]/XCUIElementTypeStaticText').get_attribute(
                    'name')
            except NoSuchElementException:
                pdp_name = pdp_web.find_element(AppiumBy.XPATH,
                                                '//XCUIElementTypeOther[@index="4"]/XCUIElementTypeStaticText').get_attribute(
                    'name')

            # 선택한 상품의 PDP에서 상품 이름 비교
            if like_product_name in pdp_name:
                print('좋아요 상품 PDP 진입 확인 - 상품명')
            else:
                test_result = 'WARN'
                warning_texts.append('PDP 진입 확인 실패')
                print(f'좋아요 상품 PDP 진입 확인 실패 - 상품명 : {like_product_name} / {pdp_name}')

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_brand_tab').click()

            # 추천 리스트의 첫번째 브랜드명 저장 및 좋아요 선택
            recommended_brand = wd.find_element(AppiumBy.XPATH,
                                                '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="3"]')
            like_brand_name = recommended_brand.find_element(AppiumBy.XPATH,
                                                             '//XCUIElementTypeStaticText[@index="1"]').text
            print(like_brand_name)
            recommended_brand.find_element(AppiumBy.IOS_CLASS_CHAIN,
                                           '**/XCUIElementTypeButton[`label == "ic heart line"`]').click()

            # BRAND 탭 새로고침
            brand_list = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_brand_list')
            com_utils.element_control.element_scroll_control(wd, brand_list, 'U', 30)

            liked_brand = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_brand_item')
            liked_brand_name = liked_brand.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@index="1"]').text
            if like_brand_name == liked_brand_name:
                print('좋아요 브랜드 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('좋아요 브랜드 노출 확인 실패')
                print(f'좋아요 브랜드 노출 확인 실패: {like_brand_name} / {liked_brand_name}')

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_post_tab').click()

            # 추천 게시물 페이지로 이동
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "인기 게시물 보기"`]').click()

            # 첫번째 추천 게시물명 확인 및 선택
            recommended_post = wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                                               '**/XCUIElementTypeCell[`name == "recommended_post"`][1]')
            like_post_name = recommended_post.find_element(AppiumBy.XPATH, 'XCUIElementTypeStaticText[2]').text
            print(like_post_name)
            recommended_post.click()

            # post 내 좋아요 버튼 선택
            post_view = wd.find_elements(AppiumBy.XPATH,
                                         '//XCUIElementTypeWebView/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther')
            post_view_len = len(post_view) - 1
            wd.find_element(AppiumBy.XPATH, f'//XCUIElementTypeOther[{post_view_len}]/XCUIElementTypeButton[1]').click()

            # LIKE 탭으로 복귀
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()
            except NoSuchElementException:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackWhite').click()

            # POST 탭 새로고침
            post_list = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_post_list')
            com_utils.element_control.element_scroll_control(wd, post_list, 'U', 30)

            # 좋아요 한 게시물명 확인
            liked_post = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_post_item')
            liked_post_name = liked_post.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text

            if like_post_name == liked_post_name:
                print('좋아요 게시물 노출 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('좋아요 게시물 노출 확인 실패')
                print(f'좋아요 게시물 노출 확인 실패 : {like_post_name} / {liked_post_name}')

            # 상단 Like 개수 확인
            like_total_count = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_total_count').text
            if like_total_count == '3':
                print('총 LIKE 개수 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('총 LIKE 개수 확인 실패')
                print('총 LIKE 개수 확인 실패')

            liked_post.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton').click()

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_brand_tab').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'ic heart line').click()

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_product_tab').click()
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icHeartLine').click()

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
            wd.get('app29cm://home')

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data
