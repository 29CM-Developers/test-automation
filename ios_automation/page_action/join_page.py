from time import sleep
from selenium.common import NoSuchElementException
from com_utils.element_control import ialk, ialc, ials, ial


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


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
