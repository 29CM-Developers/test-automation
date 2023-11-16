from appium.webdriver.extensions.android.nativekey import AndroidKey

import com_utils.element_control
from selenium.common import NoSuchElementException
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from com_utils.element_control import aal, aalc, scroll_up_to_element_id, scroll_control, scroll_to_element_xpath


# welove 페이지에서 뒤로가기
def click_welove_back_btn(wd):
    sleep(3)
    # 뒤로가기 버튼 시뮬레이트
    wd.press_keycode(AndroidKey.BACK)
    sleep(3)


# 포스트에서 welove 페이지로 뒤로가기
def click_post_to_welove_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()


def click_hash_tag_back_btn(wd):
    sleep(3)
    # 뒤로가기 버튼 시뮬레이트
    wd.press_keycode(AndroidKey.BACK)
    sleep(3)


def save_first_post_title(wd):
    post_title = aal(wd, 'com.the29cm.app29cm:id/txtPostTitle').text
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
            post = aal(wd, 'com.the29cm.app29cm:id/seriesContainer')
            first_hash_tag = aal(post,
                                 '//android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.TextView')
            if first_hash_tag.is_displayed():
                post_hash_tag = first_hash_tag.text
                break
            com_utils.element_control.scroll_control(wd, 'D', 30)
        except NoSuchElementException:
            pass
    return post_hash_tag


def click_first_post_hashtag(wd, post_hash_tag):
    aalc(wd, f'c_{post_hash_tag}')
    sleep(4)


def check_hash_tag_title(wd, warning_texts, hash_tag):
    print("check_hash_tag_title")
    hash_tag_title = aal(wd, hash_tag).text
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
            post = aal(wd, post_title)
            print(f'post : {post}')
            if post == None:
                com_utils.element_control.scroll_control(wd, "D", 30)
            elif post.is_displayed():
                test_result = 'PASS'
                print('포스트 해시태그 확인 - 페이지 내 포스트')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 30)
    if test_result == 'WARN':
        test_result = 'WARN'
        warning_texts.append('포스트 해시태그 확인 실패 - 포스트 타이틀')
        print('포스트 해시태그 확인 실패 - 포스트 타이틀')
    return test_result


def find_and_save_third_post(wd, warning_texts):
    test_result = 'WARN'
    com_utils.element_control.scroll_control(wd, "D", 40)
    sleep(2)
    try:
        post_layer = aal(wd, 'com.the29cm.app29cm:id/weloveRecyclerView')
        post = aal(post_layer,
                   "//android.widget.LinearLayout[3]/android.widget.RelativeLayout/android.widget.TextView[1]")
        print(f'post : {post}')
        if post == None:
            com_utils.element_control.scroll_control(wd, "D", 40)
            sleep(2)
            post_layer = aal(wd, 'com.the29cm.app29cm:id/weloveRecyclerView')
            post = aal(post_layer,
                       "//android.widget.LinearLayout[3]/android.widget.RelativeLayout/android.widget.TextView[1]")
        if post.is_displayed():
            test_result = 'PASS'
            print(f'포스트 추가 노출 확인 : {post.text}')
    except NoSuchElementException:
        pass
    if test_result == 'WARN':
        warning_texts.append('포스트 추가 노출 확인 실패')
        print('포스트 추가 노출 확인 실패')
    return test_result
