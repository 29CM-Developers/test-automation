from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="common back icon black"]').click()


def check_no_reviews_available(wd, test_result, warning_texts):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '아직 리뷰를 작성할 수 있는')
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '주문내역이 없습니다.')
        print("주문 건이 없을 경우, 상품 리뷰 확인 - 작성 가능 리뷰")
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('주문 건이 없을 경우, 상품 리뷰 확인 실패')
        print("주문 건이 없을 경우, 상품 리뷰 확인 실패 - 작성 가능 리뷰")
    return test_result


def click_my_review_tab(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, '내 리뷰 (').click()


def check_no_written_reviews(wd, test_result, warning_texts):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '작성한 리뷰가 없습니다.')
        print("주문 건이 없을 경우, 상품 리뷰 확인 - 내 리뷰")
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('주문 건이 없을 경우, 상품 리뷰 확인 실패')
        print("주문 건이 없을 경우, 상품 리뷰 확인 실패 - 내 리뷰")
    return test_result
