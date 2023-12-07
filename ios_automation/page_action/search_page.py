from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, swipe_control, scroll_control, ials


def click_back_btn(wd):
    ialc(wd, 'navi_back_btn')


def find_recent_keyword(wd):
    for i in range(0, 3):
        try:
            recent = ial(wd, 'c_최근 검색어')
            if recent.is_displayed():
                break
            else:
                scroll_control(wd, 'U', 30)
        except NoSuchElementException:
            scroll_control(wd, 'U', 50)


def clear_recent_keyword(wd):
    try:
        ial(wd, '//XCUIElementTypeOther[@name="recent_keyword"]')
        ialc(wd, '//XCUIElementTypeButton[@name="모두 지우기"]')
    except NoSuchElementException:
        pass


def check_recent_keyword(wd, keyword):
    recent_keyword = ial(wd, '//XCUIElementTypeOther[@name="recent_keyword"]/XCUIElementTypeStaticText').text
    if keyword == recent_keyword:
        test_result = 'PASS'
        print('최근 검색어 노출 확인')
    else:
        test_result = 'WARN'
        keyword.append('최근 검색어 노출 확인 실패')
        print(f'최근 검색어 노출 확인 실패 : recent-{recent_keyword} / search-{keyword}')
    return test_result


def change_criteria_to_all(wd):
    filter_btn = ial(wd, 'keyword_filter')
    if filter_btn.text == '전체 기준':
        print('필터 : 전체 기준 확인')
        pass
    else:
        filter_btn.click()
        ialc(wd, 'gender_filter_all')
        print(f'필터 : 전체 기준이 아닌 것으로 확인되어 전체 기준으로 변경 - {filter_btn.text}')


def change_criteria_to_women(wd):
    ialc(wd, 'keyword_filter')
    ialc(wd, 'gender_filter_female')


def check_filter_criteria(wd, warning_texts):
    brand_filter = ial(wd, 'keyword_filter').text
    if brand_filter == '여성 기준':
        test_result = 'PASS'
        print('필터 적용 확인 - 필터 기준 문구')
    else:
        test_result = 'WARN'
        warning_texts.append('필터 적용 확인 실패')
        print(f'필터 적용 확인 실패 : {brand_filter.text}')
    return test_result


def check_first_popular_brand_category(wd, warning_texts, first_brand_category_name):
    brand_category_name = ial(wd, '//XCUIElementTypeStaticText[@name="first_popular_brand_title"]').text
    if f'지금 많이 찾는 {first_brand_category_name} 브랜드' in brand_category_name:
        test_result = 'PASS'
        print('첫번째 인기 브랜드 타이틀 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('인기 브랜드 타이틀 확인 실패')
        print('첫번째 인기 브랜드 타이틀 확인 실패')
    return test_result


# num : 검색어 위치 입력 (좌측 첫번째 : 1, 우측 세번째 : 6)
def save_popular_brand_name(wd, num):
    brand_1st = ial(wd, f'(//XCUIElementTypeOther[@name="first_popular_brand_name"])[{num}]')
    brand_1st_name = ial(brand_1st, '//XCUIElementTypeStaticText').text
    return brand_1st_name


def check_popular_brand_name(warning_texts, api_brand_name, brand_name):
    if api_brand_name == brand_name:
        test_result = 'PASS'
        print(f'인기 브랜드 {brand_name} 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('인기 브랜드 확인 실패')
        print(f'인기 브랜드 확인 실패 : api-{api_brand_name} / search-{brand_name}')
    return test_result


def click_first_popular_brand_name(wd):
    ialc(wd, '(//XCUIElementTypeOther[@name="first_popular_brand_name"])[1]')


def click_30th_popular_brand_name(wd):
    ialc(wd, '(//XCUIElementTypeOther[@name="first_popular_brand_name"])[6]')


def swipe_brand_area(wd):
    popular_brand = ial(wd, '//XCUIElementTypeCollectionView[@name="first_popular_brand_list"]')
    swipe_control(wd, popular_brand, 'left', 30)


def check_popular_keyword_title(wd, warning_texts):
    for i in range(0, 3):
        try:
            keyword_title = ial(wd, '지금 많이 찾는 검색어')
            if keyword_title.is_displayed():
                test_result = 'PASS'
                print('인기 검색어 타이틀 확인')
                break
            else:
                scroll_control(wd, 'D', 50)
        except NoSuchElementException:
            scroll_control(wd, 'D', 50)
    else:
        test_result = 'WARN'
        warning_texts.append('인기 검색어 타이틀 확인 실패')
        print('인기 검색어 타이틀 확인 실패')
    return test_result


def save_popular_keyword(wd, ranking):
    keyword = ''
    rank_break = False
    for i in range(0, 10):
        try:
            xpath = '//XCUIElementTypeOther[@name="popular_keyword_rank"]/XCUIElementTypeStaticText'
            keyword_rank = wd.find_elements(AppiumBy.XPATH, xpath)
            i = 0
            for rank in keyword_rank:
                if rank.text == ranking:
                    parent = ials(wd, f'{xpath}/../..')
                    keyword = ial(parent[i],
                                  '//XCUIElementTypeOther[@name="popular_keyword"]/XCUIElementTypeStaticText').text
                    rank_break = True
                    break
                i += 1
            if rank_break:
                break
            scroll_control(wd, "D", 60)
        except NoSuchElementException:
            pass
    return keyword


def check_popular_keyword(warning_texts, popular_keyword, api_keyword):
    if popular_keyword == api_keyword:
        test_result = 'PASS'
        print(f'인기 검색어 {popular_keyword} 노출 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('인기 검색어 노출 확인 실패')
        print(f'인기 검색어 노출 확인 실패 : search-{popular_keyword} / api-{api_keyword}')
    return test_result


def click_popular_keyword(wd, keyword):
    ialc(wd, f'//XCUIElementTypeOther[@name="popular_keyword"]/XCUIElementTypeStaticText[@label="{keyword}"]')


def enter_keyword_and_click_search_btn(wd, keyword):
    wd.find_element(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextField').send_keys(keyword)
    ialc(wd, 'search_btn')
