from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_back_btn').click()


def check_notification(wd, warning_texts):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '쇼핑 알림')
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '재입고 알림')
        test_result = 'PASS'
        print('설정 화면 진입 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('설정 화면 진입 확인 실패')
        print('설정 화면 진입 확인 실패')
    return test_result
