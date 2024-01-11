from time import sleep
from selenium.common import NoSuchElementException
from com_utils import element_control
from com_utils.element_control import aal, aalc, aals


def click_delete_btn_to_first_product(wd):
    # 웹 뷰에서 장바구니 첫번째 상품 삭제
    aalc(wd, '//div[@id="__next"]/div/section[1]/div[2]/div[2]/div/div[2]/button')
    sleep(3)
    print('첫번째 상품 삭제')


def click_to_increase_the_number_of_products(wd):
    # 웹뷰에서 장바구니 첫번째 상품 갯수 증가 선택
    aalc(wd, '//div[@id="__next"]/div/section[1]/div[2]/div[2]/div/div[3]/div/div/button[2]')
    sleep(3)
    print('첫번째 상품 갯수 증가 선택')


def click_check_out_btn(wd):
    sleep(5)
    aalc(wd, 'c_CHECK OUT')
    print('CHECK OUT 선택')
    sleep(5)


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')
    print('뒤로가기 선택')
    sleep(1)


def click_delete_btn_to_all_product(wd):
    # 웹 뷰에서 장바구니 첫번째 상품 삭제
    delete_btn = aal(wd, 'c_선택삭제')
    if delete_btn == None:
        print("장바구니에 담긴 상품 없음")
    else:
        print("장바구니에 담긴 상품 존재")
        aalc(wd, 'c_선택삭제')
        sleep(3)
        print('전체상품삭제')
    click_back_btn(wd)


def click_cart_btn(wd):
    # 웹 뷰에서 장바구니 첫번째 상품 삭제
    aalc(wd, 'com.the29cm.app29cm:id/imgCart')
    print('장바구니 아이콘 선택')
    sleep(2)


def change_webview_contexts(wd):
    # 앱에서 웹뷰로 전환
    webview_contexts = wd.contexts  # 사용 가능한 모든 컨텍스트 가져오기
    print("Available Contexts:", webview_contexts)
    # 웹뷰로 전환
    wd.switch_to.context(webview_contexts[-1])  # 가장 최근의 웹뷰 컨텍스트로 전환
    print(f'wd.current_window_handle : {wd.current_window_handle}')
    print(f'wd.window_handles : {wd.window_handles}')
    print("웹뷰로 전환 성공")
    sleep(4)


def change_native_contexts(wd):
    webview_contexts = wd.contexts  # 사용 가능한 모든 컨텍스트 가져오기
    print("Available Contexts:", webview_contexts)
    # 네이티브로 전환
    wd.switch_to.context('NATIVE_APP')
    print("네이티브 변환 성공")

def change_pinpay_webview_contexts(wd):
    # 앱에서 웹뷰로 전환
    webview_contexts = wd.contexts  # 사용 가능한 모든 컨텍스트 가져오기
    print("Available Contexts:", webview_contexts)
    # 웹뷰로 전환
    wd.switch_to.context(webview_contexts[-1])  # 가장 최근의 웹뷰 컨텍스트로 전환
    print(f'wd.current_window_handle : {wd.current_window_handle}')
    print(f'wd.window_handles : {wd.window_handles}')
    print("웹뷰로 전환 성공")
    sleep(4)

def save_product_price(wd):
    try:
        product_price = aal(wd, '//div[@id="__next"]/div/section[1]/div[2]/div[2]/div/div[4]/div[1]/span')
        product_price = product_price.text
        print(f'product_price : {product_price}')
        price = int(product_price.replace(',', ''))
        print(f'price : {price}')
    except NoSuchElementException:
        pass
    return price


