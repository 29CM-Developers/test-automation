from appium.webdriver.common.appiumby import AppiumBy
from time import sleep
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()


def input_id_password(wd, id, password):
    wd.find_element(AppiumBy.XPATH,
                    '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeTextField[@index="0"]').send_keys(
        id)
    wd.find_element(AppiumBy.XPATH,
                    '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeSecureTextField[@index="1"]').send_keys(
        password)
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, '로그인하기').click()
    sleep(3)


def clear_id_password(wd):
    wd.find_element(AppiumBy.XPATH,
                    '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeTextField[@index="0"]').clear()
    wd.find_element(AppiumBy.XPATH,
                    '//XCUIElementTypeOther[@name="로그인 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeSecureTextField[@index="1"]').clear()


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
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()


def click_simple_join_btn(wd):
    wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeLink[`label == "간편 회원가입하기"`]').click()
