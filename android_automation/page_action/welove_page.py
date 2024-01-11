from appium.webdriver.extensions.android.nativekey import AndroidKey

import com_utils.element_control
from selenium.common import NoSuchElementException
from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from com_utils.element_control import aal, aalc, aals, scroll_up_to_element_id, scroll_control, scroll_to_element_xpath


# welove 페이지에서 뒤로가기
def click_welove_back_btn(wd):
    sleep(3)
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')
    sleep(3)


def click_hash_tag_close_btn(wd):
    sleep(3)
    # 뒤로가기 버튼 시뮬레이트
    wd.press_keycode(AndroidKey.BACK)
    sleep(3)


# 포스트에서 welove 페이지로 뒤로가기
def click_post_to_welove_back_btn(wd):
    aalc(wd, 'common back icon black')


def click_hash_tag_back_btn(wd):
    sleep(3)
    # 뒤로가기 버튼 시뮬레이트
    wd.press_keycode(AndroidKey.BACK)
    sleep(3)


def save_first_post_title(wd):
    sleep(2)
    # post_title = aal(wd, 'com.the29cm.app29cm:id/txtPostTitle')
    post_title = aals(wd, '//h3')[1]
    if post_title == None:
        com_utils.element_control.scroll_control(wd, "D", 30)
    # post_title = aal(wd, 'com.the29cm.app29cm:id/txtPostTitle').text
    # post_title = aal(wd, '//div[@id="__next"]/section/section[1]/div[2]/ul/li[1]/a/div[2]/h3').text
    post_title = aals(wd, '//h3')[1].text
    print(f'포스트명 : {post_title}')
    return post_title


def save_first_post_title_for_recently_viewed(wd):
    sleep(2)
    post_title = aal(wd, 'com.the29cm.app29cm:id/txtPostTitle')
    # post_title = aal(wd, '//div[@id="__next"]/section/section[1]/div[2]/ul/li[1]/a/div[2]/h3')
    if post_title == None:
        com_utils.element_control.scroll_control(wd, "D", 30)
    post_title = aal(wd, 'com.the29cm.app29cm:id/txtPostTitle').text
    # post_title = aal(wd, '//div[@id="__next"]/section/section[1]/div[2]/ul/li[1]/a/div[2]/h3').text
    print(f'포스트명 : {post_title}')
    return post_title


def click_first_post_for_recently_viewed(wd):
    aalc(wd, 'com.the29cm.app29cm:id/txtPostTitle')
    sleep(3)


def click_first_post(wd):
    # aalc(wd, 'com.the29cm.app29cm:id/txtPostTitle')
    aalc(wd, '//div[@id="__next"]/section/section[1]/div[2]/ul/li[1]/a/div[2]/h3')
    sleep(3)


def save_first_post_hashtag(wd):
    post_hash_tag = ''
    com_utils.element_control.scroll_control(wd, 'D', 30)
    for i in range(0, 3):
        try:
            # post = aal(wd, 'com.the29cm.app29cm:id/seriesContainer')
            # first_hash_tag = aal(post,
            #                      '//android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.TextView')
            # first_hash_tag = aal(wd, '//*[@id="__next"]/section/section[1]/div[2]/ul/li[1]/div/div[1]/button')
            first_hash_tag = aal(wd, '//button')
            if first_hash_tag.is_displayed():
                post_hash_tag = first_hash_tag.text
                break
            com_utils.element_control.scroll_control(wd, 'D', 30)
        except NoSuchElementException:
            com_utils.element_control.scroll_control(wd, 'D', 30)
            pass
    return post_hash_tag


def save_first_post_hashtag_native(wd):
    post_hash_tag = ''
    com_utils.element_control.scroll_control(wd, 'D', 30)
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
            com_utils.element_control.scroll_control(wd, 'D', 30)
            pass
    return post_hash_tag


def click_first_post_hashtag(wd, post_hash_tag):
    post_hash_tag = post_hash_tag.replace('#', '')
    print(f'post_hash_tag {post_hash_tag}')
    # aalc(wd, f'c_{post_hash_tag}')
    # aalc(wd, f'//button[@data-series-title="{post_hash_tag}"')
    # aalc(wd, '//*[@id="__next"]/section/section[1]/div[2]/ul/li[1]/div/div[1]/button')
    # com_utils.element_control.scroll_control(wd, 'D', 30)
    aalc(wd, '//button')
    sleep(5)


