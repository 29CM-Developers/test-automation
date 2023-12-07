import os
import sys
import traceback
import requests
import com_utils.element_control

from com_utils import values_control
from time import time, sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.api_control import search_total_popular_brand_name
from com_utils.testrail_api import send_test_result
from ios_automation.page_action import navigation_bar, bottom_sheet, home_page, like_page, my_page, product_detail_page, \
    context_change, search_page


class Home:
    def check_feed_title(self):

        first_feed_title = ''
        first_relate_item_feed_title = ''
        second_feed_title = ''

        # 우먼 탭 컨텐츠 API 호출
        response = requests.get(
            'https://content-api.29cm.co.kr/api/v5/feeds?experiment=&feed_sort=WOMEN&home_type=APP_HOME&limit=20&offset=0')
        if response.status_code == 200:
            contents_api_data = response.json()
            feed_item_contents = contents_api_data['data']['results']

            for i in range(0, 10):
                feed_contents_type = feed_item_contents[i]['feedType']
                related_feed_item = feed_item_contents[i]['relatedFeedItemList']

                # feedType이 contents인 첫번째, 두번째 컨텐츠의 타이틀 저장
                if feed_contents_type == 'contents':
                    if not first_feed_title:
                        first_feed_title = feed_item_contents[i]['feedTitle']
                    elif not second_feed_title:
                        second_feed_title = feed_item_contents[i]['feedTitle']

                # 연결된 상품이 있는 첫번째 컨텐츠의 타이틀 저장
                if related_feed_item and not first_relate_item_feed_title:
                    first_relate_item_feed_title = feed_item_contents[i]['feedTitle']

                if first_feed_title and first_relate_item_feed_title and second_feed_title:
                    break

            print(
                f'첫번째 피드 : {first_feed_title}\n연결된 상품이 있는 첫번째 피드 : {first_relate_item_feed_title}\n두번째 피드 : {second_feed_title}')
        else:
            print('피드 컨텐츠 API 불러오기 실패')

        return first_feed_title, first_relate_item_feed_title, second_feed_title

    def test_home_banner(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        print(f'[{test_name}] 테스트 시작')

        try:
            bottom_sheet.find_icon_and_close_bottom_sheet(wd)

            # 라이프 탭 디폴트 선택 여부 확인 및 닫기
            home_page.click_close_life_tab(wd)

            # 라이프 탭 선택
            home_page.click_tab_name(wd, '라이프')

            # 라이프 선택 시, 노출되는 탭 이름 비교
            save_tab_names = home_page.save_tab_names(wd)
            test_result = home_page.check_tab_names(self, test_result, warning_texts, 'life', save_tab_names)

            # 라이프 선택 닫기
            home_page.click_close_life_tab(wd)

            # 기본으로 노출되는 탭 이름 비교
            save_tab_names = home_page.save_tab_names(wd)
            test_result = home_page.check_tab_names(self, test_result, warning_texts, 'home', save_tab_names)

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '우먼').click()

            # 홈화면 배너 API 호출
            response = requests.get(
                f'https://content-api.29cm.co.kr/api/v4/banners?bannerDivision=HOME_MOBILE&gender={self.pconf["gender"]}')
            if response.status_code == 200:
                # 호출한 API의 모든 배너 타이틀 저장
                banner_api_data = response.json()
                banner_count = int(banner_api_data['data']['count'])

                # 모든 홈 배너의 id와 contents를 저장해서 중복 여부를 확인
                banner_id = []
                for i in range(0, banner_count):
                    banner_id_api = banner_api_data['data']['bannerList'][i]['bannerId']
                    banner_id.append(banner_id_api)
                id_duplicate = set()
                check_id = [x for x in banner_id if x in id_duplicate or (id_duplicate.add(x) or False)]

                banner_contents = []
                for i in range(0, banner_count):
                    banner_contents_api = banner_api_data['data']['bannerList'][i]['bannerId']
                    banner_contents.append(banner_contents_api)
                contents_duplicate = set()
                check_contents = [x for x in banner_contents if
                                  x in contents_duplicate or (contents_duplicate.add(x) or False)]

                if not check_id and not check_contents:
                    print('중복된 홈 배너 없음 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('중복된 홈 배너 없음 확인 실패')
                    print(f'중복된 홈 배너 없음 확인 실패: {check_id} / {check_contents}')

                banner_title = []
                for i in range(0, banner_count):
                    banner_title_api = banner_api_data['data']['bannerList'][i]['bannerTitle']
                    if banner_title_api == 'ㅤ':
                        pass
                    else:
                        banner_title_api = banner_title_api.replace('\n', " ")
                        banner_title.append(banner_title_api)

                # 홈화면 배너 타이틀 3개 저장
                banner_home = []
                for i in range(0, 3):
                    sleep(2)
                    try:
                        banner_title_text = wd.find_element(AppiumBy.XPATH,
                                                            '//XCUIElementTypeOther[@name="home_banner_title"]/XCUIElementTypeStaticText').text
                        banner_home.append(banner_title_text)
                        print(banner_title_text)
                    except NoSuchElementException:
                        print("타이틀 없는 배너")
                        pass
                    except Exception:
                        # 에러 발생하여 타이틀 확인 실패 시, 이전 배너로 스와이프하여 타이틀 저장
                        banner = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'home_banner')
                        com_utils.element_control.swipe_control(wd, banner, 'right', 30)
                        banner_title_text = wd.find_element(AppiumBy.XPATH,
                                                            '//XCUIElementTypeOther[@name="home_banner_title"]/XCUIElementTypeStaticText').text
                        banner_home.append(banner_title_text)
                        print(banner_title_text)

                # API 호출 배너 리스트와 저장된 홈 배너 리스트 비교 (저장한 홈 배너 리스트 안에 호출한 리스트가 포함되면 pass)
                if any(banner in banner_title for banner in banner_home):
                    print('홈 배너 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('홈 배너 확인 실패')
                    print(f'홈 배너 확인 실패: {set(banner_home).difference(set(banner_title))}')
            else:
                test_result = 'WARN'
                warning_texts.append('피드 컨텐츠 API 불러오기 실패')
                print('피드 컨텐츠 API 불러오기 실패')

            # 다이나믹 게이트 -> 센스있는 선물하기 선택
            for i in range(0, 3):
                try:
                    wd.find_element(AppiumBy.ACCESSIBILITY_ID, '센스있는 선물하기').click()
                    sleep(3)
                    break
                except NoSuchElementException:
                    dynamic_gate = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'dynamic_gate')
                    com_utils.element_control.swipe_control(wd, dynamic_gate, 'left', 30)

            # 상단 타이틀과 선물하기 페이지 내부 타이틀 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '센스있는 선물하기')
                context_change.switch_context(wd, 'webview')
                wd.find_element(AppiumBy.XPATH, '//span[contains(text(), "선물인가요")]')
                print('다이나믹 게이트 타이틀 확인')
                context_change.switch_context(wd, 'native')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('다이나믹 게이트 타이틀 확인 실패')
                print('다이나믹 게이트 타이틀 확인 실패')

            # 뒤로가기 버튼 동작하지 않아 딥링크 사용하여 Home으로 이동
            wd.get('app29cm://home')

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
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '홈화면의 배너, 다이나믹 게이트 확인')
            return result_data

    def test_home_contents(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        print(f'[{test_name}] 테스트 시작')

        try:
            # 바텀시트 노출 여부 확인
            bottom_sheet.find_icon_and_close_bottom_sheet(wd)

            # # 로그인한 유저의 추천 탭 타이틀 확인
            # home_page.click_tab_name(wd, '추천')
            # test_result = home_page.check_entry_recommended_tab(self, wd, test_result, warning_texts)

            # 우먼 카테고리 탭 선택
            home_page.click_tab_name(wd, '우먼')

            # 피드 정보 불러오기
            feed_title_list = Home.check_feed_title(self)
            feed_title_1st = feed_title_list[0]
            feed_contain_item = feed_title_list[1]
            feed_title_2nd = feed_title_list[2]

            # 저장한 첫번째 피드 정보와 동일한 피드 정보가 노출 될 때까지 스크롤
            test_result = home_page.scroll_to_feed_contents(wd, test_result, warning_texts, feed_title_1st)

            # 싱픔이 연결된 피드 정보와 동일한 피드 정보가 노출 될 때까지 스크롤
            test_result = home_page.scroll_to_feed_contents(wd, test_result, warning_texts, feed_contain_item)

            # 좋아요 버튼 선택 전, 좋아요 수 저장
            content_like_count = home_page.save_contents_like_count(wd)

            # 좋아요 버튼 선택하여 좋아요 후, 카운트 확인
            home_page.click_contents_like_btn(wd)
            content_like_select = home_page.save_contents_like_count(wd)
            test_result = home_page.check_increase_like_count(test_result, warning_texts,
                                                              content_like_count, content_like_select)

            # 좋아요 버튼 선택하여 좋아요 해제 후, 카운트 확인
            home_page.click_contents_like_btn(wd)
            content_like_unselect = home_page.save_contents_like_count(wd)
            test_result = home_page.check_decrease_like_count(test_result, warning_texts,
                                                              content_like_count, content_like_unselect)

            # 컨텐츠 상품의 상품명과 상품가격 저장 후, 해당 상품의 상세 페이지 진입
            contents_prodcut_name = home_page.save_contents_product_name(wd)
            contents_product_price = home_page.save_contents_product_price(wd)
            home_page.click_contents_product(wd)

            # 상품명 비교 확인
            pdp_name = product_detail_page.save_product_name(wd)
            product_detail_page.check_product_name(pdp_name, contents_prodcut_name)

            # webview 전환
            context_change.switch_context(wd, 'webview')

            # 상품 가격 비교 확인
            pdp_price = product_detail_page.save_product_price(wd)
            product_detail_page.check_product_price(pdp_price, contents_product_price)

            # native 전환
            context_change.switch_context(wd, 'native')

            # Home으로 복귀
            product_detail_page.click_pdp_back_btn(wd)

            # 두번째 피드 정보와 동일한 피드 정보가 노출 될 때까지 스크롤
            test_result = home_page.scroll_to_feed_contents(wd, test_result, warning_texts, feed_title_2nd)

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
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '홈화면의 컨텐츠(피드) 탐색')
            return result_data

    def test_move_tab_from_home(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # CATEGORY 탭 진입
            navigation_bar.move_to_category(wd)

            wd.find_element(AppiumBy.XPATH,
                            '//XCUIElementTypeCollectionView[@index="2"]/XCUIElementTypeCell[@index="0"]').click()

            # 중 카테고리 리스트 중 상단 4개의 카테고리명을 리스트로 저장
            check_category = ['all', 'for_you', 'best', 'new']
            category_list = []
            for medium in check_category:
                category_cell = wd.find_element(AppiumBy.ACCESSIBILITY_ID, medium)
                category_text = category_cell.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text
                category_list.append(category_text)
            category_list = ', '.join(category_list)

            if self.conf['compare_category_list'] == category_list:
                print('HOME 탭에서 CATEGORY 탭 이동 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 CATEGORY 탭 이동 확인 실패')
                print(f'HOME 탭에서 CATEGORY 탭 이동 확인 실패 : {category_list}')

            # HOME 탭으로 이동하여 29CM 로고 확인
            navigation_bar.move_to_home(wd)
            home_page.check_home_logo(wd)

            # SEARCH 탭 진입
            navigation_bar.move_to_search(wd)

            # 첫번째 인기 브랜드 카테고리 타이틀 저장
            first_brand_category = search_total_popular_brand_name()['category_name']

            # 첫번째 인기 브랜드 카테고리 확인
            search_page.check_first_popular_brand_category(wd, first_brand_category)

            # 인기 브랜드 타이틀 확인
            search_page.check_popular_keyword_title(wd)

            # HOME으로 이동하여 29CM 로고 확인
            search_page.click_back_btn(wd)
            bottom_sheet.close_bottom_sheet(wd)
            home_page.check_home_logo(wd)

            # LIKE 탭 진입
            navigation_bar.move_to_like(wd)

            # LIKE 탭 상단 문구 확인
            test_result = like_page.check_like_phases(wd, test_result, warning_texts)

            # HOME 탭으로 이동하여 29CM 로고 확인
            navigation_bar.move_to_home(wd)
            home_page.check_home_logo(wd)

            # MY 탭 진입하여 닉네임 확인
            navigation_bar.move_to_my(wd)
            my_page.check_nickname(self, wd)

            # HOME 탭으로 이동하여 29CM 로고 확인
            navigation_bar.move_to_home(wd)
            home_page.check_home_logo(wd)

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
            com_utils.deeplink_control.move_to_home_iOS(self, wd)

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            send_test_result(self, test_result, '홈화면에서 다른 탭으로 이동')
            return result_data
