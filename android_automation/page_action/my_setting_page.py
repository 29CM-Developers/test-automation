from time import sleep
from com_utils.element_control import aal, aalc


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


def check_notification(wd):
    try:
        label_shopping = aal(wd, 'com.the29cm.app29cm:id/txtLabelShopping').text
        alarm_label = aal(wd, 'com.the29cm.app29cm:id/txtAlarmLabel').text
        if label_shopping == '쇼핑 알림' and alarm_label == '재입고 알림':
            print("설정 화면 진입 확인")
            pass
        else:
            print(f"타이틀 확인 : {label_shopping}, {alarm_label}")
            print('설정 화면 진입 확인 실패')
            raise Exception('설정 화면 진입 확인 실패')
    except Exception:
        print('설정 화면 진입 확인 실패')
        raise Exception('설정 화면 진입 확인 실패')
