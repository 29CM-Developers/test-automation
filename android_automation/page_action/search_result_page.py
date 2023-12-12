from time import sleep
from com_utils.api_control import search_relate_keyword, search_brand_category_info
from com_utils.element_control import aal, aalc, aals, scroll_control, element_scroll_control, swipe_control
from selenium.common import NoSuchElementException


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


def check_input_field(wd, keyword):
    search_input_field = aal(wd, 'input_keyword').text
    if search_input_field == keyword:
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
            product_name = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/contentsDescription"]')
            if product_name == None:
                scroll_control(wd, 'D', 30)
            else:
                product_name = product_name[0].text
                break
        except NoSuchElementException:
            scroll_control(wd, 'D', 30)

    if product_name == compare_name:
        print('카테고리 필터 적용으로 상품 노출 확인')
    else:
        print('카테고리 필터 적용으로 상품 노출 확인 실패')
        raise Exception('카테고리 필터 적용으로 상품 노출 확인 실패')


def click_brand_category(wd, keyword):
    category_name = search_brand_category_info(keyword)

    large = category_name['large_name']
    aalc(wd, f'c_{large}')
    sleep(1)

    medium = category_name['medium_name']
    aalc(wd, f'c_{medium}')
    sleep(1)

    small = category_name['small_name']
    aalc(wd, f'c_{small}')
    sleep(1)
