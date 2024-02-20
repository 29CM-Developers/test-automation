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


def kakao_input_id_password(wd, id, password):
    try:
        ialc(wd, '다른 카카오계정으로 로그인')
        ialc(wd, '//XCUIElementTypeLink[@name="새로운 계정으로 로그인"]')
    except:
        pass
    ialk(wd, '//XCUIElementTypeOther[@name="기사"]/XCUIElementTypeTextField', id)
    ialk(wd, '//XCUIElementTypeOther[@name="기사"]/XCUIElementTypeSecureTextField', password)
    ialc(wd, '//XCUIElementTypeButton[@name="로그인"]')
    sleep(1)


def naver_input_id_password(wd, id, password):
    try:
        ialc(wd, id)
    except:
        ialk(wd, '//XCUIElementTypeOther[@name="네이버 : 로그인"]/XCUIElementTypeTextField', id)
        ialk(wd, '//XCUIElementTypeOther[@name="네이버 : 로그인"]/XCUIElementTypeSecureTextField', password)
        ialc(wd, '//XCUIElementTypeOther[@name="로그인 상태 유지"]')
        ialc(wd, '//XCUIElementTypeButton[@name="로그인"]')
        pass
    sleep(1)


def facebook_input_id_password(wd, id, password):
    try:
        ial(wd, '29CM에 연결하려면 Facebook 계정에 로그인하세요')
        ialk(wd, '//XCUIElementTypeOther[@name="주요"]/XCUIElementTypeTextField', id)
        ialk(wd, '//XCUIElementTypeOther[@name="주요"]/XCUIElementTypeSecureTextField', password)
        ialc(wd, '//XCUIElementTypeButton[@name="로그인"]')
    except:
        pass


def facebook_login_confirm(wd, id, password):
    try:
        ialc(wd, 'c_님으로 계속')
    except:
        facebook_input_id_password(wd, id, password)
        sleep(2)
        ialc(wd, 'c_님으로 계속')
    sleep(1)


def apple_input_password(wd, password):
    try:
        apple_popup = ial(wd, '//XCUIElementTypeOther[@name="Sign In With Apple"]')
        ialk(apple_popup, '//XCUIElementTypeSecureTextField', password)
        ialc(wd, '//XCUIElementTypeButton[@name="로그인"]')
    except:
        pass
    sleep(1)


# sns_name : '카카오', '네이버', '페이스북', 'Apple'
def click_sns_login_btn(wd, sns_name):
    context_change.switch_context(wd, 'webview')
    print(f'{sns_name} 로그인 확인')
    ialc(wd, f'//span[contains(text(), "{sns_name}")]/..')
    context_change.switch_context(wd, 'native')

    if sns_name == 'Apple':
        try:
            ialc(wd, "//XCUIElementTypeCell[contains(@label, '나의 이메일 가리기')]")
        except:
            pass
        ialc(wd, 'AUTHORIZE_BUTTON_TITLE')
    elif sns_name == '네이버':
        pass
    else:
        ialc(wd, '계속')
