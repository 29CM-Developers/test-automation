import com_utils.element_control

from selenium.common import NoSuchElementException
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from com_utils.element_control import ial, ialc, ials
from ios_automation.page_action import context_change


# welove 페이지에서 뒤로가기
def click_welove_back_btn(wd):
    ialc(wd, 'c_ack')


# 포스트에서 welove 페이지로 뒤로가기
def click_post_to_welove_back_btn(wd):
    ialc(wd, 'common back icon black')


def click_hash_tag_back_btn(wd):
    ialc(wd, '//*[@id="hash_tag_close_btn"]')


def save_first_post_title(wd):
    if 'WEBVIEW' in wd.current_context:
        post_title = ial(wd, '//*[@id="first_post_title"]').text
    else:
        posts = ials(wd,
                     '//XCUIElementTypeStaticText[@name="Recommended Post"]/preceding-sibling::XCUIElementTypeStaticText')
        post_title = posts[len(posts) - 2].text
    return post_title


def click_first_post(wd):
    if 'WEBVIEW' in wd.current_context:
        ialc(wd, '//*[@id="first_post_title"]')
    else:
        ialc(wd, '**/XCUIElementTypeCell[`name == "recommended_post"`][1]')
    sleep(3)


# like_post_name = 포스트 제목
def click_post_like_btn(wd):
    context_change.switch_context(wd, 'webview')
    ialc(wd, '//button[contains(@class, "css-1w1sbu5")]')


def save_first_post_hashtag(wd):
    com_utils.element_control.scroll_control(wd, 'D', 10)
    post_hash_tag = ial(wd, '//*[@id="first_post_hash_tag"]').text.replace('#', '')
    return post_hash_tag


def click_first_post_hashtag(wd):
    ialc(wd, '//*[@id="first_post_hash_tag"]')
    sleep(3)


def check_hash_tag_title(wd, hash_tag):
    hash_tag_title = ial(wd, '//*[@id="hash_tag_title"]').text.replace('# ', '')
    if hash_tag_title == hash_tag:
        print('포스트 해시태그 확인')
    else:
        print(f'포스트 해시태그 확인 실패 : {hash_tag} / {hash_tag_title}')
        raise Exception('포스트 해시태그 확인 실패')


def check_hash_tag_post(wd, post_title):
    tag_break = False
    for i in range(0, 5):
        try:
            post = ial(wd, f'//h1[contains(text(), "{post_title}")]')
            if post.is_displayed():
                tag_break = True
                print('포스트 해시태그 확인 - 페이지 내 포스트')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)
    if not tag_break:
        print('포스트 해시태그 확인 실패 - 포스트 타이틀')
        raise Exception('포스트 해시태그 확인 실패 - 포스트 타이틀')


def find_and_save_third_post(wd):
    post_title = ial(wd, '//*[@id="third_post_title"]').text
    find_break = False
    for i in range(0, 5):
        try:
            post = ial(wd, f'//*[contains(text(), "{post_title}")]')
            if post.is_displayed():
                find_break = True
                print('포스트 추가 노출 확인')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 40)
    if not find_break:
        print('포스트 추가 노출 확인 실패')
        raise Exception('포스트 추가 노출 확인 실패')
