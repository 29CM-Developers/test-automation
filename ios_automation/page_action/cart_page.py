from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.api_control import cart_product_count, add_product_to_cart
from com_utils.deeplink_control import move_to_cart
from com_utils.element_control import ialc, ial, ials
from ios_automation.page_action import context_change


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


def clear_cart_list(self, wd):
    move_to_cart(self, wd)
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
        ialc(wd, '//*[@id="select_product_delete_btn"]')
        print('장바구니에 담긴 상품 삭제 완료')
        context_change.switch_context(wd, 'native')
    click_back_btn(wd)


def save_number_of_order_product(wd):
    info = ial(wd, '//*[@id="number_of_order_products"]').text
    order_product_count = int(info.replace('총 ', ''))
    return order_product_count


def save_total_order_price(wd):
    total_price = int(ial(wd, '//*[@id="total_order_amount"]').text.replace(',', '').replace('원', ''))
    return total_price


def save_product_name_list(wd):
    cart_product_name = []
    product = ials(wd, '//*[contains(@id, "product_title")]')
    for name in product[0:2]:
        product_name = name.text
        cart_product_name.append(product_name)
    sleep(2)
    return cart_product_name


def save_product_name(wd):
    product_name = ial(wd, '//*[contains(@id, "product_title")]').text
    return product_name


def save_product_price(wd):
    product_price = ial(wd, '//*[contains(@id, "product_amount")]')
    product_price = int(product_price.text.replace(',', ''))
    return product_price


def save_product_count(wd):
    product_count = ial(wd, '//*[contains(@id, "number_of_products")]').get_attribute('value')
    product_count = int(product_count)
    return product_count


def click_delete_product(wd):
    ialc(wd, '//*[contains(@id, "product_delete_btn_")]')
    sleep(2)


def click_add_product(wd):
    ialc(wd, '//*[contains(@id, "add_product_btn")]')
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
    ialc(wd, '//button[contains(text(), "CHECK OUT")]')
    sleep(3)


def check_need_to_add_product_to_cart(self, wd, id, password):
    cart_count = cart_product_count(id, password)
    if cart_count < 2:
        while cart_count < 2:
            add_product_to_cart(id, password)
            cart_count = cart_product_count(id, password)
        move_to_cart(self, wd)
