from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException

import com_utils.element_control


def enter_setting_page(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarSettingWhite').click()


def enter_login_page(wd):
    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]').click()
    sleep(3)


def find_login_btn(wd):
    for i in range(0, 5):
        try:
            element = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]')
            if element.is_displayed():
                break
        except NoSuchElementException:
            pass
        wd.execute_script('mobile:swipe', {'direction': 'down'})


def check_login_btn(wd, warning_texts):
    try:
        wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="로그인·회원가입"]')
        test_result = 'PASS'
        print('로그아웃 성공 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('로그아웃 성공 확인 실패')
        print('로그아웃 성공 확인')
    return test_result


def check_nickname(self, wd, warning_texts):
    test_result = 'WARN'
    for i in range(0, 5):
        try:
            element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, self.pconf['nickname'])
            if element.is_displayed():
                test_result = 'PASS'
                print('HOME 탭 닉네임 확인')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "U", 50)
    if test_result == 'WARN':
        warning_texts.append('HOME 탭 닉네임 확인 실패')
        print('HOME 탭 닉네임 확인 실패')
    return test_result


def check_recent_title(wd, warning_texts, type, title):
    recent_title = wd.find_element(AppiumBy.XPATH,
                                   '//XCUIElementTypeCell/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeStaticText').text
    if recent_title in title:
        test_result = 'PASS'
        print(f'최근 본 {type} 확인')
    else:
        test_result = 'WARN'
        warning_texts.append(f'최근 본 {type} 확인 실패')
        print(f'최근 본 {type} 확인 실패 : {title} / {recent_title}')
    return test_result


def expand_recent_contents(wd):
    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[6]').click()


def close_recent_contents(wd):
    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[4]').click()


def check_recent_history(wd, warning_texts, product_name, post_title):
    recent_history = []
    recent = wd.find_elements(AppiumBy.XPATH,
                              '//XCUIElementTypeCell/XCUIElementTypeTable/XCUIElementTypeCell')
    for title in recent[:2]:
        title = title.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text
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
            element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, '주문배송조회')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "U", 50)


def click_review_menu(wd):
    for i in range(0, 5):
        try:
            element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, '상품 리뷰')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)


def click_edit_user_info_menu(wd):
    for i in range(0, 5):
        try:
            element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, '회원 정보 수정')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)


def find_logout_btn(wd):
    for i in range(0, 5):
        try:
            element = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="LOGOUT"]')
            if element.is_displayed():
                break
        except NoSuchElementException:
            pass
        wd.execute_script('mobile:swipe', {'direction': 'up'})


def click_logout_btn(wd):
    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="LOGOUT"]').click()
