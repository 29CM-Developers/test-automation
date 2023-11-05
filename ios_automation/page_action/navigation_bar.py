from appium.webdriver.common.appiumby import AppiumBy
from ios_automation.page_action.bottom_sheet import close_bottom_sheet


def move_to_home(wd):
    wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "HOME"`]').click()
    close_bottom_sheet(wd)
