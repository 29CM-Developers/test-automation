from time import sleep
from appium.webdriver.common.appiumby import AppiumBy


def save_first_contents_title(wd):
    posts = wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            '**/XCUIElementTypeCell[`name == "recommended_post"`][1]')
    post_title = posts.find_element(AppiumBy.XPATH, 'XCUIElementTypeStaticText[2]').text
    post_title = ' '.join(post_title.split())
    return post_title


def click_first_contents(wd):
    wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeCell[`name == "recommended_post"`][1]').click()
    sleep(3)
