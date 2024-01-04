from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from com_utils.api_control import home_banner_info
from com_utils.element_control import ial, ialc, ials, scroll_control, swipe_control
from ios_automation.page_action import context_change
from ios_automation.page_action.bottom_sheet import close_bottom_sheet


def check_home_logo(wd):
    try:
        ial(wd, 'navi_logo_btn')
        print('HOME 탭으로 이동 확인')
    except NoSuchElementException:
        print('HOME 탭으로 이동 확인 실패')


def click_search_btn(wd):
    ialc(wd, 'navi_search_btn')


def click_close_life_tab(wd):
    tab = ial(wd, f'//*[contains(@label, "라이프")]/../../..')
    select_tab = ial(tab, '//XCUIElementTypeStaticText[1]').text
    if select_tab == '라이프':
        ialc(wd, 'ic close white')
    else:
        print('라이프 탭 디폴트 아님')
        pass


# click_tab_name : 선택하려는 상단 탭 이름 입력
def click_tab_name(wd, click_tab_name):
    ialc(wd, click_tab_name)


def save_tab_names(wd):
    tab = ials(wd, f'//*[contains(@label, "라이프")]/../../../XCUIElementTypeCell')
    tab_name_list = []
    for text in tab:
        tab_name = text.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text
        tab_name_list.append(tab_name)
    tab_name_list = ', '.join(tab_name_list)
    return tab_name_list


# tab : 탭을 보여주는 카테고리 / 전체 : 'home' / 라이프 선택 상태 : 'life'
# tab_list : 비교할 탭 이름 리스트
def check_tab_names(self, tab, tab_list):
    if self.conf['compare_home_tab'][tab] in tab_list:
        print(f'홈 상단 {tab} 탭 확인')
    else:
        print(f'홈 상단 {tab} 탭 확인 실패 - {tab_list}')
        raise Exception(f'홈 상단 {tab} 탭 확인 실패')


def click_dynamic_gate(wd):
    # 다이나믹 게이트 -> 센스있는 선물하기 선택
    for i in range(0, 3):
        try:
            element = ial(wd, '센스있는 선물하기')
            if element.is_displayed():
                ialc(wd, '센스있는 선물하기')
                sleep(3)
                break
            else:
                dynamic_gate = ial(wd, 'dynamic_gate')
                swipe_control(wd, dynamic_gate, 'left', 30)
        except NoSuchElementException:
            dynamic_gate = ial(wd, 'dynamic_gate')
            swipe_control(wd, dynamic_gate, 'left', 30)


def check_dynamic_gate_gift_page(wd):
    try:
        ial(wd, '센스있는 선물하기')
        context_change.switch_context(wd, 'webview')
        ial(wd, '//span[contains(text(), "선물인가요")]')
        print('다이나믹 게이트 타이틀 확인')
        context_change.switch_context(wd, 'native')
    except NoSuchElementException:
        print('다이나믹 게이트 타이틀 확인 실패')
        raise Exception('다이나믹 게이트 타이틀 확인 실패')


def check_for_duplicate_banner_contents(self):
    # 홈화면 배너 API 호출
    banner_data = home_banner_info(self)
    banner_ids = banner_data['banner_ids']
    banner_contents = banner_data['banner_contents']

    # 모든 홈 배너의 id와 contents의 중복 여부를 확인
    check_id = len(banner_ids) != len(set(banner_ids))
    check_contents = len(banner_contents) != len(set(banner_contents))

    if not check_id:
        if not check_contents:
            print('중복된 홈 배너 id와 컨텐츠 없음 확인')
        else:
            print('중복된 홈 배너 id는 없으나, 동일한 컨텐츠 있음 확인')
    else:
        print(f'중복된 홈 배너 없음 확인 실패')
        raise Exception('중복된 홈 배너 없음 확인 실패')


