from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ialc


def click_back_btn(wd):
    ialc(wd, 'navi_back_btn')


def check_notification(wd):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '쇼핑 알림')
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '재입고 알림')
        print('설정 화면 진입 확인')
    except NoSuchElementException:
        print('설정 화면 진입 확인 실패')
        raise Exception('설정 화면 진입 확인 실패')
