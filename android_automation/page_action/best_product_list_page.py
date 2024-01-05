from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from com_utils.element_control import aal, aalc, aals
from com_utils.element_control import scroll_control


def click_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


# period = 실시간, 일간, 주간, 월간
def click_period_sort(wd, period):
    aalc(wd, f'c_{period}')
    print(f'{period} 선택')


def save_best_first_product_name(wd):
    product_name = aal(wd, 'best_item_title').text
    print(f'{product_name} 필터링 설정 확인')
    return product_name


def check_best_product_name(compare_name, product_name):
    print(f'베스트 PLP 상품명 확인 : {compare_name} / {product_name}')
    if compare_name in product_name:
        print('베스트 PLP 상품명 확인')
    else:
        print(f'베스트 PLP 상품명 확인 실패 : {compare_name} / {product_name}')
        raise Exception('베스트 PLP 상품명 확인 실패')


def check_best_product_page(wd):
    best_page_title = aal(wd, 'com.the29cm.app29cm:id/txtPageTitle')
    if best_page_title == None:
        print("베스트 페이지 진입 확인 실패")
        raise Exception('베스트 페이지 진입 확인 실패')
    else:
        if best_page_title.text == '베스트':
            print("베스트 페이지 진입 확인")
            sleep(1)
        else:
            print("베스트 페이지 진입 확인 실패")
            raise Exception('베스트 페이지 진입 확인 실패')


def save_best_first_product_name(wd):
    sleep(1)
    product_name = aal(wd, 'best_item_title')
    if product_name == None:
        print("요소미발견")
    else:
        product_name = product_name.text
        print(f'product_name : {product_name}')
        return product_name

    # product_name_list = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/contentsDescription"]')
    # print(f'{product_name_list[0].text}')
    # product_name = product_name_list[0].text


def save_best_first_product_price(wd):
    best_product_list_price = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/lastSalePrice"]')
    print(f"베스트 상품 가격 : {best_product_list_price[0].text} ")
    best_product_price = best_product_list_price[0].text
    return best_product_price


def save_best_product_like_count(wd):
    heart_count = aal(wd, 'best_item_like_count')
    if heart_count == None:
        print('요소없음')
    else:
        heart_count = heart_count.text
        heart_count = int(heart_count.replace(',', ''))
        # 문자열을 정수로 변환
        heart_count = int(heart_count)
    return heart_count


def click_best_product_like_btn(wd):
    aalc(wd, 'best_item_like')
    sleep(2)


def click_best_first_product(wd):
    # product_name_list = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/contentsDescription"]')
    # product_name_list[0].click()

    aalc(wd, 'best_item_title')

    sleep(1)
    close_bottom_sheet(wd)


def check_app_evaluation_pop_up_exposure(wd):
    # 앱평가 발생 시 팝업 제거
    app_evaluation = aals(wd, "//*[contains(@text, '29CM 앱을 어떻게 생각하시나요?')]")
    if len(app_evaluation) == 0:
        print("앱 평가 팝업 미발생")
        pass
    else:
        aalc(wd, "//*[contains(@text, '좋아요')]")
        sleep(1)
        aalc(wd, "//*[contains(@text, '나중에 하기')]")
        print("앱 평가 팝업 발생하여 닫기")


def check_increase_like_count(heart_count, heart_select):
    if heart_select == heart_count + 1:
        print('아이템 좋아요 개수 증가 확인')
    else:
        print(f'아이템 좋아요 개수 증가 확인 실패: {heart_count} / {heart_select}')
        raise Exception('아이템 좋아요 개수 증가 확인 실패')


def check_decrease_like_count(heart_count, heart_unselect):
    if heart_unselect == heart_count:
        print('아이템 좋아요 개수 차감 확인')
        sleep(2)
    else:
        print(f'아이템 좋아요 개수 차감 확인 실패: {heart_count} / {heart_unselect}')
        raise Exception('아이템 좋아요 개수 차감 확인 실패')


def save_plp_price(wd):
    price = aal(wd, 'best_item_price')
    if price == None:
        print("요소발견못함")
    else:
        price = price.text
        price = price.replace('원', '')
        price = int(price.replace(',', ''))
        print(f'price : {price}')
    return price


def check_best_product_name(compare_name, product_name):
    if compare_name in product_name:
        print('베스트 PLP 상품명 확인')
    else:
        print(f'베스트 PLP 상품명 확인 실패 : {compare_name} / {product_name}')
        raise Exception('베스트 PLP 상품명 확인 실패')


def find_scroll_and_find_product_rank(wd, text):
    for _ in range(10):
        element = aal(wd, f"//*[contains(@text, '{text}')]")
        if element == None:
            pass
        else:
            print(f"element : {element.text}")
            if element.is_displayed():
                break
        # 요소를 찾지 못하면 아래로 스크롤
        scroll_control(wd, "D", 50)
        sleep(2)


def check_additional_product(wd, product_name):
    element = aal(wd, f"//*[contains(@text, '{product_name}')]")
    if element == None:
        print('베스트 PLP 상품 추가 노출 확인 실패')
        raise Exception('베스트 PLP 상품 추가 노출 확인 실패')
    else:
        print(f"api호출 10번째 아이템명 : {product_name} , 베스트 10위 아이템명 : {element.text}")
        print('베스트 PLP 상품 추가 노출 확인')


def save_api_product_name(prefix, product_name):
    if not prefix:
        best_product_name = product_name
    else:
        best_product_name = f'{prefix[0]} {product_name}'
    print(best_product_name)
    return best_product_name
