from appium.webdriver.common.appiumby import AppiumBy
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from com_utils.element_control import aalc


def move_to_home(wd):
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
