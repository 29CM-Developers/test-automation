from time import sleep
import re
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc, scroll_control, aals
from android_automation.page_action import bottom_sheet


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


def check_no_delivery_order(wd, warning_texts):
    try:
        aal(wd, 'c_주문내역이 없습니다')
        test_result = 'PASS'
        print("주문 건이 없을 경우, 주문 배송 조회 확인")
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('주문 건이 없을 경우, 주문 배송 조회 확인 실패')
        print("주문 건이 없을 경우, 주문 배송 조회 확인 실패")
    return test_result


def check_delivery_order(wd, order_no):
    try:
        aalc(wd, f'c_{order_no}')
        sleep(3)
        print('주문 배송 조회 확인 - 주문번호')
    except NoSuchElementException:
        print('주문 배송 조회 확인 실패 - 주문번호')
        raise Exception('주문 배송 조회 확인 실패 - 주문번호')


def check_order_detail_price(wd, payment_type, order_price):
    for i in range(0, 3):
        element = aal(wd, f'c_{payment_type}')
        if element == None:
            scroll_control(wd, 'D', 50)
        elif element.is_displayed():
            break
    find_element = wd.find_element(AppiumBy.XPATH, f'//*[contains(@text, "{payment_type}")]/../..')
    p1 = aals(find_element, '//android.widget.TextView')
    for j in range(len(p1)):
        print(f'element : {p1[j].text}')
        if p1[j].text == '결제금액':
            price = p1[j + 1].text
            price = re.sub(r'[^0-9]', '', price)
            price = int(price)
            break

    if price == order_price:
        print('주문 상세 내역 확인 - 결제금액')
    else:
        print(f'주문 상세 내역 확인 실패 - 결제금액 : 주문서-{order_price} / 주문 내역-{price}')
        raise Exception('주문 상세 내역 확인 실패 - 결제금액')


def click_order_cancel_btn(wd):
    aalc(wd, 'c_취소접수')
    sleep(3)
    aalc(wd, 'c_취소접수 완료하기')
    sleep(3)


def check_order_cancel(wd):
    try:
        aal(wd, 'c_주문 취소가 완료되었습니다.')
        print('주문 취소 완료 확인')
    except NoSuchElementException:
        print('주문 취소 완료 확인 실패')
        raise Exception('주문 취소 완료 확인 실패')


def click_move_to_home(wd):
    aalc(wd, 'c_홈으로 가기')
    bottom_sheet.close_bottom_sheet(wd)
