from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


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
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, self.pconf['nickname'])
        test_result = 'PASS'
        print("이메일 로그인 성공 확인")
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('이메일 로그인 성공 확인 실패')
        print("이메일 로그인 성공 확인 실패")
    return test_result


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
