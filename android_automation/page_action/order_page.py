import re
from time import sleep
from appium import webdriver
from selenium.webdriver.common.by import By

import com_utils.element_control
from com_utils.element_control import aal, aalc, aals, scroll_control
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


def click_virtual_account(wd):
    sleep(2)
    virtual_account = False
    for i in range(0, 5):
        try:
            element = aal(wd, 'c_무통장입금')
            if element == None:
                scroll_control(wd, 'U', 50)
            elif element.is_displayed():
                virtual_account = True
                element.click()
                break
        except NoSuchElementException:
            print("NOSUCH")
            scroll_control(wd, 'U', 50)
            pass
    if not virtual_account:
        print('무통장 입금 옵션 미노출')


def click_all_agreement(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, 'c_동의합니다')
            if element == None:
                print("NOSUCH")
                scroll_control(wd, 'D', 50)
            elif element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            print("NOSUCH")
            scroll_control(wd, 'D', 50)
            pass


def click_payment(wd):
    aalc(wd, 'c_결제하기')


def click_virtual_account_payment(wd):
    sleep(1)
    aalc(wd, 'c_전체 동의')
    aalc(wd, 'c_토스뱅크')
    scroll_control(wd, 'D', 50)
    try:
        elements = aals(wd, 'c_다음')
        for i in range(len(elements)):
            print(f'elements[i].text : {elements[i].text}')
            if elements[i].text == '다음':
                elements[i].click()
                break
    except NoSuchElementException:
        pass
    sleep(3)


def click_delivery_order_tracking(wd):
    aalc(wd, 'c_주문조회')
    sleep(3)


def save_purchase_price(wd):
    price = ''
    for i in range(0, 5):
        try:
            element = aal(wd, 'c_결제금액')
            if element == None:
                scroll_control(wd, 'D', 100)
            else:
                if element.is_displayed():
                    parent_elements = wd.find_element(By.XPATH, f'//*[contains(@text, "결제금액")]/../..')
                    print(f'parent_elements:{parent_elements}')

                    p1 = aals(parent_elements, '//android.widget.Button')
                    print(f'p1 : {p1[0].text}')
                    price = p1[0].text.replace('원', '').replace(',', '')
                    price = int(price)
                    print(f'price : {price}')
                    break
        except NoSuchElementException:
            scroll_control(wd, 'D', 100)
            pass

    return price
def save_purchase_btn_price(wd):
    price_btn = aal(wd, 'c_결제하기').text
    price = int(price_btn.replace('원 결제하기', '').replace(',', ''))
    print(f'save_purchase_btn_price : {price}')
    return price
def save_delivery_price(wd):
    parent_elements = wd.find_element(By.XPATH, '//*[contains(@text, "결제금액")]/../..')
    com_utils.element_control.scroll_control(wd, 'D', 30)
    aalc(parent_elements, '//android.widget.Button')
    com_utils.element_control.scroll_control(wd, 'D', 100)
    # 웹뷰로 전환
    change_webview(wd)

    # 웹뷰에서 작업 수행 (예: 웹 요소 찾기, 클릭 등)
    delivery_price_parents = wd.find_element(By.XPATH, '//div[@id="__next"]/div/div[2]/aside/section/div/ul/li[4]')
    delivery_price_element = delivery_price_parents.find_elements(By.XPATH, '*')
    for i in range(len(delivery_price_element)):
        print(f'delivery_price_element : {delivery_price_element[i].text}')
        if delivery_price_element[i].text == '배송비':
            delivery_price = delivery_price_element[i + 1].text
            print(f'delivery_price : {delivery_price}')
            break
    # 배송비 문자열 숫자 변환
    delivery_price = re.sub(r'[^0-9]', '', delivery_price)
    delivery_price = int(delivery_price) if delivery_price else 0
    print(f'delivery_price : {delivery_price}')
    return delivery_price


def change_webview(wd):
    # 앱에서 웹뷰로 전환
    webview_contexts = wd.contexts  # 사용 가능한 모든 컨텍스트 가져오기
    print("Available Contexts:", webview_contexts)

    # 웹뷰로 전환
    wd.switch_to.context(webview_contexts[-1])  # 가장 최근의 웹뷰 컨텍스트로 전환
    print(f'wd.current_context : {wd.current_context}')
    print(f'wd.current_window_handle : {wd.current_window_handle}')
    print(f'wd.window_handles : {wd.window_handles}')
    print(f'len(wd.window_handles) : {len(wd.window_handles)}')
    for i in range(len(wd.window_handles) - 1, -1, -1):

        if wd.window_handles[i] != wd.current_window_handle:
            print(f'wd.window_handles[i] : {wd.window_handles[i]}')
            wd.switch_to.window(wd.window_handles[i])
            break

    print(f'wd.current_window_handle : {wd.current_window_handle}')
    print("웹뷰로 전환 성공")
    sleep(3)


def change_native(wd):
    # 네이티브로 전환
    webview_contexts = wd.contexts  # 사용 가능한 모든 컨텍스트 가져오기
    # print("Available Contexts:", webview_contexts)
    # print(f'wd.current_context : {wd.current_context}')
    # print(f'wd.current_window_handle : {wd.current_window_handle}')
    print(f'wd.window_handles : {wd.window_handles}')
    wd.switch_to.context('NATIVE_APP')
    print("네이티브 변환 성공")


