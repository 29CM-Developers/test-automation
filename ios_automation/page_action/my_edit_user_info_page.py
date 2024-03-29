from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, ialk
from ios_automation.page_action import context_change


def input_password(wd, password):
    context_change.switch_context(wd, 'webview')
    ialk(wd, '//input[contains(@type, "password")]', password)
    context_change.switch_context(wd, 'native')


def click_next_btn(wd):
    ialc(wd, '다음')


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


def check_edit_page_title(wd):
    try:
        ial(wd, '//XCUIElementTypeStaticText[@name="회원정보 수정"]')
        print('회원 정보 수정 페이지 확인 - 타이틀')
    except NoSuchElementException:
        print('이메일 로그인 실패 확인 실패 - 타이틀')
        raise Exception('이메일 로그인 실패 확인 실패 - 타이틀')


def check_edit_page_id(wd, id):
    try:
        ial(wd, id)
        print('회원 정보 수정 페이지 확인 - 이메일')
    except NoSuchElementException:
        print('이메일 로그인 실패 확인 실패 - 이메일')
        raise Exception('이메일 로그인 실패 확인 실패 - 이메일')
