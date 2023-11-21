from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, scroll_control
from ios_automation.page_action import bottom_sheet


def click_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()


def check_no_delivery_order(wd, warning_texts):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '주문내역이 없습니다')
        test_result = 'PASS'
        print("주문 건이 없을 경우, 주문 배송 조회 확인")
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('주문 건이 없을 경우, 주문 배송 조회 확인 실패')
        print("주문 건이 없을 경우, 주문 배송 조회 확인 실패")
    return test_result


def check_delivery_order(wd, warning_texts, order_no):
    try:
        order_no = ial(wd, f'c_{order_no}')
        order_no.click()
        sleep(2)
        test_result = 'PASS'
        print('주문 배송 조회 확인 - 주문번호')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('주문 배송 조회 확인 실패 - 주문번호')
        print('주문 배송 조회 확인 실패 - 주문번호')
    return test_result


def check_order_detail_price(wd, warning_texts, payment_type, order_price):
    for i in range(0, 3):
        try:
            element = ial(wd, f'c_{payment_type}')
            if element.is_displayed():
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, 'D', 50)

    find_element = wd.find_elements(AppiumBy.XPATH, f'//*[contains(@label, "{payment_type}")]/../..')
    price = find_element[0].find_element(AppiumBy.XPATH, '//XCUIElementTypeOther[2]/XCUIElementTypeStaticText').text
    price = int(price.replace(',', ''))

    if price == order_price:
        test_result = 'PASS'
        print('주문 상세 내역 확인 - 결제금액')
    else:
        test_result = 'WARN'
        warning_texts.append('주문 상세 내역 확인 실패 - 결제금액')
        print(f'주문 상세 내역 확인 실패 - 결제금액 : 주문서-{order_price} / 주문 내역-{price}')
    return test_result


def click_order_cancel_btn(wd):
    ialc(wd, '//XCUIElementTypeButton[@name="취소접수"]')
    sleep(3)
    ialc(wd, '//XCUIElementTypeButton[@name="취소접수 완료하기"]')
    sleep(3)


def check_order_cancel(wd, warning_texts):
    try:
        ial(wd, '//XCUIElementTypeStaticText[@name="주문 취소가 완료되었습니다."]')
        test_result = 'PASS'
        print('주문 취소 완료 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('주문 취소 완료 확인 실패')
        print('주문 취소 완료 확인 실패')
    return test_result


def click_move_to_home(wd):
    ialc(wd, '//XCUIElementTypeStaticText[@name="홈으로 가기"]')
    bottom_sheet.find_icon_and_close_bottom_sheet(wd)
