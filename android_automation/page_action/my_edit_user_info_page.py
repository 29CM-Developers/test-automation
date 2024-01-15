from time import sleep
from com_utils.element_control import aal, aalc, aalk


def input_password(wd, password):
    aalk(wd, '//android.widget.EditText', password)


def click_next_btn(wd):
    aalc(wd, 'cn_android.widget.Button')


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')
    print('뒤로가기 선택')


def check_edit_page_title(wd):
    try:
        edit_member_information = aal(wd, 'c_회원정보 수정')
        print("회원정보 수정 화면 진입")
        if edit_member_information.text == '회원정보 수정':
            print("회원정보 수정 페이지 타이틀 확인")
            print(f"가이드 문구 : {edit_member_information.text} ")
        else:
            print("회원정보 수정 페이지 타이틀 확인 실패")
            print(f"가이드 문구 : {edit_member_information.text} ")
            raise Exception('이메일 로그인 실패 확인 실패 - 타이틀')
    except Exception:
        print("회원정보 수정 페이지 타이틀 확인 실패")
        print(f"가이드 문구 : {edit_member_information.text} ")
        raise Exception('이메일 로그인 실패 확인 실패 - 타이틀')


def check_edit_page_id(wd, id):
    try:
        user_email = aal(wd, f'c_{id}')
        print("로그인한 유저 이메일 확인")

        if user_email.text == id:
            print("회원정보 수정 페이지 확인")
        else:
            print("회원정보 수정 페이지 확인 실패")
            raise Exception('이메일 로그인 실패 확인 실패 - 이메일')
        print(f"가이드 문구 : {user_email.text} ")
    except Exception:
        print("회원정보 수정 페이지 타이틀 확인 실패")
        print(f"가이드 문구 : {user_email.text} ")
        raise Exception('이메일 로그인 실패 확인 실패 - 이메일')
