from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, ials, swipe_control, element_scroll_control, scroll_control


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


def check_large_category_list(wd, warning_texts, api_large_categoty_list):
    large_category_list = []
    for i in range(0, 3):
        # 대 카테고리 리스트 저장
        large_category = wd.find_elements(AppiumBy.ACCESSIBILITY_ID, 'large_category')
        for large in large_category:
            large_category_text = large.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text
            if large_category_text not in large_category_list:
                large_category_list.append(large_category_text)
        if len(large_category_list) < len(api_large_categoty_list):

            # 대 카테고리 영역 스크롤 동작
            large_field = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'large_category_list')
            element_scroll_control(wd, large_field, 'D', 30)
        else:
            break
    print(f'대카테고리 리스트 : {large_category_list}')

    if api_large_categoty_list == large_category_list:
        test_result = 'PASS'
        print('대 카테고리 리스트 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('카테고리 리스트 확인 실패')
        print('대 카테고리 리스트 확인 실패')
    return test_result


def scroll_up_large_category(wd):
    large_field = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'large_category_list')
    element_scroll_control(wd, large_field, 'U', 30)


def click_best_category(wd):
    ialc(wd, 'best')


def click_category(wd, category_name):
    ialc(wd, category_name)


def check_category_page_title(wd, warning_texts, category_name):
    sleep(3)
    try:
        wd.find_element(AppiumBy.XPATH, f'//XCUIElementTypeButton[@name="{category_name}"]')
        test_result = 'PASS'
        print(f'{category_name} 카테고리 PLP 진입 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append(f'{category_name} 카테고리 PLP 진입 확인 실패')
        print(f'{category_name} 카테고리 PLP 진입 확인 실패')
    return test_result


def click_filter_by_new(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'sort_filter').click()
    wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "신상품순"`]').click()


def save_category_product_name(wd):
    for i in range(0, 5):
        try:
            category_product = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'product_name')
            if category_product.is_displayed():
                break
            else:
                scroll_control(wd, 'D', 30)
        except NoSuchElementException:
            scroll_control(wd, 'D', 30)
    plp_name = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'product_name').text
    return plp_name


def check_category_product_name(warning_texts, plp_name, compare_name):
    if plp_name == compare_name:
        test_result = 'PASS'
        print('카테고리 페이지의 상품 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('카테고리 페이지의 상품 확인 실패')
        print('카테고리 페이지의 상품 확인 실패')
    return test_result
