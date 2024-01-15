from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, ials
from ios_automation.page_action.context_change import switch_context


def click_back_btn(wd):
    ialc(wd, 'common back icon black')


def click_coupon_type(wd):
    ialc(wd, '//XCUIElementTypeOther[@name="쿠폰 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeButton[@index="0"]')


def click_option_cart(wd):
    ialc(wd, '//XCUIElementTypeButton[@name="장바구니"]')
    ialc(wd, '확인')


def click_option_product(wd):
    ialc(wd, '//XCUIElementTypeButton[@name="상품"]')
    ialc(wd, '확인')


def save_my_coupon_list(wd):
    switch_context(wd, 'webview')
    coupon_list = []
    try:
        coupon = ials(wd, '//*[contains(@id, "coupon_name")]')
        for name in coupon:
            coupon_name = name.text
            coupon_list.append(coupon_name)
    except NoSuchElementException:
        pass
    switch_context(wd, 'native')
    return coupon_list


def check_coupon_list(wd, api_coupon_list, coupon_list, coupon_type):
    if not coupon_list:
        try:
            ial(wd, '발급 받은 쿠폰이 없습니다.')
            print(f'{coupon_type} 쿠폰 목록 없음 확인')
        except NoSuchElementException:
            print(f'{coupon_type} 쿠폰 목록 확인 실패')
            raise Exception(f'{coupon_type} 쿠폰 목록 확인 실패')
    elif coupon_list == api_coupon_list:
        print(f'{coupon_type} 쿠폰 목록 확인')
    else:
        print(f'{coupon_type} 쿠폰 목록 확인 실패')
        raise Exception(f'{coupon_type} 쿠폰 목록 확인 실패')
