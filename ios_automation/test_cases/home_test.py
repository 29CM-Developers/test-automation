import os
import sys
import traceback
import requests
import com_utils.element_control

from com_utils import values_control
from time import time, sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


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
            # 홈화면 배너 API 호출
            response = requests.get(
                f'https://content-api.29cm.co.kr/api/v4/banners?bannerDivision=HOME_MOBILE&gender={self.pconf["gender"]}')
            if response.status_code == 200:
                # 호출한 API의 모든 배너 타이틀 저장
                banner_api_data = response.json()
                banner_count = int(banner_api_data['data']['count'])

                banner_api = []
                for i in range(0, banner_count):
                    banner_title_api = banner_api_data['data']['bannerList'][i]['bannerTitle']
                    if banner_title_api == 'ㅤ':
                        pass
                    else:
                        banner_api.append(banner_title_api)

                # 홈화면 배너 타이틀 모두 저장
                banner_home = []
                for i in range(0, 3):
                    sleep(2)
                    try:
                        banner_title_text = wd.find_element(AppiumBy.XPATH,
                                                            '//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeStaticText').text
                        banner_home.append(banner_title_text)
                        print(banner_title_text)
                    except NoSuchElementException:
                        print("타이틀 없는 배너")
                        pass
                    except Exception:
                        # 에러 발생하여 타이틀 확인 실패 시, 이전 배너로 스와이프하여 타이틀 저장
                        banner = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeCollectionView/XCUIElementTypeCell')
                        com_utils.element_control.swipe_control(wd, banner, 'right', 30)
                        banner_title_text = wd.find_element(AppiumBy.XPATH,
                                                            '//XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeStaticText').text
                        banner_home.append(banner_title_text)
                        print(banner_title_text)

                # API 호출 배너 리스트와 저장된 홈 배너 리스트 비교 (저장한 홈 배너 리스트 안에 호출한 리스트가 포함되면 pass)
                if set(banner_home).issubset(set(banner_api)):
                    print('홈 배너 확인')
                else:
                    test_result = 'WARN'
                    warning_texts.append('홈 배너 확인 실패')
                    print(f'홈 배너 확인 실패: {set(banner_home).difference(set(banner_api))}')
            else:
                test_result = 'WARN'
                warning_texts.append('피드 컨텐츠 API 불러오기 실패')
                print('피드 컨텐츠 API 불러오기 실패')

            # 다이나믹 게이트 -> 센스있는 선물하기 선택
            for i in range(0, 3):
                try:
                    wd.find_element(AppiumBy.ACCESSIBILITY_ID, '센스있는 선물하기').click()
                    break
                except NoSuchElementException:
                    dynamic_gate = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeOther[@index="0"]/XCUIElementTypeOther[@index="1"]/XCUIElementTypeScrollView')
                    com_utils.element_control.swipe_control(wd, dynamic_gate, 'left', 30)

            sleep(3)
            print("!! 상단 타이틀 비교 진행 필요")

            # 웹뷰 요소가 잡히지 않아 비교할 요소값 확인 불가
            # 아래 뒤로가기 동작 안함
            # wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()

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
            wd.get('app29cm://home')

        finally:
            run_time = f"{time() - start_time:.2f}"
            warning = [str(i) for i in warning_texts]
            warning_points = "\n".join(warning)
            result_data = {
                'test_result': test_result, 'error_texts': error_texts, 'img_src': img_src,
                'test_name': test_name, 'run_time': run_time, 'warning_texts': warning_points}
            return result_data

    def test_home_contents(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()
        print(f'[{test_name}] 테스트 시작')

        try:
            # 로그인한 유저의 추천 탭 타이틀 확인
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '추천').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, f'{self.pconf["nickname"]}님을 위한 추천 상품')
                print('홈화면 추천 탭 타이틀 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('홈화면 추천 탭 타이틀 확인 실패')
                print('홈화면 추천 탭 타이틀 확인 실패')

            # 우먼 카테고리 탭 선택
            wd.find_element(AppiumBy.ACCESSIBILITY_ID, '우먼').click()

            # 피드 정보 불러오기
            feed_title_list = Home.check_feed_title(self)
            feed_title_1st = feed_title_list[0]
            feed_contain_item = feed_title_list[1]
            feed_title_2nd = feed_title_list[2]

            # 저장한 첫번째 피드 정보와 동일한 피드 정보가 노출 될 때까지 스크롤
            for i in range(0, 10):
                try:
                    feed_contents = wd.find_element(AppiumBy.XPATH,
                                                    '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeStaticText').text
                    if feed_title_1st == feed_contents:
                        print('첫번째 피드 컨텐츠 노출 확인')
                        break
                    else:
                        com_utils.element_control.scroll_control(wd, 'D', 50)
                        print('첫번째 피드 확인 안되어 스크롤')
                except NoSuchElementException:
                    com_utils.element_control.scroll_control(wd, 'D', 50)

            # 싱픔이 연결된 피드 정보와 동일한 피드 정보가 노출 될 때까지 스크롤
            for i in range(0, 10):
                try:
                    feed_contents = wd.find_element(AppiumBy.XPATH,
                                                    '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeStaticText').text
                    if feed_contain_item == feed_contents:
                        print('상품이 연결된 첫번째 피드 컨텐츠 노출 확인')
                        break
                    else:
                        com_utils.element_control.scroll_control(wd, 'D', 50)
                        print('싱품이 연결된 첫번째 피드 확인 안되어 스크롤')
                except NoSuchElementException:
                    com_utils.element_control.scroll_control(wd, 'D', 50)

            # 첫번째 피드의 첫번째 상품의 좋아요 xpath와 좋아요 수 xpath
            content_like_xpath = '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]'
            content_like_count_xpath = f'{content_like_xpath}/XCUIElementTypeStaticText'

            # 좋아요 버튼 선택 전, 좋아요 수 저장
            content_like_count = wd.find_element(AppiumBy.XPATH, content_like_count_xpath).text
            content_like_count = int(content_like_count.replace(',', ''))

            # 좋아요 버튼 선택 -> 찜하기 등록
            wd.find_element(AppiumBy.XPATH, content_like_xpath).click()
            content_like_select = wd.find_element(AppiumBy.XPATH, content_like_count_xpath).text
            content_like_select = int(content_like_select.replace(',', ''))
            if content_like_select == content_like_count + 1:
                print('피드 아이템 좋아요 개수 증가 확인')
                pass
            else:
                test_result = 'WARN'
                warning_texts.append('피드 아이템 좋아요 개수 증가 확인 실패')
                print('피드 아이템 좋아요 개수 증가 확인 실패')

            # 좋아요 버튼 선택 -> 찜하기 해제
            wd.find_element(AppiumBy.XPATH, content_like_xpath).click()
            content_like_select = wd.find_element(AppiumBy.XPATH, content_like_count_xpath).text
            content_like_select = int(content_like_select.replace(',', ''))
            if content_like_select == content_like_count:
                print('피드 아이템 좋아요 개수 차감 확인')
                pass
            else:
                test_result = 'WARN'
                warning_texts.append('피드 아이템 좋아요 개수 차감 확인 실패')
                print('피드 아이템 좋아요 개수 차감 확인 실패')

            # 두번째 피드 정보와 동일한 피드 정보가 노출 될 때까지 스크롤
            for i in range(0, 10):
                try:
                    feed_contents = wd.find_element(AppiumBy.XPATH,
                                                    '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="0"]/XCUIElementTypeOther/XCUIElementTypeStaticText').text
                    if feed_title_2nd == feed_contents:
                        print('피드 컨텐츠 추가 노출 확인')
                        break
                    else:
                        com_utils.element_control.scroll_control(wd, 'D', 50)
                        print('피드 컨텐츠 추가 노출 확인 안되어 스크롤')
                except NoSuchElementException:
                    com_utils.element_control.scroll_control(wd, 'D', 50)

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

    def test_move_tab_from_home(self, wd, test_result='PASS', error_texts=[], img_src='', warning_texts=[]):
        test_name = self.dconf[sys._getframe().f_code.co_name]
        start_time = time()

        try:
            print(f'[{test_name}] 테스트 시작')

            # CATEGORY 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "CATEGORY"`]').click()

            wd.find_element(AppiumBy.XPATH,
                            '//XCUIElementTypeCollectionView[@index="2"]/XCUIElementTypeCell[@index="0"]').click()

            # 중 카테고리 리스트 중 상단 4개의 카테고리명을 리스트로 저장
            medium_category_list = wd.find_elements(AppiumBy.XPATH,
                                                    '//XCUIElementTypeCollectionView[2]/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeStaticText')
            medium_category_list = medium_category_list[0:4]

            category_list = []
            for medium_category in medium_category_list:
                category_list.append(medium_category.text)
            category_list = ', '.join(category_list)

            if self.conf['compare_category_list'] == category_list:
                print('HOME 탭에서 CATEGORY 탭 이동 확인')
            else:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 CATEGORY 탭 이동 확인 실패')
                print(f'HOME 탭에서 CATEGORY 탭 이동 확인 실패 : {category_list}')

            # HOME 탭으로 이동
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "HOME"`]').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarLogoWhite')
                print('HOME 탭으로 이동')
            except NoSuchElementException:
                print('HOME 탭으로 이동 실패')

            # SEARCH 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "SEARCH"`]').click()

            # 인기 브랜드 타이틀 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '지금 많이 찾는 브랜드')
                print('HOME 탭에서 SEARCH 탭 이동 확인 - 인기 브랜드 타이틀')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 SEARCH 탭 이동 확인')
                print('HOME 탭에서 SEARCH 탭 이동 확인 실패 - 인기 브랜드 타이틀')

            # 인기 브랜드 타이틀 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, '지금 많이 찾는 검색어')
                print('HOME 탭에서 SEARCH 탭 이동 확인 - 인기 검색어 타이틀')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 SEARCH 탭 이동 확인')
                print('HOME 탭에서 SEARCH 탭 이동 확인 실패 - 인기 검색어 타이틀')

            wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarLogoWhite')
                print('HOME 탭으로 이동')
            except NoSuchElementException:
                print('HOME 탭으로 이동 실패')

            # LIKE 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "LIKE"`]').click()

            # LIKE 진입 시, 브랜드 추천 페이지 노출 여부 확인
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'recommended_brand_page')
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()
                print('브랜드 추천 페이지 노출')
            except NoSuchElementException:
                pass

            try:
                wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="LIKE"]')
                print('HOME 탭에서 LIKE 탭 이동 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 LIKE 탭 이동 확인 실패')
                print('HOME 탭에서 LIKE 탭 이동 확인 실패')

            # HOME 탭으로 이동
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "HOME"`]').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarLogoWhite')
                print('HOME 탭으로 이동')
            except NoSuchElementException:
                print('HOME 탭으로 이동 실패')

            # MY 탭 진입
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`label == "MY"`]').click()
            try:
                wd.find_element(AppiumBy.ACCESSIBILITY_ID, self.pconf['nickname'])
                print('HOME 탭에서 MY 탭 이동 확인')
            except NoSuchElementException:
                test_result = 'WARN'
                warning_texts.append('HOME 탭에서 MY 탭 이동 확인 실패')
                print('HOME 탭에서 MY 탭 이동 확인 실패')

            # HOME 탭으로 이동
            wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "HOME"`]').click()

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
