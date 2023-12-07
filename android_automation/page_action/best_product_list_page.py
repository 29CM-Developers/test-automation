from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc
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
