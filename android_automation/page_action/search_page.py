from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc, swipe_control, scroll_control, aals


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


def is_keyboard_displayed(wd):
    try:
        return wd.is_keyboard_shown()
    except Exception as e:
        print(f"Error checking keyboard state: {e}")
        return False


# 키보드 닫기 함수
def close_keyboard(wd):
    try:
        wd.hide_keyboard()
    except Exception as e:
        print(f"Error hiding keyboard: {e}")


def find_recent_keyword(wd):
    for i in range(0, 3):
        try:
            recent = aal(wd, 'c_최근 검색어')
            if recent.is_displayed():
                break
            else:
                scroll_control(wd, 'U', 30)
        except NoSuchElementException:
            scroll_control(wd, 'U', 50)


def clear_recent_keyword(wd):
    try:
        aal(wd, 'c_최근 검색어')
        aalc(wd, 'c_모두 지우기')
    except NoSuchElementException:
        pass


def check_recent_keyword(wd, keyword):
    recent_keyword = aal(wd,
                         '//android.view.ViewGroup/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.TextView').text
    if keyword == recent_keyword:
        print('최근 검색어 노출 확인')
    else:
        print(f'최근 검색어 노출 확인 실패 : recent-{recent_keyword} / search-{keyword}')
        raise Exception('최근 검색어 노출 확인 실패')


def enter_keyword_and_click_search_btn(wd, keyword):
    wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/searchEditText').send_keys(keyword)
    aalc(wd, 'com.the29cm.app29cm:id/searchImg')
    sleep(2)


def save_popular_brand_name(wd, num):
    # 키보드가 올라가 있는지 확인하고, 올라가 있다면 닫기
    if is_keyboard_displayed(wd):
        print("키패드 열림 확인")
        close_keyboard(wd)
        print("키패드 닫기")
    else:
        print("키패드 미노출")

    delete_all = aal(wd, 'c_모두 지우기')
    if delete_all == None:
        print("최근검색어 없음")
    else:
        print("최근검색어 있음")
        aalc(wd, 'c_모두 지우기')

    brand_6th = aal(wd, f'(//android.view.View[@content-desc="popular_brand_layer"])[1]/android.view.View[{num}]')
    brand_6th_name = aal(brand_6th, '//android.widget.TextView[2]').text
    print(f'브랜드 6위 이름 : {brand_6th_name}')
    return brand_6th_name


def click_popular_brand_name(wd, num):
    brand_6th = aal(wd, f'(//android.view.View[@content-desc="popular_brand_layer"])[1]/android.view.View[{num}]')
    aalc(brand_6th, '//android.widget.TextView[2]')
    sleep(2)
    print('브랜드 6위 선택')
