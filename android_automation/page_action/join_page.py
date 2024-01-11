from time import sleep
from com_utils.element_control import aal, aalc, aalk


def click_back_btn(wd):
    # 뒤로가기로 홈화면 진입 확인
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')
    print("뒤로가기 선택")
    # sleep(2)


def click_required_terms(wd):
    # 이용 약관 모두 동의 선택
    try:
        aalc(wd, "//*[contains(@text, 'all')]")
        print('이용 약관 모두 동의 선택')
        # 동의하고 가입하기 선택
        aalc(wd, "//*[contains(@text, '동의하고 가입하기')]")
        print('동의하고 가입하기 선택')
        #sleep(2)
    except Exception:
        click_back_btn(wd)
        pass


def input_email(wd, email):
    aalk(wd, 'cn_android.widget.EditText', email)
    sleep(1)


def check_same_email_join_error(wd):
    try:
        element = aal(wd, "//*[contains(@text, '동일한 이메일 주소로 가입된 계정이 있습니다. 기존 계정으로 로그인해주세요.')]")
        if element == None:
            print("기가입된 계정으로 회원가입 실패 확인 실패")
            raise Exception('기가입된 계정으로 회원가입 실패 확인 실패')
        print("기가입된 계정으로 회원가입 실패 확인 성공")
    except Exception:
        print("기가입된 계정으로 회원가입 실패 확인 실패")
        raise Exception('기가입된 계정으로 회원가입 실패 확인 실패')
