from time import sleep
from com_utils.api_control import search_relate_keyword, search_brand_category_info
from com_utils.element_control import aal, aalc, aals, scroll_control, element_scroll_control, swipe_control
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')
    print('뒤로가기 선택')
    sleep(1)


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
        try:
            product_brand = aals(wd, 'brand_name')
            product_brand_name = product_brand[0]
            if product_brand_name.is_displayed():
                product_brand_name = product_brand_name.text
                break
        except NoSuchElementException:
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
        print(f'product_name : {product_name}, compare_name : {compare_name}')
        print('카테고리 필터 적용으로 상품 노출 확인 실패')
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

    sleep(1)

    sticky_mediu_categories = aal(wd, 'com.the29cm.app29cm:id/stickyMediumCategories')

    if sticky_mediu_categories == None:
        aalc(wd, f'c_{medium}')
    else:
        aalc(sticky_mediu_categories, f'c_{medium}')

    sleep(1)

    small_categories = aal(wd, 'com.the29cm.app29cm:id/smallCategories')

    if small_categories == None:
        aalc(wd, f'c_{small}')
    else:
        aalc(small_categories, f'c_{small}')
    sleep(1)


def check_relate_brand_name(wd, compare_brand_name):
    # 확인3-2 : 브랜드 영역에 노출되는 브랜드와 검색한 브랜드명이 동일한지 확인
    brand_layer = aal(wd, 'com.the29cm.app29cm:id/searchResultBrandComposeView')
    relate_brand_name = aal(brand_layer, '//android.view.View/android.view.View[1]/android.widget.TextView[1]').text

    if compare_brand_name in relate_brand_name:
        print('인기 브랜드 검색 확인 - 연관 브랜드')
    else:
        print(f'인기 브랜드 검색 확인 실패 - 연관 브랜드 : 입력-{compare_brand_name} / 노출-{relate_brand_name}')
        raise Exception(f'인기 브랜드 검색 확인 실패 - 연관 브랜드')
