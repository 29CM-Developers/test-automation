from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ialc, ial, ials, ialwc
from ios_automation.page_action import context_change


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


def clear_cart_list(wd):
    wd.get('app29cm://order/cart')
    sleep(3)
    try:
        ial(wd, '//XCUIElementTypeLink[@name="CONTINUE SHOPPING"]')
        pass
    except NoSuchElementException:
        context_change.switch_context(wd, 'webview')
        all_select = wd.find_element(AppiumBy.XPATH, '//label[contains(text(), "전체선택")]')
        select_count = all_select.text
        index = select_count.find('/')
        if select_count[index - 1] != select_count[index + 1]:
            all_select.click()
        ialwc(wd, '//button[contains(text(), "선택삭제")]')
        print('장바구니에 담긴 상품 삭제 완료')
        context_change.switch_context(wd, 'native')
    click_back_btn(wd)


def save_number_of_order_product(wd):
    info = ial(wd, '//strong[contains(text(), "총")]').text
    order_product_count = int(info.replace('총 ', ''))
    return order_product_count


def save_total_order_price(wd):
    info = ial(wd, '//dt[contains(text(), "주문금액")]/..')
    count = ials(info, '//dd')
    total_price = int(count[1].text.replace(',', '').replace('원', ''))
    return total_price


def save_product_name_list(wd):
    cart_product_name = []
    product = ials(wd, '//a[contains(@href, "product.29cm.co.kr/catalog")][contains(@class, "css")]')
    for name in product[0:2]:
        product_name = name.text
        cart_product_name.append(product_name)
    sleep(2)
    return cart_product_name


def save_product_name(wd):
    product_name = ial(wd, '//a[contains(@href, "product.29cm.co.kr/catalog")][contains(@class, "css")]').text
    return product_name


def save_product_price(wd):
    product_price = wd.find_element(AppiumBy.XPATH, '//span[contains(@class, "css-bmeojf")]')
    product_price = int(product_price.text.replace(',', ''))
    return product_price


def save_product_count(wd):
    product_count = wd.find_element(AppiumBy.CSS_SELECTOR, '[inputmode="numeric"]').get_attribute('value')
    product_count = int(product_count)
    return product_count


def click_delete_product(wd):
    ialwc(wd, '//div[2]/button[contains(text(), "삭제")]')
    sleep(2)


def click_add_product(wd):
    ialwc(wd, '//button[contains(text(), "+")]')
    sleep(2)


def check_cart_product_list(wd, best_pdp_name, keyword_pdp_name):
    cart_product_list = save_product_name_list(wd)
    if best_pdp_name in cart_product_list and keyword_pdp_name in cart_product_list:
        print('장바구니 리스트 확인')
    else:
        print(f'장바구니 리스트 확인 실패 - {cart_product_list}')
        raise Exception('장바구니 리스트 확인 실패')


def check_delete_product(before_count, after_count, before_price, after_price, product_price):
    if after_count == before_count - 1 and after_price == before_price - product_price:
        print('장바구니 상품 제거 확인')
    else:
        print('장바구니 상품 제거 확인 실패')
        raise Exception('장바구니 상품 제거 확인 실패')


def check_add_product(before_count, after_count, before_price, after_price, product_price):
    if after_count == before_count + 1 and after_price == before_price + product_price:
        print('장바구니 상품 추가 확인')
    else:
        print('장바구니 상품 변경 추가 실패')
        raise Exception('장바구니 상품 변경 추가 실패')


def click_check_out_btn(wd):
    ialwc(wd, '//button[contains(text(), "CHECK OUT")]')
    sleep(3)
