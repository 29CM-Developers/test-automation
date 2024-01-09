from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc, aals

import com_utils.element_control

def enter_login_page(wd):
    # 로그인 회원가입 버튼 선택
    aalc(wd, 'com.the29cm.app29cm:id/txtLogin')
    print("로그인 버튼 선택")
    sleep(3)


def check_recent_title(wd, type, title):
    recent_title = aal(wd, 'com.the29cm.app29cm:id/txtHistoryTitle').text
    print(f"recent_title : {recent_title} ")
    if recent_title in title:
        print(f'최근 본 {type} 확인')
    else:
        print(f'최근 본 {type} 확인 실패 : {title} / {recent_title}')
        raise Exception(f'최근 본 {type} 확인 실패')


def expand_recent_contents(wd, post_title):
    sleep(1)
    aalc(wd, f'c_{post_title}')


def close_recent_contents(wd):
    aalc(wd, 'com.the29cm.app29cm:id/pullUpLayout')


def check_recent_history(wd, product_name, post_title):
    recent_history = []
    sleep(2)
    recent = aals(wd, '//android.widget.TextView[@resource-id="com.the29cm.app29cm:id/txtHistoryTitle"]')
    if recent == None:
        print("못찾앗음")
    else:
        print(f'recent : {recent[0].text}')
    for i in range(2):
        title = recent[i].text
        recent_history.append(title)
    print(f'히스토리 : {recent_history}')

    if product_name in recent_history and post_title in recent_history:
        print('최근 본 컨텐츠 히스토리 확인')
    else:
        print(f'최근 본 컨텐츠 히스토리 확인 실패 : {product_name} / {post_title}')
        raise Exception(f'최근 본 컨텐츠 히스토리 확인 실패')


def click_delivery_order_menu(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, '주문배송조회')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "U", 50)


def click_review_menu(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, 'c_상품 리뷰')
            if element == None:
                com_utils.element_control.scroll_control(wd, "D", 30)
            elif element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)


def click_edit_user_info_menu(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, 'c_회원 정보 수정')
            if element == None:
                com_utils.element_control.scroll_control(wd, "D", 30)
            elif element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 30)


def click_coupon_menu(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, '쿠폰')
            if element.is_displayed():
                element.click()
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)


def find_logout_btn(wd):
    for i in range(0, 10):
        try:
            element = aal(wd, 'com.the29cm.app29cm:id/btnLogout')
            if element == None:
                com_utils.element_control.scroll_control(wd, "D", 50)
            elif element.is_displayed():
                com_utils.element_control.scroll_control(wd, "D", 20)
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)


def find_login_btn(wd):
    for i in range(0, 5):
        try:
            element = aal(wd, 'com.the29cm.app29cm:id/txtLogin')
            if element == None:
                com_utils.element_control.scroll_control(wd, "U", 40)
            if element.is_displayed():
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "U", 40)

def click_logout_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/btnLogout')
    sleep(2)


def check_nickname(self, wd):
    # 로그인 성공 진입 확인
    login_name = aal(wd, 'com.the29cm.app29cm:id/txtUserName')
    if login_name.text == self.pconf['MASKING_NAME']:
        print("로그인 문구 확인")
        pass
    else:
        print("로그인 문구 실패")
        print(f"로그인 유저 이름 : {login_name.text} ")
        raise Exception('My 탭 닉네임 확인 실패')
    print(f"로그인 유저 이름 : {login_name.text} ")


def check_login_btn(wd):
    sleep(1)
    logout_check = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtLogin')
    if '로그인' in logout_check.text:
        pass
    else:
        print('My 탭 로그인 문구 확인 실패')
        raise Exception('My 탭 로그인 문구 확인 실패')
    print(f"로그아웃 문구 확인 :{logout_check.text} ")

def enter_setting_page(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgSetting')
    print('설정 화면 진입')
    sleep(2)
