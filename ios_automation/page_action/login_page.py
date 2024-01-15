from appium.webdriver.common.appiumby import AppiumBy
from time import sleep
from selenium.common import NoSuchElementException
from com_utils.element_control import ialk, ialc, ial
from ios_automation.page_action import context_change


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


def input_id_password(wd, id, password):
    context_change.switch_context(wd, 'webview')
    ialk(wd, '//input[contains(@name, "username")]', id)
    ialk(wd, '//input[contains(@name, "password")]', password)
    ialc(wd, '//button[contains(text(), "로그인하기")]')
    context_change.switch_context(wd, 'native')
    sleep(3)


def clear_id_password(wd):
    context_change.switch_context(wd, 'webview')
    ial(wd, '//input[contains(@name, "username")]').clear()
    ial(wd, '//input[contains(@name, "password")]').clear()
    context_change.switch_context(wd, 'native')


def check_login_error_text(self, wd):
    error_text = wd.find_element(AppiumBy.XPATH,
                                 '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeOther[1]/XCUIElementTypeStaticText').text
    if self.conf['login_error_text'] in error_text or self.conf['login_exceeded_text'] in error_text:
        print("이메일 로그인 실패 확인")
    else:
        print("이메일 로그인 실패 확인 실패")
        raise Exception('이메일 로그인 실패 확인 실패')


def check_login_page(wd):
    sleep(2)
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인하기')
        print('로그인 페이지 진입 확인')
    except NoSuchElementException:
        print('로그인 페이지 진입 확인 실패')
        raise Exception('로그인 페이지 진입 확인 실패')
    ialc(wd, 'common back icon black')


def click_simple_join_btn(wd):
    context_change.switch_context(wd, 'webview')
    ialc(wd, '//a[contains(text(), "회원가입하기")]')
    context_change.switch_context(wd, 'native')
