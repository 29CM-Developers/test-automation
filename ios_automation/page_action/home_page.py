from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException

from com_utils.element_control import ial, ialc


def check_home_logo(wd):
    try:
        ial(wd, 'navi_logo_btn')
        print('HOME 탭으로 이동 확인')
    except NoSuchElementException:
        print('HOME 탭으로 이동 확인 실패')


def click_close_life_tab(wd):
    select_tab = ial(wd,
                     '//XCUIElementTypeOther[3]/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeStaticText').text
    if select_tab == '라이프':
        ialc(wd, 'ic close white')
    else:
        print('라이프 탭 디폴트 아님')
        pass


# click_tab_name : 선택하려는 상단 탭 이름 입력
def click_tab_name(wd, click_tab_name):
    tab = wd.find_elements(AppiumBy.XPATH,
                           '//XCUIElementTypeOther[3]/XCUIElementTypeCollectionView/XCUIElementTypeCell')
    for text in tab:
        tab_name = text.find_element(AppiumBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeStaticText')
        if tab_name.text == click_tab_name:
            tab_name.click()
        else:
            pass


def save_tab_names(wd):
    tab = wd.find_elements(AppiumBy.XPATH,
                           '//XCUIElementTypeOther[3]/XCUIElementTypeCollectionView/XCUIElementTypeCell')
    tab_name_list = []
    for text in tab:
        tab_name = text.find_element(AppiumBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeStaticText').text
        tab_name_list.append(tab_name)
    tab_name_list = ', '.join(tab_name_list)
    print(tab_name_list)
    return tab_name_list


# tab : 탭을 보여주는 카테고리 / 전체 : 'home' / 라이프 선택 상태 : 'life'
# tab_list : 비교할 탭 이름 리스트
def check_tab_names(self, warning_texts, tab, tab_list):
    if self.conf['compare_home_tab'][tab] in tab_list:
        test_result = 'PASS'
        print('홈 상단 탭 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('이메일 로그인 실패 확인 실패')
        print(self.conf['compare_home_tab'][tab])
        print('홈 상단 탭 확인 실패')
    return test_result