def save_banner_title(wd):
    title_element = '//XCUIElementTypeOther[@name="home_banner_title"]/XCUIElementTypeStaticText'
    banner_titles = []
    for i in range(0, 3):
        try:
            WebDriverWait(wd, 10).until(EC.element_attribute_to_include((By.XPATH, title_element), 'label'))
            banner_title = ial(wd, title_element).text
            banner_titles.append(banner_title)
        except Exception:
            pass
        sleep(2)
    return banner_titles


def check_home_banner_title(self, home_banner_title):
    # 홈화면 배너 api 호출하여 타이틀 저장
    api_banner_title = home_banner_info(self)['banner_titles']

    # API 호출 배너 리스트와 저장된 홈 배너 리스트 비교 (저장한 홈 배너 리스트 안에 호출한 리스트가 포함되면 pass)
    if any(banner in api_banner_title for banner in home_banner_title):
        print('홈 배너 확인')
    else:
        print(f'홈 배너 확인 실패: {set(home_banner_title).difference(set(api_banner_title))}')
        raise Exception('홈 배너 확인 실패')


def check_scroll_to_recommended_contents(wd):
    find_contents = False
    for i in range(0, 5):
        try:
            recommend_text = ial(wd, 'c_위한 추천')
            if recommend_text.is_displayed():
                find_contents = True
                print('홈화면 추천 타이틀 확인')
                break
            else:
                scroll_control(wd, 'D', 50)
        except NoSuchElementException:
            scroll_control(wd, 'D', 60)
    if not find_contents:
        print('홈화면 추천 타이틀 확인 실패')
        raise Exception('홈화면 추천 타이틀 확인 실패')


def scroll_to_feed_contents(wd, feed_title):
    find_contents = False
    for i in range(0, 10):
        try:
            feed_contents = wd.find_elements(AppiumBy.ACCESSIBILITY_ID, 'home_content_title')
            for title in feed_contents:
                if title.is_displayed() and feed_title == title.text:
                    find_contents = True
                    print('피드 컨텐츠 노출 확인')
                    break
            else:
                scroll_control(wd, 'D', 40)
        except NoSuchElementException:
            scroll_control(wd, 'D', 60)
        if find_contents:
            break
    if not find_contents:
        print('피드 컨텐츠 노출 확인 실패')
        raise Exception('피드 컨텐츠 노출 확인 실패')


def save_contents_like_count(wd):
    content_like_count = ial(wd, 'home_content_like_count')
    for i in range(0, 3):
        if content_like_count.is_displayed():
            content_like_count = int(content_like_count.text.replace(',', ''))
            break
        else:
            scroll_control(wd, 'D', 30)
    return content_like_count


def click_contents_like_btn(wd):
    ialc(wd, 'home_content_like_btn')


def check_increase_like_count(heart_count, heart_select):
    if heart_select == heart_count + 1:
        print('피드 아이템 좋아요 개수 증가 확인')
    else:
        print(f'피드 아이템 좋아요 개수 증가 확인 실패: {heart_count} / {heart_select}')
        raise Exception('피드 아이템 좋아요 개수 증가 확인 실패')


def check_decrease_like_count(heart_count, heart_unselect):
    if heart_unselect == heart_count:
        print('피드 아이템 좋아요 개수 차감 확인')
    else:
        print(f'피드 아이템 좋아요 개수 차감 확인 실패: {heart_count} / {heart_unselect}')
        raise Exception('피드 아이템 좋아요 개수 차감 확인 실패')


def save_contents_product_name(wd):
    product_name = ial(wd,
                       '//XCUIElementTypeOther[@name="home_content_product"]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText[2]').text
    product_name = product_name.strip()
    return product_name


def save_contents_product_price(wd):
    product_price = ial(wd,
                        '//XCUIElementTypeOther[@name="home_content_product"]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText[3]').text
    if '%' in product_price:
        percent = product_price.find('%')
        start_index = percent + 2
        end_index = len(product_price)
        product_price = int(product_price[start_index:end_index].replace(',', ''))
    else:
        product_price = int(product_price.replace(',', ''))
    return product_price


def click_contents_product(wd):
    ialc(wd, '//XCUIElementTypeOther[@name="home_content_product"]')
    sleep(1)
    close_bottom_sheet(wd)
