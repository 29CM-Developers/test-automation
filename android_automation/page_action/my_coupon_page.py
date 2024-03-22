from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc, aals
from time import sleep


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


def click_coupon_type(wd):
    sleep(4)
    aalc(wd, 'c_전체 쿠폰')
    print('전체쿠폰 선택')


def click_cart_coupon_type(wd):
    #sleep(1)
    aalc(wd, 'c_장바구니 쿠폰')
    print('장바구니 쿠폰 선택')
    #sleep(1)


def click_option_cart(wd):
    aalc(wd, '//android.widget.Button[@text="장바구니"]')
    print('장바구니 버튼 선택')
    aalc(wd, 'c_확인')


def click_option_product(wd):
    aalc(wd, '//android.widget.Button[@text="상품"]')
    print('상품 버튼 선택')
    aalc(wd, 'c_확인')


def save_my_coupon_list(wd):
    coupon_list = []
    try:
        no_coupon = aal(wd, 'c_발급 받은 쿠폰이 없습니다.')
        if no_coupon != None:
            print("발급 받은 쿠폰이 없습니다 단어를 찾을 수 없습니다.")
            return coupon_list
        coupon_layer = aals(wd, f'//*[@resource-id[contains(., "-slide01")]]')
        for coupon_layer_item in coupon_layer:
            coupon = aal(coupon_layer_item, '//android.widget.TextView[contains(@resource-id, "coupon_name")]')
            if coupon == None:
                print('쿠폰명 찾기 실패 ')
            else:
                full_coupon_name = coupon.text
                print(f'쿠폰 이름 : {full_coupon_name} 확인')
                coupon_list.append(full_coupon_name)
    except NoSuchElementException:
        print('쿠폰명 찾기 실패')
        pass
    return coupon_list


def check_coupon_list(wd, api_coupon_list, coupon_list, coupon_type):
    if not coupon_list:
        try:
            aal(wd, 'c_발급 받은 쿠폰이 없습니다.')
            print(f'{coupon_type} 쿠폰 목록 없음 확인')
        except NoSuchElementException:
            print(f'{coupon_type} 쿠폰 목록 확인 실패')
            raise Exception(f'{coupon_type} 쿠폰 목록 확인 실패')
            print(f'{coupon_type} 쿠폰 목록 확인 실패')
    elif coupon_list == api_coupon_list:
        print(f'{coupon_type} 쿠폰 목록 확인')
    else:
        print(f'{coupon_type} 쿠폰 목록 확인 실패')
        raise Exception(f'{coupon_type} 쿠폰 목록 확인 실패')
