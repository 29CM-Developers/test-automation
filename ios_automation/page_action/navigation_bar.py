from appium.webdriver.common.appiumby import AppiumBy
from ios_automation.page_action.bottom_sheet import find_icon_and_close_bottom_sheet, close_bottom_sheet
from com_utils.element_control import ialc
from ios_automation.page_action import like_page


def move_to_home(wd):
    ialc(wd, '**/XCUIElementTypeButton[`label == "HOME"`]')
    find_icon_and_close_bottom_sheet(wd)


def move_to_category(wd):
    ialc(wd, '**/XCUIElementTypeButton[`label == "CATEGORY"`]')
    find_icon_and_close_bottom_sheet(wd)


def move_to_search(wd):
    ialc(wd, '**/XCUIElementTypeButton[`label == "SEARCH"`]')
    close_bottom_sheet(wd)


def move_to_like(wd):
    ialc(wd, '**/XCUIElementTypeButton[`label == "LIKE"`]')
    close_bottom_sheet(wd)
    like_page.close_noti_bottom_sheet(wd)
    like_page.close_brand_recommended_page(wd)


def move_to_my(wd):
    ialc(wd, '**/XCUIElementTypeButton[`label == "MY"`]')
    find_icon_and_close_bottom_sheet(wd)
