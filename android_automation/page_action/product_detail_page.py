from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException

from android_automation.page_action import context_change
from android_automation.page_action.context_change import change_webview_contexts, change_native_contexts, \
    switch_context
from com_utils.element_control import aal, aalc, aals, aalk, scroll_control
from com_utils.api_control import product_detail, best_plp_women_clothes, product_no_soldout_option


def click_pdp_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')
    print('뒤로가기 선택')


def click_home_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgHome')


def save_remove_prefix_product_name(product_name):
    index = product_name.find(']_')
    if index == -1:
        no_prefix_product_name = product_name
    else:
        start_index = index + 2
        end_index = len(product_name)
        no_prefix_product_name = product_name[start_index:end_index]
    return no_prefix_product_name


# product_name : pdp 상품명
# compare_name: pdp 상품명과 비교한 상품명
def check_product_name(product_name, compare_name):
    product_name = product_name.replace('_', ' ')
    compare_name = compare_name.replace('_', ' ')
    print(f'상품명 - pdp: {product_name} / 비교: {compare_name}')
    if compare_name in product_name:
        print('상품명 동일 확인')
    else:
        print(f'PDP 진입 확인 실패 - pdp: {product_name} / 비교: {compare_name}')
        raise Exception('상품명 동일 확인 실패')


def check_product_name1(product_name, compare_name):
    product_name = product_name.replace('_', ' ')
    compare_name = compare_name.replace('_', ' ')
    print(f'상품명 - pdp: {product_name} / 비교: {compare_name}')
    if compare_name in product_name:
        print('PDP 진입 확인 - 상품명')
    else:
        print(f'PDP 진입 확인 실패 - pdp: {product_name} / 비교: {compare_name}')
        raise Exception('PDP 진입 확인 실패 - 상품명')


def click_purchase_btn(wd):
    aalc(wd, 'c_구매하기')


def click_gift_btn(wd):
    sleep(1)
    aalc(wd, 'c_선물하기')


def click_put_in_cart_btn(wd):
    aalc(wd, 'c_장바구니 담기')


def click_direct_purchase_btn(wd):
    aalc(wd, 'c_바로 구매하기')


def click_direct_gift_btn(wd):
    aalc(wd, 'c_바로 선물하기')


def click_move_to_cart(wd):
    aalc(wd, 'c_바로가기')


def click_like_btn(wd):
    aalc(wd, 'c_찜하기')


# 옵션 존재 여부 확인
def option_exist(product_item_no):
    option_items_list = product_detail(product_item_no)['option_items_list']
    options = '옵션 있음' if option_items_list else '옵션 없음'
    print(options)
    return options


# 옵션 존재 여부와 개수에 따라 옵션 선택
def select_options(wd, product_item_no):
    sleep(1)
    element = aal(wd, '//label[contains(text(), "수량")]')
    if element == None:
        options = '옵션 있음'
    else:
        options = '옵션 없음'
    # 옵션 있을 경우, 옵션 선택
    if options == '옵션 있음':
        option_list = product_no_soldout_option(product_item_no)

        for list, value in option_list.items():
            if list.startswith('layout'):
                aalc(wd, f'//input[@placeholder="{value}"]/..')
            elif list.startswith('option'):
                aalc(wd, f'//li[contains(text(), "{value}")]')
    sleep(1)

    # 텍스트 입력 영역 있을 경우, 텍스트 입력
    text_fild = aal(wd, '//textarea[contains(@class, "css")]')
    if text_fild == None:
        pass
    else:
        aalk(wd, '//textarea[contains(@class, "css")]', '랜덤으로 부탁드려요.')

    sleep(1)

def check_add_product_to_cart(wd):
    element = aal(wd, 'c_장바구니에 상품')
    if element == None:
        print('상품 장바구니 담기 확인 실패')
        raise Exception('상품 장바구니 담기 확인 실패')
    else:
        print('상품 장바구니 담기 확인')


def save_no_soldout_product_no():
    product_item_no = ''
    for i in range(1, 100):
        product_soldout = best_plp_women_clothes(i, 'NOW')['item_soldout']
        if not product_soldout:
            product_item_no = best_plp_women_clothes(i, 'NOW')['item_no']
            print(f'베스트 상품 번호 : {product_item_no}')
            break
    return product_item_no


def save_purchase_price(wd):
    switch_context(wd, 'webview')
    sleep(1)
    price = wd.find_element(AppiumBy.ID, 'total_amount')
    if price == None:
        print('금액 요소 못찾음')
    else:
        price = price.text
        print(f'구매 가능 금액 : {price} 확인')

    price = price.replace('원', '')
    price = int(price.replace(',', ''))
    print(f'구매 가능 가격 : {price}확인')
    change_native_contexts(wd)
    return price


def check_bottom_sheet_title(wd):
    try:
        title1 = aal(wd, 'c_함께 보면 좋은 상품').text
        if title1 == '함께 보면 좋은 상품':
            print('바텀 시트의 함께 보면 좋은 상품 타이틀 비교 확인')
        else:
            print(f'바텀 시트 타이틀 : {title1}')
            raise Exception('바텀 시트의 함께 보면 좋은 상품 타이틀 비교 확인 실패')

        title2 = aal(wd, 'c_다른 고객이 함께 구매한 상품').text
        if title2 == None:
            print('바텀 시트의 다른 고객이 함께 구매한 상품 타이틀 미발생')
            pass
        elif title2 == '다른 고객이 함께 구매한 상품':
            print('바텀 시트의 다른 고객이 함께 구매한 상품 타이틀 비교 확인')
        else:
            print(f'바텀 시트 타이틀 : {title2}')
            raise Exception('바텀 시트의 함께 보면 좋은 상품 타이틀 비교 확인 실패')
    except NoSuchElementException:
        print('바텀 시트의 함께 보면 좋은 상품 타이틀 비교 확인 실패')
        raise Exception('바텀 시트의 함께 보면 좋은 상품 타이틀 비교 확인 실패')

def save_product_name(wd):
    product_name = aal(wd, '//*[@id="pdp_product_name"]')
    if product_name == None:
        scroll_control(wd, 'D', 20)
        product_name = aal(wd, '//*[@id="pdp_product_name"]')

    product_name = aal(wd, '//*[@id="pdp_product_name"]').text
    return product_name
