from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, ials


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
    coupon_list = []
    try:
        coupon = ials(wd,
                      '//XCUIElementTypeOther[@name="쿠폰 - 감도 깊은 취향 셀렉트샵 29CM"]/XCUIElementTypeOther[1]/XCUIElementTypeOther')
        for name in coupon:
            coupon_name = ial(name, '//XCUIElementTypeStaticText[@index="3"]').text
            coupon_list.append(coupon_name)
    except NoSuchElementException:
        pass
    return coupon_list


def check_coupon_list(wd, warning_texts, api_coupon_list, coupon_list, coupon_type):
    if not coupon_list:
        try:
            ial(wd, '발급 받은 쿠폰이 없습니다.')
            test_result = 'PASS'
            print(f'{coupon_type} 쿠폰 목록 없음 확인')
        except NoSuchElementException:
            test_result = 'WARN'
            warning_texts.append(f'{coupon_type} 쿠폰 목록 확인 실패')
            print(f'{coupon_type} 쿠폰 목록 확인 실패')
    elif coupon_list == api_coupon_list:
        test_result = 'PASS'
        print(f'{coupon_type} 쿠폰 목록 확인')
    else:
        test_result = 'WARN'
        warning_texts.append(f'{coupon_type} 쿠폰 목록 확인 실패')
        print(f'{coupon_type} 쿠폰 목록 확인 실패')
    return test_result
