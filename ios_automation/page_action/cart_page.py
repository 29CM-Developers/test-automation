from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ialc, ial
from ios_automation.page_action import context_change


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


def clear_cart_list(wd):
    wd.get('app29cm://order/cart')
    sleep(3)
    try:
        ial(wd, '//XCUIElementTypeLink[@name="CONTINUE SHOPPING"]')
        print('장바구니에 담긴 상품 없음.')
        pass
    except NoSuchElementException:
        print('장바구니에 담긴 상품 있음.')
        context_change.switch_context(wd, 'webview')
        all_select = wd.find_element(AppiumBy.XPATH, '//label[contains(text(), "전체선택")]')
        select_count = all_select.text
        index = select_count.find('/')
        if select_count[index - 1] != select_count[index + 1]:
            all_select.click()
        ialc(wd, '//button[contains(text(), "선택삭제")]')
        print('장바구니 상품 삭제')
        context_change.switch_context(wd, 'native')
    click_back_btn(wd)


def save_number_of_order_product(wd):
    info = wd.find_elements(AppiumBy.CSS_SELECTOR, '[class="css-buzszu e1v64bz04"]')
    order_product_count = int(info[0].text.replace('총 ', ''))
    print(f'주문 상품 수 : {order_product_count}')
    return order_product_count


def save_total_order_price(wd):
    info = wd.find_elements(AppiumBy.CSS_SELECTOR, '[class="css-buzszu e1v64bz04"]')
    total_price = int(info[1].text.replace(',', ''))
    print(f'총 주문 금액 : {total_price}')
    return total_price


def save_product_name_list(wd):
    cart_product_name = []
    product = wd.find_elements(AppiumBy.CSS_SELECTOR, '[class="css-1lk9wst e1p0is0o10"]')
    for name in product:
        product_name = name.text
        cart_product_name.append(product_name)
    print(f'장바구니 상품 목록 : {cart_product_name}')
    sleep(2)
    return cart_product_name


def save_product_name(wd):
    product_name = wd.find_element(AppiumBy.CSS_SELECTOR, '[class="css-1lk9wst e1p0is0o10"]').text
    print(f'상품명 : {product_name}')
    return product_name


def save_product_price(wd):
    product_price = wd.find_element(AppiumBy.CSS_SELECTOR, '[class="css-bmeojf e1p0is0o15"]')
    product_price = int(product_price.text.replace(',', ''))
    print(f'상품 가격 : {product_price}')
    return product_price


def save_product_count(wd):
    product_count = wd.find_element(AppiumBy.CSS_SELECTOR, '[inputmode="numeric"]').get_attribute('value')
    product_count = int(product_count)
    print(f'상품 개수 : {product_count}')
    return product_count


def click_delete_product(wd):
    ialc(wd, '//div[2]/button[contains(text(), "삭제")]')
    sleep(2)


def click_add_product(wd):
    ialc(wd, '//button[contains(text(), "+")]')
    sleep(2)


def check_cart_product_list(wd, best_pdp_name, keyword_pdp_name):
    cart_product_list = save_product_name_list(wd)
    if best_pdp_name in cart_product_list and keyword_pdp_name in cart_product_list:
        print('장바구니 리스트 확인')
    else:
        print('장바구니 리스트 확인 실패')
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
