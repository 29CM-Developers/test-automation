from selenium.common import NoSuchElementException
from time import sleep
from android_automation.page_action import navigation_bar
from com_utils.element_control import aal, aalc, aals, swipe_control, element_scroll_control, scroll_control


def click_pin_menu(wd, find_menu):
    sleep(3)
    pin_menu_layer = aal(wd, 'com.the29cm.app29cm:id/shopComposeView')
    pin_menu_list = aal(pin_menu_layer, '//android.view.View/android.view.View[1]')
    click_break = False
    for i in range(0, 5):
        try:
            pin_menu_title = aal(wd, 'c_WELOVE')
            if pin_menu_title == None:
                swipe_control(wd, pin_menu_list, 'left', 50)
            elif pin_menu_title.text == find_menu:
                click_break = True
                # sleep(2)
                pin_menu_title.click()
                sleep(2)
        except NoSuchElementException:
            swipe_control(wd, pin_menu_list, 'left', 50)
            pass
        if click_break:
            break


def click_best_category(wd):
    aalc(wd, 'best_title')
    print("홈 > 카테고리 > 의류 > 베스트 선택")


def click_category_top(wd):
    aalc(wd, 'top_title')
    print("홈 > 카테고리 PLP 진입 > 의류 > 상의 선택")


def click_not_login_user_product_like_btn(wd):
    plp_layer = aal(wd, 'com.the29cm.app29cm:id/recyclerview')
    aalc(plp_layer, '//android.view.ViewGroup[1]/android.widget.ImageView[2]')
    print("좋아요 선택")


def click_for_you_category(wd):
    aalc(wd, 'for_you_title')
    print("for you 선택")


def check_not_login_user_recommended_tab(wd):
    # 추천 확인 추가
    recommend_title = aal(wd, 'c_당신을 위한 추천')
    if recommend_title == None:
        print('비로그인 유저 추천 페이지 타이틀 확인 실패')
        raise Exception('비로그인 유저 추천 페이지 타이틀 확인 실패')
    else:
        print('비로그인 유저 추천 페이지 타이틀 확인')


def click_back_btn(wd):
    # 뒤로가기로 카테고리 화면 진입
    top_menu = aal(wd, 'com.the29cm.app29cm:id/topMenu')
    aalc(top_menu, '//android.view.View/android.view.View')


def check_large_category_list(wd, api_large_categoty_list):
    # api에서 호출한 리스트 길이와 비교하여 노출되는 대 카테고리 리스트 저장
    large_list = []
    category_layer = aal(wd, 'com.the29cm.app29cm:id/shopComposeView')

    large_list.append(aal(wd, 'category_first_title').text)
    large_list.append(
        aal(category_layer, '//android.view.View/android.view.View[2]/android.widget.TextView[2]').text)
    large_list.append(
        aal(category_layer, '//android.view.View/android.view.View[2]/android.widget.TextView[3]').text)

    if set(large_list).intersection(api_large_categoty_list):
        print('대 카테고리 리스트 확인')
    else:
        print(f'대 카테고리 리스트 확인 실패 - {api_large_categoty_list} / {large_list} ')
        raise Exception('대 카테고리 리스트 확인 실패')


def scroll_up_large_category(wd):
    large_field = aal(wd, 'large_category_list')
    element_scroll_control(wd, large_field, 'U', 30)


def click_category(wd, category_name):
    category_layer = aal(wd, 'com.the29cm.app29cm:id/shopComposeView')
    aalc(category_layer, category_name)


def check_category_page_shose_title(wd, category_name):
    page_title = aal(wd, 'com.the29cm.app29cm:id/txtCategoryName')
    if page_title == None:
        print(f'{category_name} 카테고리 PLP 진입 확인 실패')
        raise Exception(f'{category_name} 카테고리 PLP 진입 확인 실패')
    if '신발' in page_title.text:
        print('카테고리 전체 페이지 진입 확인')
        print(f'{category_name} 카테고리 PLP 진입 확인')
    else:
        print(f'{category_name} 카테고리 PLP 진입 확인 실패')
        raise Exception(f'{category_name} 카테고리 PLP 진입 확인 실패')


