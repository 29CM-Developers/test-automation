from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc, aals

import com_utils.element_control


def check_recent_title(wd, warning_texts, type, title):
    recent_title = aal(wd, 'com.the29cm.app29cm:id/txtHistoryTitle').text
    print(f"recent_title : {recent_title} ")
    if recent_title in title:
        test_result = 'PASS'
        print(f'최근 본 {type} 확인')
    else:
        test_result = 'WARN'
        warning_texts.append(f'최근 본 {type} 확인 실패')
        print(f'최근 본 {type} 확인 실패 : {title} / {recent_title}')
    return test_result


def expand_recent_contents(wd, post_title):
    aalc(wd, f'c_{post_title}')


def close_recent_contents(wd):
    aalc(wd, 'com.the29cm.app29cm:id/pullUpLayout')


def check_recent_history(wd, warning_texts, product_name, post_title):
    recent_history = []
    sleep(2)
    recent = aals(wd, '//android.widget.TextView[@resource-id="com.the29cm.app29cm:id/txtHistoryTitle"]')
    if recent == None:
        print("못찾앗음")
    else:
        print(f'recent : {recent[0].text}')
    for i in range(2):
        title = recent[i].text
        recent_history.append(title)
    print(f'히스토리 : {recent_history}')

    if product_name in recent_history and post_title in recent_history:
        test_result = 'PASS'
        print('최근 본 컨텐츠 히스토리 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('최근 본 컨텐츠 히스토리 확인 실패')
        print(f'최근 본 컨텐츠 히스토리 확인 실패: {product_name} / {post_title} / {recent_history}')
    return test_result


def click_delivery_order_menu(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, '주문배송조회')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "U", 50)


def click_review_menu(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, '상품 리뷰')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)


def click_edit_user_info_menu(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, '회원 정보 수정')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)


def click_coupon_menu(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, '쿠폰')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)


def find_logout_btn(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, 'LOGOUT')
            if element.is_displayed():
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)


def click_logout_btn(wd):
    aalc(wd, 'LOGOUT')
