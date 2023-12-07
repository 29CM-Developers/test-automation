from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, scroll_control


def check_home_logo(wd):
    try:
        ial(wd, 'navi_logo_btn')
        print('HOME 탭으로 이동 확인')
    except NoSuchElementException:
        print('HOME 탭으로 이동 확인 실패')


def click_close_life_tab(wd):
    select_tab = ial(wd,
                     '//XCUIElementTypeOther[3]/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeStaticText').text
    if select_tab == '라이프':
        ialc(wd, 'ic close white')
    else:
        print('라이프 탭 디폴트 아님')
        pass


# click_tab_name : 선택하려는 상단 탭 이름 입력
def click_tab_name(wd, click_tab_name):
    ialc(wd, click_tab_name)


def save_tab_names(wd):
    tab = wd.find_elements(AppiumBy.XPATH,
                           '//XCUIElementTypeOther[3]/XCUIElementTypeCollectionView/XCUIElementTypeCell')
    tab_name_list = []
    for text in tab:
        tab_name = text.find_element(AppiumBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeStaticText').text
        tab_name_list.append(tab_name)
    tab_name_list = ', '.join(tab_name_list)
    print(tab_name_list)
    return tab_name_list


# tab : 탭을 보여주는 카테고리 / 전체 : 'home' / 라이프 선택 상태 : 'life'
# tab_list : 비교할 탭 이름 리스트
def check_tab_names(self, test_result, warning_texts, tab, tab_list):
    if self.conf['compare_home_tab'][tab] in tab_list:
        print('홈 상단 탭 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('홈 상단 탭 확인 실패')
        print('홈 상단 탭 확인 실패')
    return test_result


def check_entry_recommended_tab(self, wd, test_result, warning_texts):
    try:
        ial(wd, f'{self.pconf["nickname"]}님을 위한 추천 상품')
        print('홈화면 추천 탭 타이틀 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('홈화면 추천 탭 타이틀 확인 실패')
        print('홈화면 추천 탭 타이틀 확인 실패')
    return test_result


def check_not_login_user_recommended_tab(wd):
    try:
        ial(wd, '당신을 위한 추천 상품')
        print('비로그인 유저 홈화면 추천 탭 타이틀 확인')
    except NoSuchElementException:
        print('비로그인 유저 홈화면 추천 탭 타이틀 확인 실패')
        raise Exception('비로그인 유저 홈화면 추천 탭 타이틀 확인 실패')


def scroll_to_feed_contents(wd, test_result, warning_texts, feed_title):
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
        test_result = 'WARN'
        warning_texts.append('피드 컨텐츠 노출 확인 실패')
        print('피드 컨텐츠 노출 확인 실패')
    return test_result


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


def check_increase_like_count(test_result, warning_texts, heart_count, heart_select):
    if heart_select == heart_count + 1:
        print('피드 아이템 좋아요 개수 증가 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('피드 아이템 좋아요 개수 증가 확인 실패')
        print(f'피드 아이템 좋아요 개수 증가 확인 실패: {heart_count} / {heart_select}')
    return test_result


def check_decrease_like_count(test_result, warning_texts, heart_count, heart_unselect):
    if heart_unselect == heart_count:
        print('피드 아이템 좋아요 개수 차감 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('피드 아이템 좋아요 개수 차감 확인 실패')
        print(f'피드 아이템 좋아요 개수 차감 확인 실패: {heart_count} / {heart_unselect}')
    return test_result


def save_contents_product_name(wd):
    product_name = ial(wd,
                       '//XCUIElementTypeOther[@name="home_content_product"]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText[2]').text
    product_name = product_name.strip()
    print(f'컨텐츠의 상품명 : {product_name}')
    return product_name


def save_contents_product_price(wd):
    product_price = ial(wd,
                        '//XCUIElementTypeOther[@name="home_content_product"]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText[3]').text
    if '%' in product_price:
        percent = product_price.find('%')
        start_index = percent + 2
        end_index = len(product_price)
        product_price = int(product_price[start_index:end_index].replace(',', ''))
    print(f'컨텐츠의 상품가격 : {product_price}')
    return product_price


def click_contents_product(wd):
    ialc(wd, '//XCUIElementTypeOther[@name="home_content_product"]')
