import com_utils.element_control

from selenium.common import NoSuchElementException
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from com_utils.element_control import ial, ialc, ials


# welove 페이지에서 뒤로가기
def click_welove_back_btn(wd):
    ialc(wd, 'common back icon black')


def click_native_welove_back_btn(wd):
    ialc(wd, 'navi_back_btn')


# 포스트에서 welove 페이지로 뒤로가기
def click_post_to_welove_back_btn(wd):
    ialc(wd, 'common back icon black')


def click_hash_tag_back_btn(wd):
    ialc(wd, '//button[contains(@class, "css-1lwmh7z")]')


def save_first_post_title(wd):
    post_title = ials(wd, '//h3')[1].text
    return post_title


def save_native_first_post_title(wd):
    posts = wd.find_element(AppiumBy.IOS_CLASS_CHAIN,
                            '**/XCUIElementTypeCell[`name == "recommended_post"`][1]')
    post_title = posts.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[2]').text
    if '댓글' in post_title:
        post_title = posts.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[5]').text
    return post_title


def click_first_post(wd):
    ials(wd, '//h3')[1].click()
    sleep(3)


def click_native_first_post(wd):
    ialc(wd, '**/XCUIElementTypeCell[`name == "recommended_post"`][1]')
    sleep(3)


# like_post_name = 포스트 제목
def click_post_like_btn(wd):
    ialc(wd, '//button[contains(@class, "css-1w1sbu5")]')


def save_first_post_hashtag(wd):
    com_utils.element_control.scroll_control(wd, 'D', 10)
    post_hash_tag = ial(wd, '//button').text.replace('#', '')
    return post_hash_tag


def click_first_post_hashtag(wd):
    ialc(wd, '//button')
    sleep(3)


def check_hash_tag_title(wd, hash_tag):
    hash_tag_title = ial(wd, '//h3[contains(text(), "#")]').text.replace('# ', '')
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
    post_title = ials(wd, '//h3')[3].text
    find_break = False
    for i in range(0, 5):
        try:
            post = ial(wd, f'//h3[contains(text(), "{post_title}")]')
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
