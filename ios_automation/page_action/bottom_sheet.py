from time import sleep
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, tap_control


def close_bottom_sheet(wd):
    wd.implicitly_wait(1)
    try:
        ial(wd, '//XCUIElementTypeOther[@name="Title"]')
        tap_control(wd)
        print('바텀 시트 노출되어 닫기 동작')
    except NoSuchElementException:
        pass
    wd.implicitly_wait(3)


def find_icon_and_close_bottom_sheet(wd):
    ial(wd, 'navi_cart_btn')
    close_bottom_sheet(wd)


def pdp_close_bottom_sheet(wd):
    try:
        sleep(1)
        ial(wd, '//XCUIElementTypeButton[@name="다음"]')
        ial(wd, 'c_확인하세요')
        tap_control(wd)
        print('바텀 시트 노출되어 닫기 동작')
    except NoSuchElementException:
        pass
    ial(wd, 'common cart icon black')
    sleep(1)
    close_bottom_sheet(wd)
