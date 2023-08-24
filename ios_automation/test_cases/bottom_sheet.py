import sys

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


def test_bottom_sheet(wd):
    test_name = sys._getframe().f_code.co_name
    print(f'[{test_name}] 테스트 시작')

    try:
        wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeWindow[2]')
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '닫기').click()
        print('바텀 시트 노출되어 닫기 동작')

    except NoSuchElementException:
        print('바텀 시트 미노출')
        pass
