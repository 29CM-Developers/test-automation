from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from com_utils import element_control
from com_utils.element_control import aal, aalc, scroll_control, aals


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')

def check_keyboard_clear_recent_keyword(wd):
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
        recent = aal(wd, 'c_최근 검색어')
        if recent == None:
            pass
        elif recent.is_displayed():
            break
        scroll_control(wd, 'U', 50)


def clear_recent_keyword(wd):
    try:
        aal(wd, 'c_최근 검색어')
        aalc(wd, 'c_모두 지우기')
    except Exception:
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

    brand_layer = aal(wd, f'(//android.view.View[@content-desc="popular_brand_layer"])[1]/android.view.View[{num}]')
    bbrand_layer_name = aal(brand_layer, '//android.widget.TextView[2]').text
    print(f'브랜드 {num}위 이름 : {bbrand_layer_name}')
    return bbrand_layer_name


def click_popular_brand_name(wd, num):
    brand_layer = aal(wd, f'(//android.view.View[@content-desc="popular_brand_layer"])[1]/android.view.View[{num}]')
    aalc(brand_layer, '//android.widget.TextView[2]')
    print(f'{num}위 브랜드 선택')


def check_first_popular_brand_category(wd, first_brand_category_name):
    brand_category_name = aal(wd, 'search_popular_clothes_brand').text
    if f'지금 많이 찾는 {first_brand_category_name} 브랜드' in brand_category_name:
        print('첫번째 인기 브랜드 타이틀 확인')
    else:
        print(f'첫번째 인기 브랜드 타이틀 확인 실패 : {brand_category_name}')
        raise Exception('첫번째 인기 브랜드 타이틀 확인 실패')


def click_delete_btn(wd):
    # 최근 검색어 있는 경우 모두 지우기로 삭제
    delete_all = aals(wd, "c_모두 지우기")
    if delete_all == None:
        pass
    else:
        delete_all[0].click()


def change_criteria_to_all(wd):
    filter_btn = aal(wd, 'c_전체 기준')
    if filter_btn == None:
        aalc(wd, 'c_여성 기준')
        aalc(wd, 'filter_all')
        print(f'필터가 전체 기준이 아닌 것으로 확인되어 전체 기준으로 변경')
    elif filter_btn.text == '전체 기준':
        print('필터 : 전체 기준 확인')
        pass


def check_popular_brand_name(api_brand_name, brand_name):
    if api_brand_name in brand_name:
        print(f'인기 브랜드 {brand_name} 확인')
    else:
        print(f'인기 브랜드 확인 실패 : api-{api_brand_name} / search-{brand_name}')
        raise Exception(f'인기 브랜드 확인 실패 : api-{api_brand_name} / search-{brand_name}')


def swipe_brand_area(wd):
    brand_layer = wd.find_element(AppiumBy.XPATH,
                                  '(//android.view.View[@content-desc="popular_brand_layer"])[1]')
    for _ in range(0, 4):
        element_control.swipe_control(wd, brand_layer, 'left', 60)
        sleep(1)
        brand_layer = wd.find_element(AppiumBy.XPATH,
                                      '(//android.view.View[@content-desc="popular_brand_layer"])[1]')


def change_criteria_to_women(wd):
    aalc(wd, "c_전체 기준")
    aalc(wd, 'filter_woman')


def check_filter_criteria(self, wd):
    filter_name_tag = f"{self.conf['search_filter_gender']['WOMEN']} 기준"
    print(filter_name_tag)
    for _ in range(10):
        element = aal(wd, f"c_{filter_name_tag}")
        if element == None:
            pass
        else:
            print(f"element : {element.text}")
            if element.is_displayed():
                print("아이템 발견")
                brand_filter = element.text
                break
        # 요소를 찾지 못하면 아래로 스크롤
        scroll_control(wd, "D", 50)
    if brand_filter == '여성 기준':
        print('필터 적용 확인 - 필터 기준 문구')
    else:
        print(f'필터 적용 확인 실패 : {brand_filter}')
        raise Exception(f'필터 적용 확인 실패 : {brand_filter}')


def check_popular_keyword_title(wd):
    # 지금 많이 찾는 검색어 찾기
    for i in range(0, 3):
        search_container_title = aal(wd, 'search_popular_search')
        if search_container_title == None:
            pass
        else:
            search_container_title_text = search_container_title.text
            print(search_container_title_text)
            break
        scroll_control(wd, 'D', 50)

    if search_container_title_text == '지금 많이 찾는 검색어':
        print('인기 검색어 타이틀 확인')
        pass
    else:
        print('인기 검색어 타이틀 확인 실패')
        raise Exception('인기 검색어 타이틀 확인 실패')


def save_popular_keyword(wd, ranking, keyword):
    scroll_control(wd, "D", 30)
    for _ in range(10):
        element = aal(wd, f'//*[@text="{keyword}"]')
        if element == None:
            pass
        elif element.is_displayed():
            parent = aal(wd, f'//*[@text="{keyword}"]/../..')
            ranking_element = aal(parent, f'//*[@text="{ranking}"]')
            if ranking_element == None:
                pass
            else:
                return element.text
        # 요소를 찾지 못하면 아래로 스크롤
        scroll_control(wd, "D", 50)


def check_popular_keyword(popular_keyword, api_keyword):
    if popular_keyword == api_keyword:
        print(f'인기 검색어 {popular_keyword} 노출 확인')
    else:
        print(f'인기 검색어 노출 확인 실패 : search-{popular_keyword} / api-{api_keyword}')
        raise Exception('인기 검색어 노출 확인 실패')


def click_popular_keyword(wd, keyword):
    aalc(wd, f'c_{keyword}')
