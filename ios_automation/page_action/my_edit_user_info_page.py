from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, ialk


def input_password(wd, password):
    ialk(wd, '//XCUIElementTypeOther[@name="비밀번호 재확인 절차"]/XCUIElementTypeSecureTextField', password)


def click_next_btn(wd):
    ialc(wd, '다음')


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


def check_edit_page_title(wd, warning_texts):
    try:
        ial(wd, '//XCUIElementTypeStaticText[@name="회원정보 수정"]')
        test_result = 'PASS'
        print('회원 정보 수정 페이지 확인 - 타이틀')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('이메일 로그인 실패 확인 실패')
        print('이메일 로그인 실패 확인 실패 - 타이틀')
    return test_result


def check_edit_page_id(wd, warning_texts, id):
    try:
        ial(wd, id)
        test_result = 'PASS'
        print('회원 정보 수정 페이지 확인 - 이메일')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('이메일 로그인 실패 확인 실패')
        print('이메일 로그인 실패 확인 실패 - 이메일')
    return test_result
