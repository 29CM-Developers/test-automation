from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, ials
from com_utils.deeplink_control import move_to_my
from ios_automation.page_action import bottom_sheet, login_page

import com_utils.element_control


def enter_setting_page(wd):
    ialc(wd, 'setting_btn')


def enter_login_page(wd):
    ialc(wd, 'login_btn')
    sleep(3)


def find_login_btn(self, wd):
    com_utils.deeplink_control.move_to_my(self, wd)
    for i in range(0, 5):
        try:
            element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'login_btn')
            if element.is_displayed():
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "U", 50)


def check_login_btn(wd):
    try:
        ial(wd, 'login_btn')
        print('My 탭 로그인 문구 확인')
    except NoSuchElementException:
        print('My 탭 로그인 문구 확인 실패')
        raise Exception('My 탭 로그인 문구 확인 실패')


def check_nickname(self, wd):
    bottom_sheet.find_icon_and_close_bottom_sheet(wd)
    nickname_break = False
    for i in range(0, 5):
        try:
            element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, self.pconf['nickname'])
            if element.is_displayed():
                nickname_break = True
                print('My 탭 닉네임 확인')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "U", 50)
    if not nickname_break:
        print('My 탭 닉네임 확인 실패')
        raise Exception('My 탭 닉네임 확인 실패')


def check_recent_title(wd, type, title):
    recent = ial(wd, '//*[@name="나의 활동"]/../..')
    recent_title = ials(recent, '//XCUIElementTypeStaticText')[1].text
    if recent_title in title:
        print(f'최근 본 {type} 확인')
    else:
        print(f'최근 본 {type} 확인 실패 : {title} / {recent_title}')
        raise Exception(f'최근 본 {type} 확인 실패')


def expand_recent_contents(wd):
    ialc(wd, '//XCUIElementTypeButton[6]')


def close_recent_contents(wd):
    ialc(wd, '//XCUIElementTypeButton[4]')


def check_recent_history(wd, product_name, post_title):
    recent_history = []
    recent = ials(wd, '//XCUIElementTypeCell/XCUIElementTypeTable/XCUIElementTypeCell')
    for title in recent[:3]:
        title = ial(title, '//XCUIElementTypeStaticText').text
        recent_history.append(title)

    if product_name in recent_history and post_title in recent_history:
        print('최근 본 컨텐츠 히스토리 확인')
    else:
        print(f'최근 본 컨텐츠 히스토리 확인 실패: {product_name} / {post_title} / {recent_history}')
        raise Exception('최근 본 컨텐츠 히스토리 확인 실패')


def click_delivery_order_menu(wd):
    for i in range(0, 5):
        try:
            element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, '주문배송조회')
            if element.is_displayed():
                ialc(wd, '주문배송조회')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "U", 40)


def click_review_menu(wd):
    for i in range(0, 5):
        try:
            element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, '상품 리뷰')
            if element.is_displayed():
                ialc(wd, '상품 리뷰')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 40)


def click_edit_user_info_menu(wd):
    for i in range(0, 5):
        try:
            element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, '회원 정보 수정')
            if element.is_displayed():
                ialc(wd, '회원 정보 수정')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 40)


def click_coupon_menu(wd):
    for i in range(0, 5):
        try:
            element = ial(wd, '쿠폰')
            if element.is_displayed():
                ialc(wd, '쿠폰')
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 45)


def find_logout_btn(wd):
    for i in range(0, 5):
        try:
            element = ial(wd, 'c_LOGOUT')
            if element.is_displayed():
                com_utils.element_control.scroll_control(wd, "D", 30)
                break
        except NoSuchElementException:
            pass
        com_utils.element_control.scroll_control(wd, "D", 50)


def click_logout_btn(wd):
    ialc(wd, 'c_LOGOUT')


def check_logout_and_login_btn(self, wd):
    # 로그아웃 버튼 선택
    find_logout_btn(wd)
    click_logout_btn(wd)

    # 로그아웃 완료 > 로그인,회원가입 문구 확인
    move_to_my(self, wd)
    find_login_btn(self, wd)
    check_login_btn(wd)


def check_logout_status(self, wd):
    com_utils.deeplink_control.move_to_my(self, wd)
    try:
        ial(wd, 'login_btn')
    except NoSuchElementException:
        find_logout_btn(wd)
        click_logout_btn(wd)


def check_login_status(self, wd, id):
    if 'custom' in self.user:
        id = self.pconf['id_custom_29cm']
    password = self.pconf['password_29cm']

    com_utils.deeplink_control.move_to_my(self, wd)
    try:
        ial(wd, 'login_btn')
        login_page.direct_login(self, wd, id, password)
    except NoSuchElementException:
        pass
