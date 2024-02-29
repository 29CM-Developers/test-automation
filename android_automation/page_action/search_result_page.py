from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from com_utils.api_control import search_relate_keyword, search_brand_category_info
from com_utils.element_control import aal, aalc, aals, scroll_control, swipe_control
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')
    print('뒤로가기 선택')


def check_input_field(wd, keyword):
    # 확인3-1 : 선택한 브랜드명과 입력란에 작성된 문구가 동일한지 확인
    search_input_field = aal(wd, 'com.the29cm.app29cm:id/searchEditText').text
    if keyword in search_input_field:
        print('인기 검색어 검색 확인 - 입력란')
    else:
        print(f'인기 브랜드 검색 결과 확인 실패 : 입력-{keyword} / 노출-{search_input_field}')
        raise Exception(f'인기 브랜드 검색 결과 확인 실패')


def check_product_brand_name(wd, compare_brand_name):
    product_brand_name = ''
    for i in range(0, 3):
        product_brand = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/brandName"]')
        if product_brand == None:
            pass
        else:
            product_brand_name = product_brand[0].text
            break
        scroll_control(wd, 'D', 30)

    if compare_brand_name == product_brand_name:
        print('인기 브랜드 검색 상품 확인 - 상품 브랜드')
    else:
        print(f'인기 브랜드 검색 상품 확인 실패: 검색어-{compare_brand_name} / 상품 브랜드-{product_brand_name}')
        raise Exception(f'인기 브랜드 검색 상품 확인 실패')


def check_search_product_name(wd, compare_name):
    product_name = ''
    for i in range(0, 3):
        try:
            product_name = aal(wd, '//*[@resource-id="com.the29cm.app29cm:id/contentsDescription"]')
            if product_name == None:
                scroll_control(wd, 'D', 30)
            else:
                product_name = product_name.text
                break
        except NoSuchElementException:
            scroll_control(wd, 'D', 30)

    if compare_name in product_name:
        print('카테고리 필터 적용으로 상품 노출 확인')
    else:
        print(f'카테고리 필터 적용으로 상품 노출 확인 실패 {product_name}/ {compare_name}')
        raise Exception('카테고리 필터 적용으로 상품 노출 확인 실패')


def click_brand_category(wd, keyword):
    category_name = search_brand_category_info(keyword)
    large = category_name['large_name']
    medium = category_name['medium_name']
    small = category_name['small_name']

    sticky_large_categories = aal(wd, 'com.the29cm.app29cm:id/stickyLargeCategories')

    if sticky_large_categories == None:
        aalc(wd, f'c_{large}')
    else:
        aalc(sticky_large_categories, f'c_{large}')

    sticky_mediu_categories = aal(wd, 'com.the29cm.app29cm:id/stickyMediumCategories')

    if sticky_mediu_categories == None:
        aalc(wd, f'c_{medium}')
    else:
        aalc(sticky_mediu_categories, f'c_{medium}')

    small_categories = aal(wd, 'com.the29cm.app29cm:id/smallCategories')

    if small_categories == None:
        aalc(wd, f'c_{small}')
    else:
        aalc(small_categories, f'c_{small}')


def check_relate_brand_name(wd, compare_brand_name):
    # 확인3-2 : 브랜드 영역에 노출되는 브랜드와 검색한 브랜드명이 동일한지 확인
    brand_layer = aal(wd, 'com.the29cm.app29cm:id/searchResultBrandComposeView')
    relate_brand_name = aal(brand_layer, '//android.view.View/android.view.View[1]/android.widget.TextView[1]').text

    if compare_brand_name in relate_brand_name:
        print('인기 브랜드 검색 확인 - 연관 브랜드')
    else:
        print(f'인기 브랜드 검색 확인 실패 - 연관 브랜드 : 입력-{compare_brand_name} / 노출-{relate_brand_name}')
        raise Exception(f'인기 브랜드 검색 확인 실패 - 연관 브랜드')


def check_relate_keyword(wd, api_keyword_1st):
    # 연관 검색어 리스트 API 호출
    relate_keyword_list = search_relate_keyword(api_keyword_1st)
    print(f'relate_keyword_list : {relate_keyword_list}')

    if not relate_keyword_list:
        check_input_field(wd, api_keyword_1st)
    else:
        related_1st_keyword = relate_keyword_list[0]
        related_keyword_layer = aal(wd, 'com.the29cm.app29cm:id/relatedKeywordComposeView')
        related_keyword_1st = aal(related_keyword_layer,
                                  '//android.view.View/android.view.View/android.widget.TextView[1]').text
        if related_keyword_1st in related_1st_keyword:
            print('인기 검색어 검색 확인 - 연관 검색어')
        else:
            print(f'인기 검색어 검색 결과 확인 실패 : {related_keyword_1st} / {api_keyword_1st}')
            raise Exception('인기 검색어 검색 결과 확인 실패')


