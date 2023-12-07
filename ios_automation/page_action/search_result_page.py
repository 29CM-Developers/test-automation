from time import sleep
from com_utils.api_control import search_relate_keyword
from com_utils.element_control import ial, ialc, ials, scroll_control, element_scroll_control, swipe_control
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    ialc(wd, 'navi_back_btn')


def check_input_field(wd, test_result, warning_texts, keyword):
    search_input_field = ial(wd, 'input_keyword').text
    if search_input_field == keyword:
        print('인기 검색어 검색 확인 - 입력란')
    else:
        test_result = 'WARN'
        warning_texts.append('인기 브랜드 검색 결과 확인 실패')
        print(f'인기 브랜드 검색 결과 확인 실패 : {search_input_field}')
    return test_result


def check_relate_brand_name(wd, test_result, warning_texts, compare_brand_name):
    relate_brand_name = ials(wd, '//XCUIElementTypeStaticText[@name="releate_brand_name"]')
    relate_name = ''
    relate_break = False
    for brand_name in relate_brand_name:
        relate_name = brand_name.text
        if compare_brand_name in relate_name:
            relate_break = True
            print('인기 브랜드 검색 확인 - 연관 브랜드')
            break
        else:
            pass
    if not relate_break:
        test_result = 'WARN'
        warning_texts.append('인기 브랜드 검색 확인 실패 - 연관 브랜드')
        print(f'인기 브랜드 검색 확인 실패 - 연관 브랜드 : {relate_name}')
    return test_result


def check_product_brand_name(wd, test_result, warning_texts, compare_brand_name):
    product_brand_name = ''
    for i in range(0, 3):
        try:
            product_brand = ials(wd, 'brand_name')
            product_brand_name = product_brand[0]
            if product_brand_name.is_displayed():
                product_brand_name = product_brand_name.text
                break
        except NoSuchElementException:
            scroll_control(wd, 'D', 30)

    if compare_brand_name == product_brand_name:
        print('인기 브랜드 검색 상품 확인 - 상품 브랜드')
    else:
        test_result = 'WARN'
        warning_texts.append('인기 브랜드 검색 상품 확인 실패 - 상품 브랜드')
        print(f'인기 브랜드 검색 상품 확인 실패: 검색어-{compare_brand_name} / 상품 브랜드-{product_brand_name}')
    return test_result


def check_relate_keyword(wd, test_result, warning_texts, api_keyword_1st):
    # 연관 검색어 리스트 API 호출
    relate_keyword_list = search_relate_keyword(api_keyword_1st)

    if not relate_keyword_list:
        search_input_field = ial(wd, 'input_keyword').text
        if search_input_field == api_keyword_1st:
            print('인기 검색어 검색 확인 - 입력란')
        else:
            test_result = 'WARN'
            warning_texts.append('인기 검색어 검색 결과 확인 실패')
            print(f'인기 검색어 검색 결과 확인 실패 : {api_keyword_1st} / {search_input_field}')
    else:
        relate_keyword_api = relate_keyword_list[0]
        relate_keyword = ials(wd, 'related_keyword')[0]
        relate_keyword_1st = ial(relate_keyword, '//XCUIElementTypeStaticText').text
        if relate_keyword_api == relate_keyword_1st:
            print('인기 검색어 검색 확인 - 연관 검색어')
        else:
            test_result = 'WARN'
            warning_texts.append('인기 검색어 검색 결과 확인 실패')
            print(f'인기 검색어 검색 결과 확인 실패 : {relate_keyword_1st} / {relate_keyword_api}')
    return test_result


def click_sort_filter_btn(wd, sort):
    ialc(wd, 'sort_filter')
    ialc(wd, f'**/XCUIElementTypeButton[`label == "{sort}"`]')
    print(f'정렬 : {sort} 선택')


def click_color_filter(wd, color):
    ialc(wd, 'color_filter')
    for i in range(0, 3):
        try:
            ialc(wd, f'**/XCUIElementTypeButton[`label == "{color}"`]')
            print(f'필터 - 색상 : {color} 선택')
            break
        except NoSuchElementException:
            color_sheet = ial(wd, 'type == "XCUIElementTypeScrollView"')
            element_scroll_control(wd, color_sheet, "D", 25)


def click_category_filter(wd, category):
    ialc(wd, '**/XCUIElementTypeStaticText[`label == "카테고리"`]')
    ialc(wd, category)
    print(f'필터 - 카테고리 : {category} 선택')


def click_product_info_filter(wd, info):
    ialc(wd, '**/XCUIElementTypeStaticText[`label == "상품정보"`]')
    ialc(wd, f'**/XCUIElementTypeStaticText[`label == "{info}"`]')
    print(f'필터 - 상품정보 : {info} 선택')


def click_apply_filter_btn(wd):
    ialc(wd, 'filter_apply_btn')
    sleep(2)


def save_filter_info(wd):
    # 필터 element 확인
    plp_view = ial(wd, '//XCUIElementTypeCollectionView[@index="1"]')
    filter_view = ial(plp_view, '//XCUIElementTypeOther/XCUIElementTypeCollectionView[@index="2"]')

    # 적용된 필터 확인
    filter_break = False
    filter_list = []
    for i in range(0, 2):
        filters = ials(filter_view,
                       '//XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeStaticText')
        for filter in filters:
            filter_list.append(filter.text)
            if filter.text == '브랜드':
                filter_break = True
                break
        if filter_break:
            break
        swipe_control(wd, filter_view, "left", 30)
    return filter_list


def check_filter_info(test_result, warning_texts, filter_info_list, compare_filter_list):
    filter_check = filter_info_list
    for filter in filter_check:
        if filter in set(compare_filter_list):
            print(f'{filter} 필터 적용 확인')
        else:
            test_result = 'WARN'
            warning_texts.append('인기 검색어 검색 결과 확인 실패')
            print(f'{filter} 필터 적용 확인 실패: {set(compare_filter_list)}')
    sleep(2)
    return test_result
