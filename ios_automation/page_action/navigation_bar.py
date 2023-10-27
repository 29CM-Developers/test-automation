from appium.webdriver.common.appiumby import AppiumBy


def move_to_home(wd):
    wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "HOME"`]').click()
