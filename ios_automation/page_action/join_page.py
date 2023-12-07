from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()


def click_required_terms(wd):
    terms = wd.find_elements(AppiumBy.XPATH, '//XCUIElementTypeOther[@index="2"]/XCUIElementTypeOther')
    for required_term in terms:
        if '필수' in required_term.text:
            required_term.click()
        else:
            pass
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, '동의하고 가입하기').click()


def input_email(wd, email):
    wd.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextField').send_keys(email)


def check_same_email_join_error(wd):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '동일한 이메일 주소로 가입된 계정이 있습니다. 기존 계정으로 로그인해주세요.')
        print('기가입된 계정으로 회원가입 실패 확인')
    except NoSuchElementException:
        print('기가입된 계정으로 회원가입 실패 확인 실패')
        raise Exception('기가입된 계정으로 회원가입 실패 확인 실패')
