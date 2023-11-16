from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from time import sleep, time
from com_utils.element_control import aal, aalc, aals, swipe_control


def click_pin_menu(wd, find_menu):
    sleep(3)
    pin_menu_layer = aal(wd, 'com.the29cm.app29cm:id/shopComposeView')
    pin_menu_list = aal(pin_menu_layer, '//android.view.View/android.view.View[1]')
    click_break = False
    for i in range(0, 5):
        try:
            pin_menu_title = aal(wd, 'c_WELOVE')
            if pin_menu_title == None:
                swipe_control(wd, pin_menu_list, 'left', 50)
            elif pin_menu_title.text == find_menu:
                click_break = True
                sleep(2)
                pin_menu_title.click()
        except NoSuchElementException:
            swipe_control(wd, pin_menu_list, 'left', 50)
            pass
        if click_break:
            break


def click_best_category(wd):
    aalc(wd, 'best')