def save_coupon_discount_price(wd):
    coupon_discount_price_parents = wd.find_element(By.XPATH,
                                                    '//div[@id="__next"]/div/div[2]/aside/section/div/ul/li[2]/div/div[1]')
    coupon_discount_price_element = coupon_discount_price_parents.find_elements(By.XPATH, '*')

    for i in range(len(coupon_discount_price_element)):
        print(f'coupon_discount_price_element : {coupon_discount_price_element[i].text}')
        if coupon_discount_price_element[i].text == '쿠폰 할인 금액':
            coupon_discount_price = coupon_discount_price_element[i + 1].text
            print(f'coupon_discount_price : {coupon_discount_price}')
            break

    # 쿠폰할인 문자열 숫자 변환
    coupon_discount_price = re.sub(r'[^0-9]', '', coupon_discount_price)
    coupon_discount_price = int(coupon_discount_price) if coupon_discount_price else 0
    print(f'coupon_discount_price : {coupon_discount_price}')

    # 네이티브 전환
    change_native(wd)
    return coupon_discount_price


def save_order_no(wd):
    order_no = aal(wd, 'c_주문번호 ORD').text
    order_no = re.sub(re.escape('주문번호 '), "", order_no)
    print(f'주문번호 문구 제거 후: {order_no}')
    return order_no


def check_delivery_info(wd, warning_texts):
    try:
        aal(wd, 'c_배송 정보')
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
            element = aal(wd, 'c_선물 받는 분 정보')
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
    print(f'product_name : {product_name}')
    result_string = re.sub('\[29CM 단독\]_', '', product_name)
    print(f'result_string : {result_string}')
    sleep(5)
    test_result = 'WARN'
    order_name = ''
    for i in range(0, 5):
        try:
            element = aal(wd, f'c_{result_string}')
            if element == None:
                scroll_control(wd, 'D', 50)
            else:
                order_name = element.text
                if element.is_displayed() and order_name == result_string:
                    test_result = 'PASS'
                    print('주문서 상품명 확인')
                    break
        except NoSuchElementException:
            scroll_control(wd, 'D', 50)
            pass
    if test_result == 'WARN':
        test_result = 'WARN'
        warning_texts.append('주문서 상품명 확인 실패')
        print(f'주문서 상품명 확인 실패: pdp-{product_name} / 주문서-{order_name}')
    return test_result


def check_cart_purchase_price(wd, warning_texts, pdp_price):
    order_price = save_purchase_price(wd)
    btn_price = save_purchase_btn_price(wd)
    delivery_price = save_delivery_price(wd)
    # 쿠폰할인금액
    coupon_discount_price = save_coupon_discount_price(wd)
    print(
        f'주문서 가격 확인 실패 - pdp: {pdp_price} / 배송비 : {delivery_price} / 쿠폰 할인 금액 : {coupon_discount_price} / 주문서: {order_price} / 결제 버튼 : {btn_price} ')
    compare_price = pdp_price + delivery_price - coupon_discount_price
    if order_price == compare_price and btn_price == compare_price:
        test_result = 'PASS'
        print('주문서 가격 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('주문서 가격 확인 실패')
        print(
            f'주문서 가격 확인 실패 - pdp: {pdp_price} / 배송비 : {delivery_price} / 주문서: {order_price} / 결제 버튼 : {btn_price} / 쿠폰 할인 금액 : {coupon_discount_price}')
    sleep(3)

    return test_result


def check_pdp_purchase_price(wd, warning_texts, pdp_price):
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
        print(
            f'주문서 가격 확인 실패 - pdp: {pdp_price} / 배송비 : {delivery_price} / 주문서: {order_price} / 결제 버튼 : {btn_price}')

    change_native(wd)
    sleep(5)
    return test_result


def check_inipay_page(wd):
    try:
        sleep(3)
        aal(wd, 'c_KG이니시스')
        print('이니시스 페이지 진입')
    except NoSuchElementException:
        print('이니시스 페이지 진입 실패')


def check_done_payment(wd, warning_texts):
    try:
        aal(wd, 'c_주문이 완료되었습니다.')
        test_result = 'PASS'
        print('주문 완료 페이지 확인 - 타이틀')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('주문 완료 페이지 확인 실패 - 타이틀')
        print('주문 완료 페이지 확인 실패 - 타이틀')
    return test_result
def check_payment_type(wd, warning_texts, payment_type):
    sleep(2)
    payment_info = ''
    try:
        parent_elements = wd.find_element(By.XPATH, f'//*[contains(@text, "결제방법")]/../..')
        p1 = aals(parent_elements, '//android.view.View')
        for i in range(len(p1)):
            print(f'element : {p1[i].text}')
            if p1[i].text == payment_type:
                payment_info = p1[i].text
                break
    except NoSuchElementException:
        scroll_control(wd, 'D', 100)
        pass

    if payment_info == payment_type:
        test_result = 'PASS'
        print('주문 완료 페이지 확인 - 결제방법')
    else:
        test_result = 'WARN'
        warning_texts.append('주문 완료 페이지 확인 실패 - 결제방법')
        print(f'주문 완료 페이지 확인 실패 - 결제방법 : {payment_info}')
    return test_result
