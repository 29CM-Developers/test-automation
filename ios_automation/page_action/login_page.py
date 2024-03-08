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
    error_text = ial(wd, '//*[contains(@name, "실패") or contains(@name, "시도")]').text
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
        ialc(wd, '//XCUIElementTypeLink[@name="새로운 계정으로 로그인"]')
    except NoSuchElementException:
        pass
    ialk(wd, '//XCUIElementTypeOther[@name="기사"]/XCUIElementTypeTextField', id)
    ialk(wd, '//XCUIElementTypeOther[@name="기사"]/XCUIElementTypeSecureTextField', password)
    ialc(wd, '//XCUIElementTypeButton[@name="로그인"]')


def kakao_login(wd, id, password):
    try:
        ialc(wd, '다른 카카오계정으로 로그인')
    except NoSuchElementException:
        pass
    try:
        ialc(wd, f'c_{id}')
    except NoSuchElementException:
        kakao_input_id_password(wd, id, password)
    sleep(3)


def naver_input_id_password(wd, id, password):
    try:
        ial(wd, 'c_29CM 서비스 이용약관')
        print('미가입 네이버 계정 선택 상태 확인')
    except NoSuchElementException:
        try:
            ialc(wd, id)
        except NoSuchElementException:
            try:
                ialc(wd, '다른 아이디로')
            except NoSuchElementException:
                pass
            ialk(wd, '//XCUIElementTypeTextField', id)
            ialk(wd, '//XCUIElementTypeSecureTextField', password)
            ialc(wd, '//XCUIElementTypeButton[@name="로그인"]')

        try:
            ialc(wd, '전체 동의하기')
            ialc(wd, '//XCUIElementTypeButton[@name="동의하기"]')
        except NoSuchElementException:
            pass
    sleep(3)


def facebook_input_id_password(wd, id, password):
    try:
        ialk(wd, '//XCUIElementTypeOther[@name="주요"]/XCUIElementTypeTextField', id)
        ialk(wd, '//XCUIElementTypeOther[@name="주요"]/XCUIElementTypeSecureTextField', password)
        ialc(wd, '//XCUIElementTypeButton[@name="로그인"]')
    except NoSuchElementException:
        pass


def facebook_login_error_check(wd):
    try:
        ial(wd, 'c_Back to Home')
        ialc(wd, '//XCUIElementTypeButton[@name="취소"]')
        click_sns_login_btn(wd, '페이스북')
    except NoSuchElementException:
        pass


def facebook_login_confirm(wd, id, password):
    try:
        ialc(wd, 'c_님으로 계속')
    except NoSuchElementException:
        facebook_input_id_password(wd, id, password)
        facebook_login_error_check(wd)
        sleep(2)
        ialc(wd, 'c_님으로 계속')
    sleep(3)


def apple_input_password(wd, password):
    try:
        apple_popup = ial(wd, '//XCUIElementTypeOther[@name="Sign In With Apple"]')
        ialk(apple_popup, '//XCUIElementTypeSecureTextField', password)
        ialc(wd, '//XCUIElementTypeButton[@name="로그인"]')
    except:
        pass
    sleep(3)


# sns_name : '카카오', '네이버', '페이스북', 'Apple'
def click_sns_login_btn(wd, sns_name):
    context_change.switch_context(wd, 'webview')
    print(f'"{sns_name}" 로그인 확인')
    try:
        ialc(wd, f'//span[contains(text(), "{sns_name}")]/..')
    except NoSuchElementException:
        pass
    context_change.switch_context(wd, 'native')

    if sns_name == 'Apple':
        try:
            ialc(wd, "//XCUIElementTypeCell[contains(@label, '나의 이메일 가리기')]")
        except NoSuchElementException:
            pass
        ialc(wd, 'AUTHORIZE_BUTTON_TITLE')
    elif sns_name == '네이버':
        sleep(2)
    else:
        try:
            ialc(wd, '계속')
        except NoSuchElementException:
            pass


def check_duplicate_account(wd):
    try:
        ial(wd, 'c_존재합니다')
        print("SNS 계정 회원가입 실패 확인 - 팝업")
        ialc(wd, '확인')
    except NoSuchElementException:
        print("SNS 계정 회원가입 실패 확인 실패 - 팝업")
        raise Exception('SNS 계정 회원가입 실패 확인 실패 - 팝업')


def check_id_input_field_test(wd, id):
    input_field_test = ial(wd, '//XCUIElementTypeTextField').text
    if id == input_field_test:
        print("SNS 계정 회원가입 실패 확인 - 입력란")
    else:
        print("SNS 계정 회원가입 실패 확인 실패 - 입력란")
        raise Exception('SNS 계정 회원가입 실패 확인 실패 - 입력란')