def save_total_price(wd):
    for i in (0, 3):
        try:
            total_order_amount_title_layer = aals(wd, '//*[@id="__next"]/div/section[2]/dl/dt')
            for total_order_amount_title in total_order_amount_title_layer:
                print(f'total_order_amount_title : {total_order_amount_title.text}')
                if total_order_amount_title.text == '총 주문금액':
                    print('총 주문금액 엘리먼트 확인')
                    total_order_amount_title = total_order_amount_title
                    break
            print(f'total_order_amount_title : {total_order_amount_title.text}')
            if total_order_amount_title == None:
                print('요소 발견 못함')
                element_control.scroll_control(wd, 'D', 50)
            else:
                print('요소 발견')
                total_order_price = aal(total_order_amount_title, '//../dd[2]/strong').text
                print(f'total_order_price : {total_order_price}')

                total_order_price = int(total_order_price.replace(',', ''))
                print(f'total_order_price : {total_order_price}')
                break
        except NoSuchElementException:
            element_control.scroll_control(wd, 'D', 30)
            pass
    return total_order_price


def save_product_name_one(wd):
    sleep(3)
    first_product_name = aal(wd, '//div[@id="__next"]/div/section[1]/div[2]/div[2]/div/div[2]/div/div/a').text
    print(f'first_product_name : {first_product_name}')
    return first_product_name


def check_product_name(wd, pdp_name1, pdp_name2):
    sleep(2)
    last_product_name = aal(wd, '//*[@id="__next"]/div/section[1]/div[2]/div[2]/div/div[2]/div/div/a').text
    first_product_name = aal(wd, '//*[@id="__next"]/div/section[1]/div[2]/div[3]/div/div[2]/div/div/a').text

    print(f'last_product_name :{last_product_name}, first_product_name : {first_product_name}')

    if last_product_name == pdp_name2 and first_product_name == pdp_name1:
        print('장바구니 리스트 상품 이름 확인')
    else:
        print(f'장바구니 리스트 상품 이름 확인 실패 :{first_product_name}/{pdp_name1}, {last_product_name}/{pdp_name2}')
        raise Exception('장바구니 리스트 상품 이름 확인 실패')


def check_change_in_number_of_products(wd):
    number_or_products = aal(wd, '//div[@id="__next"]/div/section[1]/div[1]/span/label').text
    # 뒤에서 2번째 문자 추출
    last_second_char = number_or_products[-2]
    # 추출한 문자를 정수로 변환
    products_total_number = int(last_second_char)
    if products_total_number == 1:
        print('주문 상품 수 총 1개로 변경 확인')
    else:
        print(f'주문 상품 수 총 1개로 변경 확인 실패 : {products_total_number}')
        raise Exception('주문 상품 수 총 1개로 변경 확인 실패')


def check_total_order_amount(delete_product_price, before_delete_total_price, after_delete_total_price):
    if before_delete_total_price == after_delete_total_price + delete_product_price:
        print('총 주문금액이 해당 상품의 가격만큼 차감 확인')
    else:
        print(
            f'장바구니 상품 제거 확인 실패 : delete_product_price:{delete_product_price}/ before_delete_total_price:{before_delete_total_price}/after_delete_total_price :{after_delete_total_price}')
        raise Exception('장바구니 상품 제거 확인 실패')


def check_increase_in_product_count(wd):
    sleep(3)
    number_of_products = aal(wd,
                             '//div[@id="__next"]/div/section[1]/div[2]/div[2]/div/div[3]/div/div/input').get_attribute(
        "value")
    # 추출한 문자를 정수로 변환
    number_of_products = int(number_of_products)
    if number_of_products == 2:
        print('주문 상품 수 총 2개로 변경 확인')
    else:
        print(f'주문 상품 수 총 {number_of_products}개로 변경 확인')
        raise Exception('주문 상품 수 총 2개로 변경 확인 실패')


def check_change_total_order_amount(first_product_price, after_delete_total_price):
    if after_delete_total_price == first_product_price * 2:
        print('총 주문금액 변경 확인')
    else:
        print(f'총 주문금액 변경 확인 실패 :{after_delete_total_price}/ {first_product_price}')
        raise Exception('총 주문금액 변경 확인 실패')