def click_first_post_hashtag_native(wd, post_hash_tag):
    com_utils.element_control.scroll_control(wd, 'D', 30)
    after_post_hash_tag = post_hash_tag.replace('#', '')
    print(f'post_hash_tag {after_post_hash_tag}')
    print(f'post_hash_tag {post_hash_tag}')
    # aalc(wd, f'c_{post_hash_tag}')
    aalc(wd, f"//*[contains(@text, '{post_hash_tag}')]")
    # aalc(wd, f'//button[@data-series-title="{post_hash_tag}"')
    # aalc(wd, '//*[@id="__next"]/section/section[1]/div[2]/ul/li[1]/div/div[1]/button')
    # com_utils.element_control.scroll_control(wd, 'D', 30)
    # aalc(wd, '//button')
    sleep(5)


def check_hash_tag_title(wd, hash_tag):
    print(f"check_hash_tag_title : {hash_tag}")
    sleep(2)
    # hash_tag_title = aal(wd, hash_tag).text
    # hash_tag_title = aal(wd, '//div[@id="__next"]/section/section[1]/div[2]/ul/li[1]/div[2]/div/h3').text
    hash_tag_title = aal(wd, '//h3[contains(text(), "#")]').text
    hash_tag_title = hash_tag_title.replace('# ', '')
    hash_tag_title = hash_tag_title.replace('#', '')
    hash_tag = hash_tag.replace('#', '')
    print(f"check_hash_tag_title : {hash_tag_title}")
    if hash_tag_title == hash_tag:
        print('포스트 해시태그 확인')
    else:
        print(f'포스트 해시태그 확인 실패 : {hash_tag} / {hash_tag_title}')
        raise Exception('포스트 해시태그 확인 실패')

def check_hash_tag_post(wd, post_title):
    tag_break = False
    for i in range(0, 5):
        # post = aal(wd, post_title)
        # post = aal(wd, '//div[@id="__next"]/section/section[1]/div[2]/ul/li[1]/div[2]/div/ul/li[1]/a/div[2]/h1')
        post = aal(wd, f'//h1[contains(text(), "{post_title}")]')
        if post == None:
            pass
        elif post.is_displayed():
            print(f'post : {post.text}')
            tag_break = True
            print('포스트 해시태그 확인 - 페이지 내 포스트')
            break
        com_utils.element_control.scroll_control(wd, "D", 30)
    if not tag_break:
        print('포스트 해시태그 확인 실패 - 포스트 타이틀')
        raise Exception('포스트 해시태그 확인 실패 - 포스트 타이틀')


def find_and_save_third_post(wd):
    find_break = False
    com_utils.element_control.scroll_control(wd, "D", 40)
    sleep(2)
    for i in range(0, 5):
        # post_layer = aal(wd, 'com.the29cm.app29cm:id/weloveRecyclerView')
        # post = aal(post_layer,
        #            "//android.widget.LinearLayout[3]/android.widget.RelativeLayout/android.widget.TextView[1]")
        post = aal(wd, '//*[@id="__next"]/section/section[1]/div[2]/ul/li[3]/a/div[2]/h3')
        if post == None:
            com_utils.element_control.scroll_control(wd, "D", 40)
            sleep(2)
            # post_layer = aal(wd, 'com.the29cm.app29cm:id/weloveRecyclerView')
            # post = aal(post_layer,
            #            "//android.widget.LinearLayout[3]/android.widget.RelativeLayout/android.widget.TextView[1]")
            post = aal(wd, '//*[@id="__next"]/section/section[1]/div[2]/ul/li[3]/a/div[2]/h3')
        if post.is_displayed():
            find_break = True
            print(f'포스트 추가 노출 확인 : {post.text}')
            break
        com_utils.element_control.scroll_control(wd, "D", 40)
    if not find_break:
        print('포스트 추가 노출 확인 실패')
        raise Exception('포스트 추가 노출 확인 실패')
