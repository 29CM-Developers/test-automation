from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from com_utils.element_control import aal, aalc, aals
from com_utils.element_control import scroll_control


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


# period = 실시간, 일간, 주간, 월간
def click_period_sort(wd, period):
    aalc(wd, f'c_{period}')


def save_best_first_product_name(wd):
    product_name = aal(wd, 'best_item_title').text
    print(f'{product_name} 필터링 설정 확인')
    return product_name


def check_best_product_name(warning_texts, compare_name, product_name):
    print(f'베스트 PLP 상품명 확인 : {compare_name} / {product_name}')
    if compare_name in product_name:
        test_result = 'PASS'
        print('베스트 PLP 상품명 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('베스트 PLP 상품명 확인 실패')
        print(f'베스트 PLP 상품명 확인 실패 : {compare_name} / {product_name}')
    return test_result


def save_best_first_product_name(wd):
    product_name_list = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/contentsDescription"]')
    print(f"베스트 상품명 : {product_name_list[0].text} ")
    product_name = product_name_list[0].text
    return product_name


def save_best_first_product_price(wd):
    best_product_list_price = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/lastSalePrice"]')
    print(f"베스트 상품 가격 : {best_product_list_price[0].text} ")
    best_product_price = best_product_list_price[0].text
    return best_product_price


def click_best_first_product(wd):
    product_name_list = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/contentsDescription"]')
    product_name_list[0].click()
    sleep(1)
    close_bottom_sheet(wd)
