from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException

from com_utils.element_control import ial, ialc, ials, swipe_control


def click_pin_menu(wd, find_menu):
    pin_menu_list = ial(wd, '//XCUIElementTypeOther[2]/XCUIElementTypeCollectionView')
    click_break = False
    for i in range(0, 5):
        try:
            pin_menu = ials(wd, '//XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell')
            for pin in pin_menu:
                pin_menu_title = ial(pin, '//XCUIElementTypeOther/XCUIElementTypeStaticText')
                if pin_menu_title.text == find_menu:
                    click_break = True
                    pin_menu_title.click()
            swipe_control(wd, pin_menu_list, 'left', 30)
        except NoSuchElementException:
            pass
        if click_break:
            break


def click_best_category(wd):
    ialc(wd, 'best')
