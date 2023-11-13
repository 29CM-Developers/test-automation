from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


def click_pdp_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()


def save_product_name(wd):
    pdp_web = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView')
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'Select a slide to show')
        product_name = pdp_web.find_element(AppiumBy.XPATH,
                                            '//XCUIElementTypeOther[@index="5"]/XCUIElementTypeStaticText').get_attribute(
            'name')
    except NoSuchElementException:
        product_name = pdp_web.find_element(AppiumBy.XPATH,
                                            '//XCUIElementTypeOther[@index="4"]/XCUIElementTypeStaticText').get_attribute(
            'name')
    print(f'PDP 상품명 : {product_name}')
    return product_name


def save_remove_prefix_product_name(product_name):
    start_index = product_name.find('_') + 1
    end_index = len(product_name)
    no_prefix_product_name = product_name[start_index:end_index]

    return no_prefix_product_name


# product_name : pdp 상품명
# compare_name: pdp 상품명과 비교한 상품명
def check_product_name(warning_texts, product_name, compare_name):
    if compare_name in product_name:
        test_result = 'PASS'
        print('PDP 진입 확인 - 상품명')
    else:
        test_result = 'WARN'
        warning_texts.append('PDP 진입 확인 실패')
        print(f'PDP 진입 확인 실패 - pdp: {product_name} / 비교: {compare_name}')
    return test_result


def close_purchase_modal(wd):
    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView').click()


def check_open_to_purchase_modal(wd, warning_texts):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니 담기')
        test_result = 'PASS'
        print('PDP 구매하기 모달 노출 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('PDP 구매하기 모달 노출 확인 실패')
        print('PDP 구매하기 모달 노출 확인')
    return test_result
