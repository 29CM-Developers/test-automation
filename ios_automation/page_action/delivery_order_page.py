from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


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
