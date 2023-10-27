from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


def save_product_name(wd):
    pdp_web = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView')
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'Select a slide to show')
        product_name = pdp_web.find_element(AppiumBy.XPATH,
                                            '//XCUIElementTypeOther[@index="5"]/XCUIElementTypeStaticText').get_attribute(
            'name')
    except NoSuchElementException:
        product_name = pdp_web.find_element(AppiumBy.XPATH,
                                            '//XCUIElementTypeOther[@index="4"]/XCUIElementTypeStaticText').get_attribute(
            'name')
    return product_name
