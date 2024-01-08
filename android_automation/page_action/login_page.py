from appium.webdriver.common.appiumby import AppiumBy
from time import sleep
from com_utils.element_control import aal, aalc, aalk


def input_id_password(wd, id, password):
    aalk(wd, '//android.widget.EditText[1]', id)
    aalk(wd, '//android.widget.EditText[2]', password)
    aalc(wd, '//android.widget.Button')
    print("로그인 버튼 선택")


def clear_id_password(wd):
    aal(wd, '//android.widget.EditText[1]').clear()
    aal(wd, '//android.widget.EditText[2]').clear()


def check_login_error_text(self, wd):
    # 로그인 실패 문구 확인
    guide_text = aal(wd, '//*[@resource-id="__next"]/android.view.View[1]/android.widget.TextView')

    if "5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다." in guide_text.text:
        print("'5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다.’ 가이드 문구 노출 확인")
    else:
        print("'5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다.’ 가이드 문구 노출 실패")
        raise Exception('이메일 로그인 실패 확인 실패')
    print(f"가이드 문구 : {guide_text.text} ")
    sleep(1)


def check_login_page(wd):
    # 로그인 화면 진입 확인
    login_page_title = aal(wd, '//*[@resource-id="__next"]/android.widget.TextView[1]')
    print("홈 > 마이페이지 > 로그인 화면 진입")
    sleep(1)
    if '로그인' in login_page_title.text:
        print("로그인 문구 확인")
    else:
        print("로그인 문구 실패")
        raise Exception('로그인 화면 진입 확인 실패')
    print(f"가이드 문구 : {login_page_title.text} ")


def click_simple_join_btn(wd):
    # 간편 회원가입하기 버튼 선택
    aalc(wd, '간편 회원가입하기')
    print("간편 회원가입하기 버튼 선택")
