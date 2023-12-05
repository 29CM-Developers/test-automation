from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc, element_scroll_control
from com_utils.api_control import my_heart_count


def close_brand_recommended_page(wd):
    try:
        # 관심 브랜드 선택 화면 발생
        brands_of_interest = aal(AppiumBy.ID, 'com.the29cm.app29cm:id/layoutMyLikeAndOrderBrand')
        print(brands_of_interest)
        if brands_of_interest == None:
            print('관심 브랜드 선택 팝업 미발생')
            pass
        else:
            print('관심 브랜드 선택 팝업 발생')
            wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/iconClose').click()
    except NoSuchElementException:
        pass


def close_noti_bottom_sheet(wd):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'liked_item_sale_notification_guide')
        aalc(wd, '닫기')
        print('알림 바텀시트 노출')
    except NoSuchElementException:
        pass


def set_like_zero(self, wd):
    # 좋아요 api 호출하여 각 탭의 좋아요 수 확인
    my_heart = my_heart_count(self.pconf['id_29cm'], self.pconf['password_29cm'])
    product_count = my_heart['product_count']
    brand_count = my_heart['brand_count']
    post_count = my_heart['post_count']

    if product_count != 0:
        print(f'좋아요 상품 수 : {product_count}')
        # product 탭 진입하여 모든 상품 좋아요 해제
        click_product_tab(wd)
        click_to_unlike_product(wd)
        # 좋아요 해제 후 새로고침
        refresh_product_like_tab(wd)

    if brand_count != 0:
        print(f'좋아요 브랜드 수 : {brand_count}')
        click_brand_tab(wd)
        click_to_unlike_brand(wd)
        # 좋아요 해제 후 새로고침
        refresh_brand_like_tab(wd)

    if post_count != 0:
        print(f'좋아요 포스트 수 : {post_count}')
        click_post_tab(wd)
        click_to_unlike_post(wd)
        # 좋아요 해제 후 새로고침
        refresh_post_like_tab(wd)


