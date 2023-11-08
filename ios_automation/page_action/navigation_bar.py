from appium.webdriver.common.appiumby import AppiumBy
from ios_automation.page_action.bottom_sheet import close_bottom_sheet
from com_utils.element_control import ialc


def move_to_home(wd):
    ialc(wd, '**/XCUIElementTypeButton[`label == "HOME"`]')
    close_bottom_sheet(wd)


def move_to_category(wd):
    ialc(wd, '**/XCUIElementTypeButton[`label == "CATEGORY"`]')


def move_to_search(wd):
    ialc(wd, '**/XCUIElementTypeButton[`label == "SEARCH"`]')


def move_to_like(wd):
    ialc(wd, '**/XCUIElementTypeButton[`label == "LIKE"`]')


def move_to_my(wd):
    ialc(wd, '**/XCUIElementTypeButton[`label == "MY"`]')
