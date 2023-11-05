from time import sleep
from appium.webdriver.common.appiumby import AppiumBy


# welove 페이지에서 뒤로가기
def click_welove_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_back_btn').click()


# 포스트에서 welove 페이지로 뒤로가기
def click_post_to_welove_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()


def save_first_post_title(wd):
    posts = wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            '**/XCUIElementTypeCell[`name == "recommended_post"`][1]')
    post_title = posts.find_element(AppiumBy.XPATH, 'XCUIElementTypeStaticText[2]').text
    print(f'포스트명 : {post_title}')
    return post_title


def click_first_post(wd):
    wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeCell[`name == "recommended_post"`][1]').click()
    sleep(3)


# like_post_name = 포스트 제목
def click_post_like_btn(wd, like_post_name):
    like_post_name = ' '.join(like_post_name.split())
    post_view = wd.find_elements(AppiumBy.XPATH,
                                 f'//XCUIElementTypeOther[@name="{like_post_name} - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeOther')
    post_view_len = len(post_view) - 1
    wd.find_element(AppiumBy.XPATH, f'//XCUIElementTypeOther[{post_view_len}]/XCUIElementTypeButton[1]').click()
