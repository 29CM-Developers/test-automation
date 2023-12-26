from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, ials, element_scroll_control
from com_utils.api_control import product_detail, best_plp_women_clothes
from ios_automation.page_action import context_change


def click_pdp_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()


def click_home_btn(wd):
    ialc(wd, 'common home icon black')


def save_product_name(wd):
    product_name = ial(wd, 'c_감도 깊은 취향 셀렉트샵 29CM').text
    product_name = product_name.replace(' - 감도 깊은 취향 셀렉트샵 29CM', '')
    return product_name


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
    if compare_name in product_name:
        print('PDP 진입 확인 - 상품명')
    else:
        print(f'PDP 진입 확인 실패 - pdp: {product_name} / 비교: {compare_name}')
        raise Exception('PDP 진입 확인 실패 - 상품명')


def save_product_price(wd):
    price = wd.find_element(AppiumBy.CSS_SELECTOR, '[class="css-4bcxzt ent7twr4"]').text
    price = int(price.replace(',', '').replace('원', ''))
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
    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView').click()


def check_open_to_purchase_modal(wd):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니 담기')
        print('PDP 구매하기 모달 노출 확인')
    except NoSuchElementException:
        print('PDP 구매하기 모달 노출 확인')
        raise Exception('PDP 구매하기 모달 노출 확인 실패')


def click_purchase_btn(wd):
    ialc(wd, '구매하기')


def click_gift_btn(wd):
    ialc(wd, '선물하기')


def click_put_in_cart_btn(wd):
    ialc(wd, '장바구니 담기')
    sleep(1)


def click_direct_purchase_btn(wd):
    ialc(wd, '바로 구매하기')
    sleep(1)


def click_direct_gift_btn(wd):
    ialc(wd, '바로 선물하기')
    sleep(1)


def click_move_to_cart(wd):
    wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`label == "바로가기"`]').click()
    sleep(3)


def click_like_btn(wd):
    ialc(wd, '//span[contains(text(), "찜하기")]')


# 옵션 존재 여부와 개수에 따라 옵션 선택
def select_options(wd, product_item_no):
    context_change.switch_context(wd, 'webview')

    try:
        ial(wd, '//label[contains(text(), "수량")]')
        options = '옵션 없음'
    except NoSuchElementException:
        options = '옵션 있음'
    print(f'{options} 확인')

    if options == '옵션 있음':
        option_layout = product_detail(product_item_no)['option_items_layout']
        option_item_list = product_detail(product_item_no)['option_items_list']
        option_name = ''

        for i in range(len(option_layout)):
            ialc(wd, f'//input[@placeholder="{option_layout[i]}"]/..')

            if i < len(option_layout) - 1:
                ialc(wd, f'//li[contains(text(), "{option_item_list[0]["title"]}")]')
                option_item_list = option_item_list[0].get('list', [])
            else:
                for option in option_item_list:
                    if option['limited_qty'] != 0:
                        option_name = option["title"].strip()
                        ialc(wd, f'//li[contains(text(), "{option_name}")]')
                        break
                    else:
                        print(f'{option_name} 옵션 품절 확인')
                        pass
    sleep(1)
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
    xpath_index = ials(wd, '//*[contains(@label, "감도 깊은 취향 셀렉트샵 29CM")]/XCUIElementTypeOther')
    index = ial(wd, '//XCUIElementTypeStaticText[@name="구매 가능 금액"]').get_attribute('index')
    price = ial(wd,
                f'//*[contains(@label, "감도 깊은 취향 셀렉트샵 29CM")]/XCUIElementTypeOther[{len(xpath_index)}]/XCUIElementTypeStaticText[@index="{int(index) + 1}"]').text
    price = int(price.replace(',', ''))
    return price


def move_bottom_sheet(wd, direction):
    element = ial(wd,
                  '//XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]')
    element_scroll_control(wd, element, direction, 40)


def check_like_bottom_sheet(wd):
    try:
        ial(wd, 'c_함께 보면 좋은 상품')
        ial(wd, 'c_다른 고객이 함께 구매한 상품')
        print('추천 상품 바텀 시트 노출 확인')
    except NoSuchElementException:
        print('추천 상품 바텀 시트 노출 확인 실패')
        raise Exception('추천 상품 바텀 시트 노출 확인 실패')
