import com_utils.element_control

from selenium.common import NoSuchElementException
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from com_utils.element_control import ial, ialc


# welove 페이지에서 뒤로가기
def click_welove_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'navi_back_btn').click()


# 포스트에서 welove 페이지로 뒤로가기
def click_post_to_welove_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()


def click_hash_tag_back_btn(wd):
    ialc(wd, 'common close icon black')


def save_first_post_title(wd):
    posts = wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            '**/XCUIElementTypeCell[`name == "recommended_post"`][1]')
    post_title = posts.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[2]').text
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


def save_first_post_hashtag(wd):
    post_hash_tag = ''
    for i in range(0, 3):
        try:
            post = wd.find_element(AppiumBy.XPATH, '(//XCUIElementTypeCell[@name="recommended_post"])[1]')
            first_hash_tag = post.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[1]')
            if first_hash_tag.is_displayed():
                post_hash_tag = post.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[1]').text
                break
            com_utils.element_control.scroll_control(wd, 'D', 30)
        except NoSuchElementException:
            pass
    return post_hash_tag


def click_first_post_hashtag(wd):
    post = wd.find_element(AppiumBy.XPATH, '(//XCUIElementTypeCell[@name="recommended_post"])[1]')
    post.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[1]').click()


def check_hash_tag_title(wd, warning_texts, hash_tag):
    hash_tag_title = ial(wd, '//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText').text
    if hash_tag_title == hash_tag:
        test_result = 'PASS'
        print('포스트 해시태그 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('포스트 해시태그 확인 실패')
        print(f'포스트 해시태그 확인 실패 : {hash_tag} / {hash_tag_title}')
    return test_result


def check_hash_tag_post(wd, warning_texts, post_title):
    test_result = 'WARN'
    for i in range(0, 5):
        try:
            post = ial(wd, post_title)
            if post.is_displayed():
                test_result = 'PASS'
                print('포스트 해시태그 확인 - 페이지 내 포스트')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)
    if test_result == 'WARN':
        test_result = 'WARN'
        warning_texts.append('포스트 해시태그 확인 실패 - 포스트 타이틀')
        print('포스트 해시태그 확인 실패 - 포스트 타이틀')
    return test_result


def find_and_save_third_post(wd, warning_texts):
    post_title = ial(wd, '(//XCUIElementTypeCell[@name="recommended_post"])[3]/XCUIElementTypeStaticText[2]').text
    print(post_title)
    test_result = 'WARN'
    for i in range(0, 5):
        try:
            post = ial(wd, post_title)
            if post.is_displayed():
                test_result = 'PASS'
                print('포스트 추가 노출 확인')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 40)
    if test_result == 'WARN':
        warning_texts.append('포스트 추가 노출 확인 실패')
        print('포스트 추가 노출 확인 실패')
    return test_result
