from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, ials, swipe_control, element_scroll_control, scroll_control


def click_back_btn(wd):
    ialc(wd, 'navi_back_btn')


def click_pin_menu(wd, find_menu):
    pin_menu_list = ial(wd, '//XCUIElementTypeOther[2]/XCUIElementTypeCollectionView')
    click_break = False
    for i in range(0, 5):
        try:
            pin_menu = ials(wd, '//XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell')
            for pin in pin_menu:
                pin_menu_title = ial(pin, '//XCUIElementTypeOther/XCUIElementTypeStaticText')
                if pin_menu_title.text == find_menu:
                    click_break = True
                    pin_menu_title.click()
            swipe_control(wd, pin_menu_list, 'left', 30)
        except NoSuchElementException:
            pass
        if click_break:
            break


def check_large_category_list(wd, api_large_categoty_list):
    large_category_list = []
    for i in range(0, 3):
        # 대 카테고리 리스트 저장
        large_category = wd.find_elements(AppiumBy.ACCESSIBILITY_ID, 'large_category')
        for large in large_category:
            large_category_text = ial(large, '//XCUIElementTypeStaticText').text
            if large_category_text not in large_category_list:
                large_category_list.append(large_category_text)
        if len(large_category_list) < len(api_large_categoty_list):
            # 대 카테고리 영역 스크롤 동작
            large_field = ial(wd, 'large_category_list')
            element_scroll_control(wd, large_field, 'D', 30)
        else:
            break
    print(f'대카테고리 리스트 : {large_category_list}')

    if api_large_categoty_list == large_category_list:
        print('대 카테고리 리스트 확인')
    else:
        print('대 카테고리 리스트 확인 실패')
        raise Exception('카테고리 리스트 확인 실패')


def scroll_up_large_category(wd):
    large_field = ial(wd, 'large_category_list')
    element_scroll_control(wd, large_field, 'U', 30)


def click_first_large_category(wd):
    ialc(wd, '//XCUIElementTypeCell[@name="large_category"]')


def check_unique_medium_category(self, wd):
    check_category = ['all', 'for_you', 'best', 'new']
    category_list = []
    for medium in check_category:
        category_cell = ial(wd, medium)
        category_text = ial(category_cell, '//XCUIElementTypeStaticText').text
        category_list.append(category_text)
    category_list = ', '.join(category_list)

    if self.conf['compare_category_list'] == category_list:
        print('Unique 카테고리 확인')
    else:
        print(f'Unique 카테고리 확인 실패 : {category_list}')
        raise Exception('Unique 카테고리 확인 실패')


def click_for_you_category(wd):
    ialc(wd, 'for_you')


def click_best_category(wd):
    ialc(wd, 'best')


def click_category(wd, category_name):
    ialc(wd, category_name)


'''
카테고리 PLP
'''


def check_not_login_user_recommended_tab(wd):
    try:
        ial(wd, 'c_당신을 위한 추천')
        print('비로그인 유저 추천 페이지 타이틀 확인')
    except NoSuchElementException:
        print('비로그인 유저 추천 페이지 타이틀 확인 실패')
        raise Exception('비로그인 유저 추천 페이지 타이틀 확인 실패')


def save_webview_category_product_name(wd):
    product = wd.find_element(AppiumBy.CSS_SELECTOR, '[class="css-j22x2q e13ypwtz2"]')
    plp_name = product.find_element(AppiumBy.XPATH, '//h5').text
    return plp_name


def check_category_page_title(wd, category_name):
    sleep(3)
    try:
        ial(wd, f'//XCUIElementTypeButton[@name="{category_name}"]')
        print(f'{category_name} 카테고리 PLP 진입 확인')
    except NoSuchElementException:
        print(f'{category_name} 카테고리 PLP 진입 확인 실패')
        raise Exception(f'{category_name} 카테고리 PLP 진입 확인 실패')


def click_filter_by_new(wd):
    ialc(wd, 'sort_filter')
    ialc(wd, '**/XCUIElementTypeButton[`label == "신상품순"`]')


def save_category_product_name(wd):
    for i in range(0, 5):
        try:
            category_product = ial(wd, 'product_name')
            if category_product.is_displayed():
                break
            else:
                scroll_control(wd, 'D', 30)
        except NoSuchElementException:
            scroll_control(wd, 'D', 30)
    plp_name = ial(wd, 'product_name').text
    return plp_name


def check_category_product_name(plp_name, compare_name):
    if plp_name == compare_name:
        print('카테고리 페이지의 상품 확인')
    else:
        print('카테고리 페이지의 상품 확인 실패')
        raise Exception('카테고리 페이지의 상품 확인 실패')


def save_category_product_price(wd):
    price = ial(wd, '//XCUIElementTypeOther[@name="product_price"]/XCUIElementTypeStaticText').text
    if '%' in price:
        percent = price.find('%')
        start_index = percent + 2
        end_index = len(price)
        price = price[start_index:end_index].replace('원', '')
    else:
        price = price.replace('원', '')
    price = int(price.replace(',', ''))
    print(f'PLP 가격 : {price}')
    return price


def click_category_product(wd):
    ialc(wd, 'product_name')


def click_not_login_user_product_like_btn(wd):
    ialc(wd, 'like_btn')
    ialc(wd, '//XCUIElementTypeButton[@name="확인"]')
