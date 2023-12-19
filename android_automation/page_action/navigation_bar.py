from appium.webdriver.common.appiumby import AppiumBy
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from android_automation.page_action.select_category_page import test_select_category
from com_utils.element_control import aalc
from time import sleep


def move_to_home(wd):
    sleep(1)
    aalc(wd, 'HOME')
    close_bottom_sheet(wd)


def move_to_category(wd):
    aalc(wd, 'CATEGORY')


def move_to_search(wd):
    aalc(wd, 'SEARCH')


def move_to_like(wd):
    aalc(wd, 'LIKE')


def move_to_my(wd):
    aalc(wd, 'MY')


def move_to_cart(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgCart')


def logout_and_move_to_home(wd):
    sleep(1)
    aalc(wd, 'HOME')
    test_select_category(wd)
    close_bottom_sheet(wd)
