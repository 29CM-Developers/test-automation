import os
import re
from time import sleep

from com_utils.api_control import my_order_status, my_order_cancel
from com_utils.element_control import ial, ialc, scroll_control
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


def check_delivery_info(wd):
    try:
        ial(wd, 'c_배송 정보')
        print('구매하기 결제 화면 진입 확인')
    except NoSuchElementException:
        print('구매하기 결제 화면 진입 확인 실패')
        raise Exception('구매하기 결제 화면 진입 확인 실패')


def check_receiver_info(wd):
    info_break = False
    for i in range(0, 5):
        try:
            element = ial(wd, 'c_선물 받는 분 정보')
            if element.is_displayed():
                info_break = True
                print('선물하기 결제 화면 진입 확인')
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'D', 50)
    if not info_break:
        print('선물하기 결제 화면 진입 확인 실패')
        raise Exception('선물하기 결제 화면 진입 확인 실패')


def check_order_product_name(wd, product_name):
    name_break = False
    order_name = ''
    for i in range(0, 5):
        try:
            element = ial(wd, f'c_{product_name}')
            order_name = element.text
            if element.is_displayed() and order_name == product_name:
                name_break = True
                print('주문서 상품명 확인')
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'D', 50)
    if not name_break:
        print(f'주문서 상품명 확인 실패: pdp-{product_name} / 주문서-{order_name}')
        raise Exception('주문서 상품명 확인 실패')


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


def save_coupon_price(wd):
    coupon_price = ial(wd,
                       '//XCUIElementTypeOther[@name="complementary"]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeStaticText[@index="1"]').text
    coupon_price = re.findall(r'\d+', coupon_price)
    coupon_price = int(''.join(coupon_price))
    return coupon_price


def check_purchase_price(wd, pdp_price):
    order_price = save_purchase_price(wd)
    btn_price = save_purchase_btn_price(wd)
    delivery_price = save_delivery_price(wd)
    compare_price = pdp_price + delivery_price

    if order_price == compare_price and btn_price == compare_price:
        print('주문서 가격 확인')
    else:
        print(f'주문서 가격 확인 실패 - pdp: {pdp_price} / 비교 : {compare_price} / 주문서: {order_price} / 결제 버튼 : {btn_price}')
        raise Exception('주문서 가격 확인 실패')


def check_cart_purchase_price(wd, cart_price):
    order_price = save_purchase_price(wd)
    btn_price = save_purchase_btn_price(wd)
    delivery_price = save_delivery_price(wd)
    coupon_price = save_coupon_price(wd)
    compare_price = cart_price + delivery_price - coupon_price

    if order_price == compare_price and btn_price == compare_price:
        print('주문서 가격 확인')
    else:
        print(f'주문서 가격 확인 실패 - cart: {cart_price} / 비교 : {compare_price} / 주문서: {order_price} / 결제 버튼 : {btn_price}')
        raise Exception('주문서 가격 확인 실패')


def click_virtual_account(wd):
    virtual_account = False
    for i in range(0, 5):
        try:
            element = ial(wd, '//XCUIElementTypeButton[@name="무통장입금"]')
            if element.is_displayed():
                virtual_account = True
                element.click()
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'U', 50)
    if not virtual_account:
        print('무통장 입금 옵션 미노출')


def click_hyundai_card(wd):
    virtual_account = False
    for i in range(0, 5):
        try:
            element = ial(wd, 'c_현대카드 X PIN PAY')
            if element.is_displayed():
                virtual_account = True
                element.click()
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'U', 50)
    if not virtual_account:
        print('현대카드 X PIN PAY 옵션 미노출')


def click_all_agreement(wd):
    for i in range(0, 5):
        try:
            element = ial(wd, 'c_동의합니다')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'D', 50)


def click_payment(wd):
    ialc(wd, 'c_결제하기')
    sleep(5)


def check_inipay_page(wd):
    try:
        sleep(2)
        ial(wd, '//XCUIElementTypeOther[@name="INIpay Mobile"]')
        print('이니시스 페이지 진입')
    except NoSuchElementException:
        print('이니시스 페이지 진입 실패')


def click_virtual_account_payment(wd):
    ialc(wd, '//XCUIElementTypeOther[@name="전체 동의"]')
    ialc(wd, 'c_토스뱅크')
    for i in range(0, 3):
        try:
            element = ial(wd, '//XCUIElementTypeButton[@name="다음"]')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'D', 50)
    sleep(3)


def check_pinpay_page(wd):
    try:
        sleep(5)
        ial(wd, '//XCUIElementTypeStaticText[@name="PIN Pay"]')
        print('Pin Pay 페이지 진입')
    except NoSuchElementException:
        print('Pin Pay 페이지 진입 실패')


def click_pinpay_payment(wd):
    ialc(wd, '//XCUIElementTypeStaticText[@name="무신사 현대카드"]')
    ialc(wd, 'c_결제하기')
    sleep(3)


def check_done_payment(wd):
    sleep(3)
    try:
        ial(wd, '//XCUIElementTypeStaticText[@name="주문이 완료되었습니다."]')
        print('주문 완료 페이지 확인 - 타이틀')
    except NoSuchElementException:
        print('주문 완료 페이지 확인 실패 - 타이틀')
        raise Exception('주문 완료 페이지 확인 실패 - 타이틀')


def save_order_no(wd):
    order_no = ial(wd, 'c_ORD').text
    print(f'주문번호 : {order_no}')
    return order_no


def check_payment_type(wd, payment_type):
    payment_info = ''
    for i in range(0, 3):
        try:
            element = ial(wd, '//XCUIElementTypeOther[@name="결제정보"]')
            if element.is_displayed():
                index = int(element.get_attribute('index'))
                payment_info = ial(wd,
                                   f'//XCUIElementTypeOther[@index="{index + 2}"]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeStaticText').text
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'D', 50)

    if payment_info == payment_type:
        print('주문 완료 페이지 확인 - 결제방법')
    else:
        print(f'주문 완료 페이지 확인 실패 - 결제방법 : {payment_info}')
        raise Exception('주문 완료 페이지 확인 실패 - 결제방법')


def click_delivery_order_tracking(wd):
    ialc(wd, '//XCUIElementTypeStaticText[@name="주문조회"]')
    sleep(1)


def check_api_order_cancel(self, order_no):
    order_status = my_order_status(self.pconf['id_29cm'], self.pconf['password_29cm'], order_no)
    if order_status != '전체취소':
        my_order_cancel(self.pconf['id_29cm'], self.pconf['password_29cm'], order_no)
        print('주문 취소 완료')
        sleep(2)
    elif order_status == '전체취소':
        print('주문 취소 최종 확인')
    else:
        print('주문 취소 최종 확인 실패')


def finally_order_cancel(self, order_no):
    if order_no:
        check_api_order_cancel(self, order_no)
    else:
        print('주문 전 Fail로 order_no 미존재')