def click_sort_filter_btn(wd, sort):
    selector_layer = aal(wd, 'com.the29cm.app29cm:id/facetGroup')
    selector = aal(selector_layer, '//android.view.View/android.view.View/android.view.View[1]/android.widget.TextView')
    selector.click()
    bottom_sheet_layer = aal(wd, 'com.the29cm.app29cm:id/design_bottom_sheet')
    filter_by_sales = aal(bottom_sheet_layer, f'c_{sort}')

    filter_by_sales_name = filter_by_sales.text
    filter_by_sales.click()
    print(f'정렬 : {sort} 선택')
    if selector.text in filter_by_sales_name:
        print("판매순 정렬 변경 확인")
    else:
        print("판매순 정렬 변경 확인 실패")
        raise Exception('판매순 정렬 변경 확인 실패')


def click_color_filter(self, wd, color):
    selector_layer = aal(wd, 'com.the29cm.app29cm:id/facetGroup')
    aalc(selector_layer, f'c_{self.conf["search_filter"]["color"]}')
    sleep(1)
    aalc(wd, f"c_{color}")
    print(f'color : {color} 선택')


def click_category_filter(wd, category):
    aalc(wd, 'category_filter_layer')
    aalc(wd, f"c_{category}")
    print(f'필터 - 카테고리 : {category} 선택')


def click_price_range_filter(wd, price_range):
    aalc(wd, 'price_range')
    aalc(wd, f"c_{price_range}")


def click_product_info_filter(wd, product_info):
    aalc(wd, 'product_information')
    aalc(wd, f"c_{product_info}")


def click_apply_filter_btn(wd):
    # aalc(wd, 'com.the29cm.app29cm:id/confirm')
    aalc(wd, f'c_개의 상품보기')


def save_filter_info(wd, filter_list):
    print(f'filter_list : {filter_list}')
    filter_list_set = []
    filter_layer = aal(wd, 'com.the29cm.app29cm:id/facetGroup')
    for filter in filter_list:
        element = aal(filter_layer, f'c_{filter}')
        if element == None:
            if filter == '5만원 ~ 10만원':
                price = '50,000원 ~ 100,000원'
                element = aal(filter_layer, f'c_{price}')
            else:
                swipe_control(wd, filter_layer, 'left', 80)
                element = aal(filter_layer, f'c_{filter}')
        print(f'element.text : {element.text}')
        filter_list_set.append(element.text)

    return filter_list_set


def check_filter_info(self, wd, to_be_filter_list):
    selector_layer = aal(wd, 'com.the29cm.app29cm:id/facetGroup')
    element = aal(selector_layer, f'c_{to_be_filter_list[1]}')
    if '블랙' in element.text:
        print("블랙 필터링 노출 확인")
    else:
        print("블랙 필터링 노출 확인 불가")
        raise Exception('인기 검색어 검색 결과 확인 실패')
    element = aal(selector_layer, f'c_{to_be_filter_list[2]}')
    if '여성의류' in element.text:
        print("여성의류 필터링 노출 확인")
    else:
        print("여성의류 필터링 노출 확인 실패")
        raise Exception('인기 검색어 검색 결과 확인 실패')
    swipe_control(wd, selector_layer, 'left', 30)
    element = aal(selector_layer, f'c_50,000원 ~ 100,000원')
    if '50,000원 ~ 100,000원' in element.text:
        print("50,000원 ~ 100,000원 필터링 노출 확인")
    else:
        print("50,000원 ~ 100,000원 필터링 노출 확인 실패")
        raise Exception('인기 검색어 검색 결과 확인 실패')
    swipe_control(wd, selector_layer, 'left', 40)
    swipe_control(wd, selector_layer, 'left', 40)
    element = aals(wd, 'c_품절상품 제외')
    if '품절상품 제외' in element[0].text:
        print("품절상품 제외 필터링 노출 확인")
    else:
        print("품절상품 제외 필터링 노출 확인 실패")
        raise Exception('인기 검색어 검색 결과 확인 실패')


def save_filter_reseult_info(self, wd):
    filter_list = []
    filter_list.append(self.conf["sort"]["order"])
    filter_list.append(self.conf["search_filter"]["black"])
    filter_list.append(self.conf["search_filter"]["woman_clothes"])
    filter_list.append(self.conf["search_filter"]["5to10"])
    filter_list.append(self.conf["search_filter"]["excludingout_of_stock_products"])
    return filter_list
