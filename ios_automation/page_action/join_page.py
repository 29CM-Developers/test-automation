from time import sleep
from selenium.common import NoSuchElementException
from com_utils.element_control import ialk, ialc, ials, ial


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


def check_required_terms_page(wd):
    try:
        ial(wd, 'c_29CM 서비스 이용약관')
        print('회원가입 페이지 진입 확인')
    except NoSuchElementException:
        print('회원가입 페이지 진입 확인 실패')
        raise Exception('회원가입 페이지 진입 확인 실패')


def click_required_terms(wd):
    sleep(2)
    terms = ials(wd, '//label')
    for required_term in terms:
        if '필수' in required_term.text:
            required_term.click()
        else:
            pass
    ialc(wd, '//button[contains(text(), "가입하기")]')


def input_email(wd, email):
    sleep(2)
    ialk(wd, '//input[contains(@name, "username")]', email)


def check_same_email_join_error(wd):
    try:
        ial(wd, '//p[contains(text(), "동일한 이메일 주소로 가입된 계정이 있습니다.")]')
        print('기가입된 계정으로 회원가입 실패 확인')
    except NoSuchElementException:
        print('기가입된 계정으로 회원가입 실패 확인 실패')
        raise Exception('기가입된 계정으로 회원가입 실패 확인 실패')


def check_auth_page(wd):
    try:
        ial(wd, 'c_본인인증하고 가입완료하기')
        print('본인 인증 페이지 진입 확인')
    except NoSuchElementException:
        print('본인 인증 페이지 진입 확인 실패')
        raise Exception('본인 인증 페이지 진입 확인 실패')
