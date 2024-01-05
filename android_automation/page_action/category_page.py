from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from time import sleep, time
from com_utils.element_control import aal, aalc, aals, swipe_control


def click_pin_menu(wd, find_menu):
    sleep(3)
    pin_menu_layer = aal(wd, 'com.the29cm.app29cm:id/shopComposeView')
    pin_menu_list = aal(pin_menu_layer, '//android.view.View/android.view.View[1]')
    click_break = False
    for i in range(0, 5):
        try:
            pin_menu_title = aal(wd, 'c_WELOVE')
            if pin_menu_title == None:
                swipe_control(wd, pin_menu_list, 'left', 50)
            elif pin_menu_title.text == find_menu:
                click_break = True
                sleep(2)
                pin_menu_title.click()
        except NoSuchElementException:
            swipe_control(wd, pin_menu_list, 'left', 50)
            pass
        if click_break:
            break


def click_best_category(wd):
    aalc(wd, 'best_title')
    print("홈 > 카테고리 > 의류 > 베스트 선택")


def click_category_top(wd):
    aalc(wd, 'top_title')
    print("홈 > 카테고리 PLP 진입 > 의류 > 상의 선택")


def click_not_login_user_product_like_btn(wd):
    sleep(3)
    plp_layer = aal(wd, 'com.the29cm.app29cm:id/recyclerview')
    aalc(plp_layer, '//android.view.ViewGroup[1]/android.widget.ImageView[2]')
    print("좋아요 선택")


def click_for_you_category(wd):
    aalc(wd, 'for_you_title')
    sleep(1)


def check_not_login_user_recommended_tab(wd):
    # 추천 확인 추가
    recommend_title = aal(wd, 'c_당신을 위한 추천')
    if recommend_title == None:
        print('비로그인 유저 추천 페이지 타이틀 확인 실패')
        raise Exception('비로그인 유저 추천 페이지 타이틀 확인 실패')
    else:
        print('비로그인 유저 추천 페이지 타이틀 확인')


def click_back_btn(wd):
    # 뒤로가기로 카테고리 화면 진입
    top_menu = aal(wd, 'com.the29cm.app29cm:id/topMenu')
    aalc(top_menu, '//android.view.View/android.view.View')
