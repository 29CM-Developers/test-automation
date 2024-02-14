from android_automation.page_action.bottom_sheet import close_bottom_sheet, close_like_bottom_sheet
from android_automation.page_action.like_page import close_brand_recommended_page
from android_automation.page_action.select_category_page import test_select_category
from com_utils.element_control import aalc
from time import sleep


def move_to_home(wd):
    aalc(wd, 'HOME')
    close_bottom_sheet(wd)


def move_to_category(wd):
    sleep(3)
    aalc(wd, 'CATEGORY')


def move_to_search(wd):
    sleep(1)
    aalc(wd, 'SEARCH')
    print("하단 SEARCH탭 선택")


def move_to_like(wd):
    aalc(wd, 'LIKE')
    sleep(2)
    # 관심 브랜드 선택 화면 발생 케이스
    close_brand_recommended_page(wd)
    close_bottom_sheet(wd)
    close_like_bottom_sheet(wd)


def move_to_my(wd):
    aalc(wd, 'MY')
    print('MY 선택')


def move_to_cart(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgCart')
    print("장바구니 선택")


def move_to_back(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')
    print("뒤로가기 선택")


def move_to_alarm(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgInboxNotification')
    print("우상단 알람 선택")


def move_to_top_cart(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgCart')
    print("우상단 장바구니 선택")


def logout_and_move_to_home(wd):
    aalc(wd, 'HOME')
    test_select_category(wd)
    close_bottom_sheet(wd)