# 비교하는 like 수를 like_count에 작성
def check_like_total_count(wd, warning_texts, like_count):
    like_total_count = aal(wd, 'like_total_count')
    if like_total_count.text == like_count:
        test_result = 'PASS'
        print('총 LIKE 개수 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('총 LIKE 개수 확인 실패')
        print('총 LIKE 개수 확인 실패')
    return test_result


def click_product_tab(wd):
    aalc(wd, 'like_product_tab')


def click_brand_tab(wd):
    aalc(wd, 'like_brand_tab')


def click_post_tab(wd):
    aalc(wd, 'like_post_tab')


def check_no_product_like(wd, warning_texts):
    try:
        aal(wd, '좋아요한 상품이 없습니다. 마음에 드는 상품의 하트를 눌러보세요.')
        test_result = 'PASS'
        print('PRODUCT 좋아요 없음 문구 노출 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('PRODUCT 좋아요 없음 문구 노출 확인 실패')
        print('PRODUCT 좋아요 없음 문구 노출 확인 실패')
    return test_result


def check_no_brand_like(wd, warning_texts):
    try:
        aal(wd, '좋아요한 브랜드가 없어요.')
        test_result = 'PASS'
        print('BRAND 좋아요 없음 문구 노출 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('BRAND 좋아요 없음 문구 노출 확인 실패')
        print('BRAND 좋아요 없음 문구 노출 확인 실패')
    return test_result


def check_no_post_like(wd, warning_texts):
    try:
        aal(wd, '좋아요한 게시물이 없습니다. 다시 보고 싶은 게시물에 하트를 눌러보세요.')
        test_result = 'PASS'
        print('POST 좋아요 없음 문구 노출 확인')
    except NoSuchElementException:
        test_result = 'WARN'
        warning_texts.append('POST 좋아요 없음 문구 노출 확인')
        print('POST 좋아요 없음 문구 노출 확인')
    return test_result


def refresh_product_like_tab(wd):
    product_list = aal(wd, 'like_product_list')
    element_scroll_control(wd, product_list, 'U', 30)


def refresh_brand_like_tab(wd):
    product_list = aal(wd, 'like_brand_list')
    element_scroll_control(wd, product_list, 'U', 30)


def refresh_post_like_tab(wd):
    product_list = aal(wd, 'like_post_list')
    element_scroll_control(wd, product_list, 'U', 30)


def click_to_unlike_product(wd):
    product_like_layer = aal(wd, 'com.the29cm.app29cm:id/likeRecyclerView')
    aalc(product_like_layer, '//android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.ImageView[2]')
    txtProductCount = aal(wd, 'com.the29cm.app29cm:id/txtProductCount').text
    print(f'txtProductCount : {txtProductCount}')
    if txtProductCount == '(0)':
        print('Product Count 감소 확인')
    else:
        print('Product Count 감소 확인 실패')


def click_to_unlike_brand(wd):
    brand = wd.find_elements(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="ic heart line"]')
    for brand_like in brand:
        brand_like.click()


def click_to_unlike_post(wd):
    post = wd.find_elements(AppiumBy.XPATH,
                            '//XCUIElementTypeCell[@name="like_post_item"]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeButton')
    for post_like in post:
        post_like.click()


def save_like_product_name(wd):
    try:
        like_product_name = aal(wd, 'com.the29cm.app29cm:id/txtBody').text
        print(f'좋아요 상품명 : {like_product_name}')
    except NoSuchElementException:
        print('상품명 못찾음')
    return like_product_name


def click_product_like_btn(wd):
    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="like_btn"]').click()


# like_product_name = 좋아요 상품 목록의 상품명과 비교할 상품명
def check_product_like(wd, warning_texts, like_product_name):
    liked_product = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_product_item')
    liked_product_name = liked_product.find_element(AppiumBy.XPATH,
                                                    '//XCUIElementTypeStaticText[@index="1"]').text
    if like_product_name == liked_product_name:
        test_result = 'PASS'
        print('좋아요 상품 노출 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('좋아요 상품 노출 확인 실패')
        print(f'좋아요 상품 노출 확인 실패: 좋아요 전-{like_product_name} / 좋아요 후-{liked_product_name}')
    return test_result


def click_liked_product_cart_btn(wd):
    liked_product = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_product_item')
    liked_product.find_element(AppiumBy.IOS_CLASS_CHAIN,
                               '**/XCUIElementTypeButton[`label == "장바구니 담기"`]').click()


def save_like_brand_name(wd):
    recommended_brand = wd.find_element(AppiumBy.XPATH,
                                        '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="3"]')
    like_brand_name = recommended_brand.find_element(AppiumBy.XPATH,
                                                     '//XCUIElementTypeStaticText[@index="1"]').text
    print(f'좋아요 브랜드명 : {like_brand_name}')
    return like_brand_name


def click_brand_like_btn(wd):
    recommended_brand = wd.find_element(AppiumBy.XPATH,
                                        '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="3"]')
    recommended_brand.find_element(AppiumBy.IOS_CLASS_CHAIN,
                                   '**/XCUIElementTypeButton[`label == "ic heart line"`]').click()


# like_brand_name = 좋아요 상품 목록의 브랜드명과 비교할 브랜드명
def check_brand_like(wd, warning_texts, like_brand_name):
    liked_brand = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_brand_item')
    liked_brand_name = liked_brand.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@index="1"]').text
    if like_brand_name == liked_brand_name:
        test_result = 'PASS'
        print('좋아요 브랜드 노출 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('좋아요 브랜드 노출 확인 실패')
        print(f'좋아요 브랜드 노출 확인 실패: 좋아요 전-{like_brand_name} / 좋아요 후-{liked_brand_name}')
    return test_result


def click_liked_brand_name(wd):
    liked_brand = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_brand_item')
    liked_brand.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@index="1"]').click()


def click_brand_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')


def save_liked_brand_product_name(wd):
    brand_product_name = aal(wd,
                             '//XCUIElementTypeCell[@name="like_brand_item"]/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeStaticText').text
    print(f'좋아요 브랜드의 상품: {brand_product_name}')
    return brand_product_name


def click_liked_brand_porduct_name(wd):
    aalc(wd,
         '//XCUIElementTypeCell[@name="like_brand_item"]/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther')


def move_to_welove_page(wd):
    wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "인기 게시물 보기"`]').click()


# like_post_name = 좋아요 상품 목록의 포스트 제목과 비교할 포스트 제목
def check_post_like(wd, warning_texts, like_post_name):
    liked_post = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_post_item')
    liked_post_name = liked_post.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text
    if like_post_name == liked_post_name:
        test_result = 'PASS'
        print('좋아요 게시물 노출 확인')
    else:
        test_result = 'WARN'
        warning_texts.append('좋아요 게시물 노출 확인 실패')
        print(f'좋아요 게시물 노출 확인 실패 : 좋아요 전-{like_post_name} / 좋아요 후-{liked_post_name}')
    return test_result


def save_grid_image_size(wd):
    image_size = aal(wd,
                     '//XCUIElementTypeCell[@name="like_product_item"]/XCUIElementTypeOther/XCUIElementTypeImage').size
    return image_size


def save_list_image_size(wd):
    image_size = aal(wd,
                     '//XCUIElementTypeCollectionView[@name="like_product_list"]/XCUIElementTypeCell[2]/XCUIElementTypeOther/XCUIElementTypeImage').size
    return image_size


def click_change_view_type_to_list(wd):
    aalc(wd, 'ic like list')


def click_change_view_type_to_grid(wd):
    aalc(wd, 'ic like grid')


def check_veiw_image_size(warning_texts, grid_height, grid_width, list_height, list_width):
    if grid_height != list_height and grid_width != list_width:
        test_result = 'PASS'
        print("좋아요 상품 탭의 뷰 정렬 변경 확인")
    else:
        test_result = 'WARN'
        warning_texts.append('좋아요 상품 탭의 뷰 정렬 변경 확인 실패')
        print("좋아요 상품 탭의 뷰 정렬 변경 확인 실패")
    return test_result
