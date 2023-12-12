from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc, swipe_control, scroll_control, aals


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


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
