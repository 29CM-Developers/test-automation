from time import sleep
from android_automation.page_action import my_page, navigation_bar
from android_automation.page_action.select_category_page import test_select_category
from com_utils.deeplink_control import move_to_my_Android
from com_utils.element_control import aal, aalc, aalk


def input_id_password(wd, id, password):
    sleep(2)
    aalk(wd, '//android.widget.EditText[1]', id)
    aalk(wd, '//android.widget.EditText[2]', password)
    aalc(wd, '//android.widget.Button')
    print("로그인 버튼 선택")


def clear_id_password(wd):
    aal(wd, '//android.widget.EditText[1]').clear()
    aal(wd, '//android.widget.EditText[2]').clear()


def check_login_error_text(self, wd):
    # 로그인 실패 문구 확인
    guide_text = aal(wd, 'c_5회 로그인 실패 시')
    if guide_text == None:
        print("'5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다.’ 가이드 문구 노출 실패")
        raise Exception('이메일 로그인 실패 확인 실패')
    elif "5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다." in guide_text.text:
        print(f"가이드 문구 : {guide_text.text} 확인")
        print("'5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다.’ 가이드 문구 노출 확인")
    else:
        print("'5회 로그인 실패 시, 로그인이 10분 동안 제한됩니다.’ 가이드 문구 노출 실패")
        raise Exception('이메일 로그인 실패 확인 실패')


def check_login_page(wd):
    sleep(5)
    # 로그인 화면 진입 확인
    login_page_button = aal(wd, 'c_로그인하기')
    print("홈 > 마이페이지 > 로그인 화면 진입")
    if '로그인' in login_page_button.text:
        print("로그인 문구 확인")
    else:
        print("로그인 문구 실패")
        raise Exception('로그인 화면 진입 확인 실패')
    print(f'login_page_button :{login_page_button.text}')


def click_simple_join_btn(wd):
    sleep(5)
    # 간편 회원가입하기 버튼 선택
    aalc(wd, 'c_간편 회원가입하기')
    print("간편 회원가입하기 버튼 선택")

def check_login(self, wd, id):
    sleep(2)
    # 로그인 페이지 진입
    move_to_my_Android(wd)

    # 로그인 성공 진입 확인
    login_name = aal(wd, 'com.the29cm.app29cm:id/txtUserName')
    if login_name == None:
        print("미로그인 상태 확인")
        my_page.enter_login_page(wd)
        input_id_password(wd, id, self.pconf['LOGIN_SUCCESS_PW'])
    elif login_name.text == self.pconf['MASKING_NAME']:
        print("로그인 상태 확인")
    my_page.check_nickname(self, wd)
    navigation_bar.move_to_home(wd)
    # 복귀 후, 홈 탭 진입 전 노출 화면 있는지 확인
    test_select_category(wd)

def check_logout(self, wd):
    sleep(2)
    # 로그인 페이지 진입
    move_to_my_Android(wd)

    # 로그인 성공 진입 확인
    login_name = aal(wd, 'com.the29cm.app29cm:id/txtUserName')
    if login_name == None:
        print("미로그인 상태 확인")
    elif login_name.text == self.pconf['MASKING_NAME']:
        # 로그아웃 버튼 선택
        my_page.find_logout_btn(wd)
        my_page.click_logout_btn(wd)

        # 로그아웃 완료 > 로그인,회원가입 문구 확인
        my_page.find_login_btn(wd)
        my_page.check_login_btn(wd)

    navigation_bar.move_to_home(wd)
    # 복귀 후, 홈 탭 진입 전 노출 화면 있는지 확인
    test_select_category(wd)