def check_category_page_sandal_title(wd):
    page_title = aal(wd, 'com.the29cm.app29cm:id/mediumCategory')
    if page_title == None:
        print(f'카테고리 샌들 PLP 진입 확인 실패')
        raise Exception(f'샌들 카테고리 PLP 진입 확인 실패')
    elif '샌들' in page_title.text:
        print(f'카테고리 샌들 PLP 진입 확인')
    else:
        print(f'카테고리 샌들 PLP 진입 확인 실패')
        raise Exception(f'카테고리 샌들 PLP 진입 확인 실패')


def save_webview_category_product_name(wd, first_product_name):
    for _ in range(10):
        try:
            element = aal(wd, f"c_{first_product_name}")
            print(f"element : {element.text}")
            if element.is_displayed():
                print("아이템 발견")
                return element.text
        except:
            pass
        # 요소를 찾지 못하면 아래로 스크롤
        scroll_control(wd, "D", 50)


def check_category_product_name(plp_name, compare_name):
    if plp_name in compare_name:
        print('카테고리 페이지의 상품 확인')
    else:
        print(f'카테고리 페이지의 상품 확인 실패 :{compare_name}/{plp_name}')
        raise Exception('카테고리 페이지의 상품 확인 실패')


def scroll_up_to_category(wd, element_id):
    for _ in range(10):
        element = aal(wd, element_id)
        if element == None:
            pass
        elif element.is_displayed():
            print(f"element : {element.get_attribute('content-desc')}")
            scroll_control(wd, "U", 30)
            return element
        # 요소를 찾지 못하면 아래로 스크롤
        scroll_control(wd, "U", 30)


def click_filter_by_new(wd):
    selector = aal(wd, 'plp_filter_sort')
    aalc(wd, 'plp_filter_sort')
    buttom_layer = aal(wd, 'com.the29cm.app29cm:id/design_bottom_sheet')
    new_product_order = aal(buttom_layer,
                            '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[2]/android.widget.TextView')
    new_product_order.click()
    print(f"정렬 : {selector.text}")
    if '신상품순' in selector.text:
        print(f"정렬 확인 : {selector.text}")
    else:
        print(f"정렬 확인 실패 : {selector.text}")
        raise Exception('카테고리 페이지의 상품 정렬 확인 실패')


def save_category_product_name(wd, text):
    for _ in range(10):
        element = aal(wd, f"//*[contains(@text, '{text}')]")
        if element == None:
            pass
        elif element.is_displayed():
            print("아이템 발견")
            print(f"element : {element.text}")
            return element.text

        # 요소를 찾지 못하면 아래로 스크롤
        scroll_control(wd, "D", 50)


def save_category_product_price(wd):
    price = aal(wd, '가격path').text
    if '%' in price:
        percent = price.find('%')
        start_index = percent + 2
        end_index = len(price)
        price = price[start_index:end_index].replace('원', '')
    else:
        price = price.replace('원', '')
    price = int(price.replace(',', ''))
    print(f'PLP 가격 : {price}')
    return price


def click_category_product(wd, text):
    aalc(wd, f'c_{text}')
    navigation_bar.close_bottom_sheet(wd)


def click_first_large_category(wd):
    category_layer = aal(wd, 'com.the29cm.app29cm:id/shopComposeView')
    # 첫번째 대메뉴 선택
    aalc(category_layer, 'category_first_title')


def check_unique_medium_category(self, wd):
    # 중 카테고리 리스트 중 상단 4개의 카테고리명을 리스트로 저장
    medium_category_list = []
    category_layer = aal(wd, 'com.the29cm.app29cm:id/shopComposeView')

    for i in range(3, 7):
        medium_category_list.append(aal(category_layer,
                                        f'//android.view.View/android.view.View[3]/android.view.View[@index={i}]/android.widget.TextView').text)

    category_list = self.pconf['compare_category_list']
    print(f"medium_category_list : {medium_category_list}, category_list : {category_list}")
    if category_list == medium_category_list:
        print('Unique 카테고리 확인')
    else:
        print(f'Unique 카테고리 확인 실패 : {medium_category_list}')
        raise Exception('Unique 카테고리 확인 실패')
