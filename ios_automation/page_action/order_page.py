import re
from com_utils.element_control import ial, ialc, scroll_control
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


def check_delivery_info(wd, warning_texts):
    try:
        ial(wd, 'c_배송 정보')
        test_result = 'PASS'
        print('구매하기 결제 화면 진입 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('구매하기 결제 화면 진입 확인 실패')
        print('구매하기 결제 화면 진입 확인 실패')
    return test_result


def check_receiver_info(wd, warning_texts):
    test_result = 'WARN'
    for i in range(0, 5):
        try:
            element = ial(wd, 'c_선물 받는 분 정보')
            if element.is_displayed():
                test_result = 'PASS'
                print('선물하기 결제 화면 진입 확인')
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'D', 50)
    if test_result == 'WARN':
        test_result = 'WARN'
        warning_texts.append('선물하기 결제 화면 진입 확인 실패')
        print('선물하기 결제 화면 진입 확인 실패')
    return test_result


def check_order_product_name(wd, warning_texts, product_name):
    test_result = 'WARN'
    order_name = ''
    for i in range(0, 5):
        try:
            element = ial(wd, f'c_{product_name}')
            order_name = element.text
            if element.is_displayed() and order_name == product_name:
                test_result = 'PASS'
                print('주문서 상품명 확인')
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'D', 50)
    if test_result == 'WARN':
        test_result = 'WARN'
        warning_texts.append('주문서 상품명 확인 실패')
        print(f'주문서 상품명 확인 실패: pdp-{product_name} / 주문서-{order_name}')
    return test_result


def save_purchase_price(wd):
    price = ''
    for i in range(0, 5):
        try:
            element = ial(wd, 'complementary')
            if element.is_displayed():
                price = ial(element, '//XCUIElementTypeButton[1]').text.replace('원', '').replace(',', '')
                price = int(price)
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'D', 50)
    return price


def save_purchase_btn_price(wd):
    price_btn = ial(wd, 'c_결제하기').text
    price = int(price_btn.replace('원 결제하기', '').replace(',', ''))
    return price


def save_delivery_price(wd):
    ialc(wd, '//XCUIElementTypeOther[@name="complementary"]/XCUIElementTypeButton[1]')
    delivery_price = ial(wd,
                         '//XCUIElementTypeOther[@name="complementary"]/XCUIElementTypeOther[2]/XCUIElementTypeOther[4]/XCUIElementTypeStaticText[@index="1"]').text
    delivery_price = re.findall(r'\d+', delivery_price)
    delivery_price = int(''.join(delivery_price))
    return delivery_price


def check_purchase_price(wd, warning_texts, pdp_price):
    order_price = save_purchase_price(wd)
    btn_price = save_purchase_btn_price(wd)
    delivery_price = save_delivery_price(wd)
    compare_price = pdp_price + delivery_price

    if order_price == compare_price and btn_price == compare_price:
        test_result = 'PASS'
        print('주문서 가격 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('주문서 가격 확인 실패')
        print(f'주문서 가격 확인 실패 - pdp: {pdp_price} / 배송비 : {delivery_price} / 주문서: {order_price} / 결제 버튼 : {btn_price}')
    return test_result
