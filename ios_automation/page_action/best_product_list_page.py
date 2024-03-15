from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc
from com_utils.element_control import scroll_control
from ios_automation.page_action.bottom_sheet import pdp_close_bottom_sheet


def click_back_btn(wd):
    ialc(wd, 'navi_back_btn')


# period = 실시간, 일간, 주간, 월간
def click_period_sort(wd, period):
    ialc(wd, f'//XCUIElementTypeButton[@name="{period}"]')


def check_entry_best_plp(wd):
    try:
        ial(wd, '//XCUIElementTypeStaticText[@name="베스트"]')
        print('베스트 PLP 진입 확인')
    except NoSuchElementException:
        print('베스트 PLP 진입 확인 실패')
        raise Exception('베스트 PLP 진입 확인 실패')


def save_best_first_product_name(wd):
    product_name = ial(wd, '//XCUIElementTypeStaticText[@name="product_name"]').text
    return product_name


def save_api_product_name(prefix, product_name):
    if not prefix:
        best_product_name = product_name
    else:
        best_product_name = f'{prefix[0]} {product_name}'
    return best_product_name


def check_best_product_name(compare_name, product_name):
    if compare_name in product_name:
        print('베스트 PLP 상품명 확인')
    else:
        print(f'베스트 PLP 상품명 확인 실패 : {compare_name} / {product_name}')
        raise Exception('베스트 PLP 상품명 확인 실패')


def save_plp_price(wd):
    price = ial(wd, '//XCUIElementTypeStaticText[@name="product_discount_price"]').text
    if '%' in price:
        percent = price.find('%')
        start_index = percent + 2
        end_index = len(price)
        price = price[start_index:end_index].replace('원', '')
    else:
        price = price.replace('원', '')
    price = int(price.replace(',', ''))
    return price


def find_scroll_and_find_product_rank(wd, find_rank):
    rank_break = False
    for i in range(0, 5):
        best = wd.find_elements(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="best_product_rank"]')
        for rank in best:
            best_rank = rank.text
            if best_rank == find_rank:
                rank_break = True
                break
        if rank_break:
            break
        scroll_control(wd, "D", 50)


def check_additional_product(wd, product_name):
    try:
        ial(wd, f'c_{product_name}')
        print('베스트 PLP 상품 추가 노출 확인')
    except NoSuchElementException:
        print('베스트 PLP 상품 추가 노출 확인 실패')
        raise Exception('베스트 PLP 상품 추가 노출 확인 실패')


def click_best_first_product(wd):
    ialc(wd, '//XCUIElementTypeStaticText[@name="product_name"]')
    sleep(1)
    pdp_close_bottom_sheet(wd)


def save_best_product_like_count(wd):
    heart_count = ial(wd, '//XCUIElementTypeButton[@name="like_btn"]').get_attribute('label')
    heart_count = int(heart_count.replace(',', ''))
    return heart_count


def click_best_product_like_btn(wd):
    ialc(wd, '//XCUIElementTypeButton[@name="like_btn"]')
    sleep(1)


def check_increase_like_count(heart_count, heart_select):
    if heart_select == heart_count + 1:
        print('아이템 좋아요 개수 증가 확인')
    else:
        print(f'아이템 좋아요 개수 증가 확인 실패: {heart_count} / {heart_select}')
        raise Exception('아이템 좋아요 개수 증가 확인 실패')


def check_decrease_like_count(heart_count, heart_unselect):
    if heart_unselect == heart_count:
        print('아이템 좋아요 개수 차감 확인')
    else:
        print(f'아이템 좋아요 개수 차감 확인 실패: {heart_count} / {heart_unselect}')
        raise Exception('아이템 좋아요 개수 차감 확인 실패')
