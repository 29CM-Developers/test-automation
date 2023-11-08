from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc
from com_utils.element_control import scroll_control


def click_back_btn(wd):
    ialc(wd, 'navi_back_btn')


# period = 실시간, 일간, 주간, 월간
def click_period_sort(wd, period):
    ialc(wd, f'//XCUIElementTypeButton[@name="{period}"]')


def check_entry_best_plp(wd, warning_texts):
    try:
        ial(wd, '//XCUIElementTypeStaticText[@name="베스트"]')
        test_result = 'PASS'
        print('베스트 PLP 진입 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('베스트 PLP 진입 확인 실패')
        print('베스트 PLP 진입 확인 실패')
    return test_result


def save_best_first_product_name(wd):
    product_name = ial(wd, '//XCUIElementTypeStaticText[@name="product_name"]').text
    return product_name


def save_api_product_name(prefix, product_name):
    if not prefix:
        best_product_name = product_name
    else:
        best_product_name = f'{prefix[0]} {product_name}'
    print(best_product_name)
    return best_product_name


def check_best_product_name(warning_texts, compare_name, product_name):
    if compare_name in product_name:
        test_result = 'PASS'
        print('베스트 PLP 상품명 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('베스트 PLP 상품명 확인 실패')
        print(f'베스트 PLP 상품명 확인 실패 : {compare_name} / {product_name}')
    return test_result


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


def check_additional_product(wd, warning_texts, product_name):
    try:
        wd.find_element(AppiumBy.IOS_PREDICATE, f'label == "{product_name}"')
        test_result = 'PASS'
        print('베스트 PLP 상품 추가 노출 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('베스트 PLP 상품 추가 노출 확인 실패')
        print(f'베스트 PLP 상품 추가 노출 확인 실패')
    return test_result


def click_best_first_product(wd):
    ialc(wd, '//XCUIElementTypeStaticText[@name="product_name"]')


def save_best_product_like_count(wd):
    heart_count = ial(wd, '//XCUIElementTypeButton[@name="like_btn"]').get_attribute('label')
    heart_count = int(heart_count.replace(',', ''))
    return heart_count


def click_best_product_like_btn(wd):
    ialc(wd, '//XCUIElementTypeButton[@name="like_btn"]')
    sleep(1)


def check_increase_like_count(warning_texts, heart_count, heart_select):
    if heart_select == heart_count + 1:
        test_result = 'PASS'
        print('아이템 좋아요 개수 증가 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('아이템 좋아요 개수 증가 확인 실패')
        print(f'아이템 좋아요 개수 증가 확인 실패: {heart_count} / {heart_select}')
    return test_result


def check_decrease_like_count(warning_texts, heart_count, heart_unselect):
    if heart_unselect == heart_count:
        test_result = 'PASS'
        print('아이템 좋아요 개수 차감 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('아이템 좋아요 개수 차감 확인 실패')
        print(f'아이템 좋아요 개수 차감 확인 실패: {heart_count} / {heart_unselect}')
    return test_result
