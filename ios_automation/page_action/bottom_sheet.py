from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, tap_control


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
    ial(wd, 'common cart icon black')
    close_bottom_sheet(wd)
