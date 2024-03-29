from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, ialk, element_scroll_control, tap_control
from com_utils.api_control import best_plp_women_clothes, product_no_soldout_option
from ios_automation.page_action import context_change


def click_pdp_back_btn(wd):
    ialc(wd, 'common back icon black')


def click_home_btn(wd):
    ialc(wd, 'common home icon black')


def save_product_name(wd):
    context_change.switch_context(wd, 'webview')
    product_name = ial(wd, '//*[@id="pdp_product_name"]').text
    context_change.switch_context(wd, 'native')
    return product_name


def save_remove_prefix_product_name(wd):
    product_name = save_product_name(wd)
    index = product_name.find(']_')
    if index == -1:
        no_prefix_product_name = product_name
    else:
        start_index = index + 2
        end_index = len(product_name)
        no_prefix_product_name = product_name[start_index:end_index]
    return no_prefix_product_name


def remove_prefix_product_name(product_name):
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
    product_name = ' '.join(product_name.split())
    compare_name = ' '.join(compare_name.split())
    if compare_name in product_name:
        print('PDP 진입 확인 - 상품명')
    else:
        print(f'PDP 진입 확인 실패 - pdp: {product_name} / 비교: {compare_name}')
        raise Exception('PDP 진입 확인 실패 - 상품명')


# product_name : pdp 상품명
# compare_name: pdp 상품명과 비교한 상품명
# 말머리 제외하고 상품명 비교 필요 (베스트 plp와 비교)
def check_prefix_product_name(product_name, compare_name):
    compare_name = remove_prefix_product_name(compare_name)
    compare_name = ' '.join(compare_name.split())
    if product_name in compare_name:
        print('PDP 진입 확인 - 상품명')
    else:
        print(f'PDP 진입 확인 실패 - pdp: {product_name} / 비교: {compare_name}')
        raise Exception('PDP 진입 확인 실패 - 상품명')


def save_product_price(wd):
    context_change.switch_context(wd, 'webview')
    price = ial(wd, '//*[@id="pdp_product_price"]').text
    price = int(price.replace(',', '').replace('원', ''))
    context_change.switch_context(wd, 'native')
    return price


# product_price : pdp 상품 가격
# compare_name: pdp 상품 가격과 비교할 상품 가격
def check_product_price(product_price, compare_price):
    if compare_price == product_price:
        print('PDP 진입 확인 - 상품가격')
    else:
        print(f'PDP 진입 확인 실패 - pdp: {product_price} / 비교: {compare_price}')
        raise Exception('PDP 진입 확인 실패 - 상품가격')


def close_purchase_modal(wd):
    tap_control(wd)


def check_open_to_purchase_modal(wd):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니 담기')
        print('PDP 구매하기 모달 노출 확인')
    except NoSuchElementException:
        print('PDP 구매하기 모달 노출 확인')
        raise Exception('PDP 구매하기 모달 노출 확인 실패')


def click_purchase_btn(wd):
    context_change.switch_context(wd, 'webview')
    ialc(wd, '//*[@id="cta_purchase"]')
    context_change.switch_context(wd, 'native')


def click_gift_btn(wd):
    context_change.switch_context(wd, 'webview')
    ialc(wd, '//*[@id="cta_gift_button"]')
    context_change.switch_context(wd, 'native')


def click_put_in_cart_btn(wd):
    context_change.switch_context(wd, 'webview')
    ialc(wd, '//*[@id="pdp_shopping_basket"]')
    context_change.switch_context(wd, 'native')
    sleep(1)


def click_direct_purchase_btn(wd):
    context_change.switch_context(wd, 'webview')
    ialc(wd, '//*[@id="pdp_buy_now"]')
    context_change.switch_context(wd, 'native')
    sleep(1)


def click_direct_gift_btn(wd):
    ialc(wd, '바로 선물하기')
    sleep(1)


def click_move_to_cart(wd):
    ialc(wd, '**/XCUIElementTypeStaticText[`label == "바로가기"`]')
    sleep(3)


def click_like_btn(wd):
    context_change.switch_context(wd, 'webview')
    ialc(wd, '//*[@id="cta_heart_button"]')
    context_change.switch_context(wd, 'native')
    sleep(1)


def click_share_btn(wd):
    context_change.switch_context(wd, 'webview')
    ialc(wd, '//*[@id="cta_shared_button"]')
    context_change.switch_context(wd, 'native')
    sleep(1)


# 옵션 존재 여부와 개수에 따라 옵션 선택
def select_options(wd, product_item_no):
    context_change.switch_context(wd, 'webview')

    try:
        ial(wd, '//label[contains(text(), "수량")]')
        options = '옵션 없음'
    except NoSuchElementException:
        options = '옵션 있음'

    # 옵션 있을 경우, 옵션 선택
    if options == '옵션 있음':
        option_list = product_no_soldout_option(product_item_no)

        for list, value in option_list.items():
            if list.startswith('layout'):
                ialc(wd, f'//input[@placeholder="{value}"]/..')
            elif list.startswith('option'):
                ialc(wd, f'//li[text()="{value}"]')
    sleep(1)

    # 텍스트 입력 영역 있을 경우, 텍스트 입력
    try:
        ialk(wd, '//textarea[contains(@class, "css")]', '랜덤으로 부탁드려요.')
    except NoSuchElementException:
        pass

    context_change.switch_context(wd, 'native')


def check_add_product_to_cart(wd):
    try:
        ial(wd, 'c_장바구니에 상품')
        print('상품 장바구니 담기 확인')
    except NoSuchElementException:
        print('상품 장바구니 담기 확인 실패')
        raise Exception('상품 장바구니 담기 확인 실패')


def save_no_soldout_product_no():
    product_item_no = ''
    for i in range(1, 100):
        product_soldout = best_plp_women_clothes(i, 'NOW')['item_soldout']
        if not product_soldout:
            product_item_no = best_plp_women_clothes(i, 'NOW')['item_no']
            break
    return product_item_no


def save_purchase_price(wd):
    sleep(1)
    context_change.switch_context(wd, 'webview')
    price = ial(wd, '//*[@id="total_amount"]').text
    context_change.switch_context(wd, 'native')
    price = int(price.replace(',', '').replace('원', ''))
    return price


def move_like_bottom_sheet(wd, direction):
    element = ial(wd,
                  '//*[@name="함께 보면 좋은 상품"]/ancestor::XCUIElementTypeCollectionView/../preceding-sibling::XCUIElementTypeOther')
    element_scroll_control(wd, element, direction, 40)


def check_like_bottom_sheet(wd):
    try:
        ial(wd, 'c_함께 보면 좋은 상품')
        ial(wd, 'c_다른 고객이 함께 구매한 상품')
        print('추천 상품 바텀 시트 노출 확인')
    except NoSuchElementException:
        print('추천 상품 바텀 시트 노출 확인 실패')
        raise Exception('추천 상품 바텀 시트 노출 확인 실패')


def click_link_copy_btn(wd):
    ialc(wd, 'c_Copy')
