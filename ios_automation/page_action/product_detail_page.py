from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, ials
from com_utils.api_control import product_detail, best_plp_women_clothes


def click_pdp_back_btn(wd):
    wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'common back icon black').click()


def click_home_btn(wd):
    ialc(wd, 'common home icon black')


def save_product_name(wd):
    product_name = ial(wd, 'c_감도 깊은 취향 셀렉트샵 29CM').text
    product_name = product_name.replace(' - 감도 깊은 취향 셀렉트샵 29CM', '')
    print(f'PDP 상품명 : {product_name}')
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
def check_product_name(warning_texts, product_name, compare_name):
    if compare_name in product_name:
        test_result = 'PASS'
        print('PDP 진입 확인 - 상품명')
    else:
        test_result = 'WARN'
        warning_texts.append('PDP 진입 확인 실패')
        print(f'PDP 진입 확인 실패 - pdp: {product_name} / 비교: {compare_name}')
    return test_result


def close_purchase_modal(wd):
    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeWebView').click()


def check_open_to_purchase_modal(wd, warning_texts):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '장바구니 담기')
        test_result = 'PASS'
        print('PDP 구매하기 모달 노출 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('PDP 구매하기 모달 노출 확인 실패')
        print('PDP 구매하기 모달 노출 확인')
    return test_result


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


# 옵션 존재 여부 확인
def option_exist(product_item_no):
    option_items_list = product_detail(product_item_no)['option_items_list']
    options = '옵션 있음' if option_items_list else '옵션 없음'
    print(options)
    return options


# 옵션 존재 여부와 개수에 따라 옵션 선택
def select_options(wd, product_item_no):
    exist = option_exist(product_item_no)
    if exist == '옵션 있음':
        option_layout = product_detail(product_item_no)['option_items_layout']
        option_item_list = product_detail(product_item_no)['option_items_list']
        option_name = ''

        for i in range(len(option_layout)):
            print(f'{i + 1}/{len(option_layout)}')
            ialc(wd, f'//XCUIElementTypeButton[@name="{option_layout[i]}"]')
            print(f'항목 : {option_layout[i]}')

            if i < len(option_layout) - 1:
                ialc(wd, f'//XCUIElementTypeButton[@name="{option_item_list[0]["title"]}"]')
                print(f'옵션 : {option_item_list[0]["title"]}')
                option_item_list = option_item_list[0].get('list', [])
            else:
                for option in option_item_list:
                    if option['limited_qty'] != 0:
                        option_name = option["title"].strip()
                        print(f'옵션 : {option_name}')
                        ialc(wd, f'//XCUIElementTypeButton[@name="{option_name}"]')
                        break
                    else:
                        print(f'{option_name} 옵션 품절')
                        pass
    sleep(1)


def check_add_product_to_cart(wd, warning_texts):
    try:
        ial(wd, 'c_장바구니에 상품')
        test_result = 'PASS'
        print('상품 장바구니 담기 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('상품 장바구니 담기 확인 실패')
        print('상품 장바구니 담기 확인 실패')
    return test_result


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
    xpath_index = ials(wd, '//*[contains(@label, "감도 깊은 취향 셀렉트샵 29CM")]/XCUIElementTypeOther')
    index = ial(wd, '//XCUIElementTypeStaticText[@name="구매 가능 금액"]').get_attribute('index')
    price = ial(wd,
                f'//*[contains(@label, "감도 깊은 취향 셀렉트샵 29CM")]/XCUIElementTypeOther[{len(xpath_index)}]/XCUIElementTypeStaticText[@index="{int(index) + 1}"]').text
    price = int(price.replace(',', ''))
    print(f'구매 가능 가격 : {price}')
    return price
