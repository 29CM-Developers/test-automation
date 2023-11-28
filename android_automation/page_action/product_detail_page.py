from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc, aals
from com_utils.api_control import product_detail, best_plp_women_clothes


def click_pdp_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


def click_home_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgHome')


def save_product_name(wd):
    # 스페셜 오더 상품 확인
    try:
        wd.find_element(AppiumBy.XPATH, "//*[contains(@text, 'SPECIAL-ORDER')]")
        element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=4]'
        print('SPECIAL-ORDER 상품 발견')
    except NoSuchElementException:
        print('SPECIAL-ORDER 상품 미발견')
        element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=5]'
        pass
    # 이굿 위크 상품 확인
    try:
        sale_tag = aal(wd, '이굿위크 할인 상품')
        if sale_tag == None:
            element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=3]'
            print('sale_tag 상품 ㅁㅣ발견')
        else:
            element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=5]'
            print('sale_tag 상품 발견')
    except NoSuchElementException:
        print('sale_tag 상품 미발견')
        element_xpath = '//android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.widget.TextView[@index=3]'
        pass

    PDP_product_title = wd.find_element(AppiumBy.XPATH, element_xpath).text
    print(f'PDP 상품명 : {PDP_product_title}')
    return PDP_product_title


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
        print('상품명 동일 확인')
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
    aalc(wd, 'c_구매하기')


def click_gift_btn(wd):
    aalc(wd, 'c_선물하기')
    sleep(1)


def click_put_in_cart_btn(wd):
    aalc(wd, 'c_장바구니 담기')
    sleep(1)


def click_direct_purchase_btn(wd):
    aalc(wd, '바로 구매하기')
    sleep(1)


def click_direct_gift_btn(wd):
    sleep(3)
    aalc(wd, 'c_바로 선물하기')
    sleep(1)


def click_move_to_cart(wd):
    aalc(wd, f'c_바로가기')


def click_like_btn(wd):
    sleep(1)
    aalc(wd, 'c_찜하기')
    sleep(5)

# 옵션 존재 여부 확인
def option_exist(product_item_no):
    option_items_list = product_detail(product_item_no)['option_items_list']
    options = '옵션 있음' if option_items_list else '옵션 없음'
    print(options)
    return options


# 옵션 존재 여부와 개수에 따라 옵션 선택
def select_options(wd, product_item_no):
    sleep(5)
    exist = option_exist(product_item_no)
    if exist == '옵션 있음':
        option_layout = product_detail(product_item_no)['option_items_layout']
        option_item_list = product_detail(product_item_no)['option_items_list']
        option_name = ''
        print(f'option_layout : {option_layout}')

        for i in range(len(option_layout)):
            print(f'{i + 1}/{len(option_layout)}')
            sleep(2)
            # aalc(wd, f'c_{option_layout[i]}"]')
            opthios_layer = aal(wd,
                                '//androidx.drawerlayout.widget.DrawerLayout/android.view.ViewGroup/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View/android.view.View')
            print(f'opthins_layer', opthios_layer)
            opthios_layer1 = aal(opthios_layer, '//android.widget.Button')
            aalc(opthios_layer, "//android.widget.Button")
            sleep(5)
            print(f'opthins_layer1 : {opthios_layer1}')

            print(f'항목 : {option_layout[i]}')

            if i < len(option_layout) - 1:
                aalc(opthios_layer1, f'c_{option_item_list[0]["title"]}"]')
                print(f'옵션1 : {option_item_list[0]["title"]}')
                option_item_list = option_item_list[0].get('list', [])
            else:
                for option in option_item_list:
                    if option['limited_qty'] != 0:
                        option_name = option["title"].strip()

                        print(f'옵션2 : {option_name}')
                        opthios_layer2 = aals(opthios_layer, '//android.widget.Button[@index=1]')
                        print(f'opthios_layer2 : {opthios_layer2}')
                        # aalc(opthios_layer, '//android.widget.Button[2]')
                        aalc(wd, f'c_{option_name}')
                        break
                    else:
                        print(f'{option_name} 옵션 품절')
                        pass
    sleep(1)


def check_add_product_to_cart(wd, warning_texts):
    try:
        aal(wd, 'c_장바구니에 상품')
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
    amount_available_for_purchase_elemenent = aal(wd, f'c_구매 가능 금액')
    print(amount_available_for_purchase_elemenent.text)
    # 예시로 XPath를 사용하여 특정 엘리먼트를 찾음
    # 부모 엘리먼트를 찾음
    parent_element = wd.find_element(AppiumBy.XPATH, "//*[contains(@text, '구매 가능 금액')]/..")  # ".."은 상위 엘리먼트를 나타냄
    print(f'parent_element : {parent_element}')
    # 부모의 자식 엘리먼트들을 모두 찾은 후에, 형제 엘리먼트를 찾음
    amount_available_for_purchase = aals(parent_element, '//android.widget.TextView')
    for i in range(len(amount_available_for_purchase)):
        print(f'amount_available_for_purchase : {amount_available_for_purchase[i].text}')
        if amount_available_for_purchase[i].text == '구매 가능 금액':
            price = amount_available_for_purchase[i + 1].text
            print(f'구매 가능 가격 : {price}')
            break
    print(f'구매 가능 가격 : {price}')
    price = int(price.replace(',', ''))
    print(f'구매 가능 가격 : {price}')
    return price


def check_bottom_sheet_title(wd, warning_texts):
    try:
        title1 = aal(wd, 'c_함께 보면 좋은 상품').text
        if title1 == '함께 보면 좋은 상품':
            test_result = 'PASS'
            print('바텀 시트의 함께 보면 좋은 상품 타이틀 비교 확인')
        else:
            print(f'바텀 시트 타이틀 : {title1}')
            test_result = 'WARN'
            warning_texts.append('바텀 시트의 함께 보면 좋은 상품 타이틀 비교 확인 실패')

        title2 = aal(wd, 'c_다른 고객이 함께 구매한 상품').text
        if title2 == None:
            print('바텀 시트의 다른 고객이 함께 구매한 상품 타이틀 미발생')
            pass
        elif title2 == '다른 고객이 함께 구매한 상품':
            test_result = 'PASS'
            print('바텀 시트의 다른 고객이 함께 구매한 상품 타이틀 비교 확인')
        else:
            print(f'바텀 시트 타이틀 : {title2}')
            test_result = 'WARN'
            warning_texts.append('바텀 시트의 바텀 시트의 다른 고객이 함께 구매한 상품 타이틀 비교 확인 타이틀 비교 확인 실패')
    except NoSuchElementException:
        print('NoSuchElementException')
        test_result = 'WARN'
        warning_texts.append('바텀 시트의 함께 보면 좋은 상품 타이틀 비교 확인 실패')
        print('바텀 시트의 함께 보면 좋은 상품 타이틀 비교 확인 실패')
    return test_result
