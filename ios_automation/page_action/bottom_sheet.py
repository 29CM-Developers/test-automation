from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


def close_bottom_sheet(wd):
    wd.implicitly_wait(1)
    try:
        wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeWindow[2]')
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '닫기').click()
        print('바텀 시트 노출되어 닫기 동작')
    except NoSuchElementException:
        wd.implicitly_wait(0)
        print('바텀 시트 미노출')
        pass
    wd.implicitly_wait(3)
