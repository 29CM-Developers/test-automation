from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, element_scroll_control
from com_utils.api_control import my_heart_count


def close_brand_recommended_page(wd):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'recommended_brand_page')
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'icNavigationbarBackBlack').click()
        print('브랜드 추천 페이지 노출 확인')
    except NoSuchElementException:
        pass


def close_noti_bottom_sheet(wd):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'liked_item_sale_notification_guide')
        ialc(wd, '닫기')
        print('알림 바텀시트 노출 확인')
    except NoSuchElementException:
        pass


def set_like_zero(self, wd):
    # 좋아요 api 호출하여 각 탭의 좋아요 수 확인
    my_heart = my_heart_count(self.pconf['id_29cm'], self.pconf['password_29cm'])
    product_count = my_heart['product_count']
    brand_count = my_heart['brand_count']
    post_count = my_heart['post_count']

    if product_count != 0:
        # product 탭 진입하여 모든 상품 좋아요 해제
        click_product_tab(wd)
        click_to_unlike_product(wd)
        # 좋아요 해제 후 새로고침
        refresh_product_like_tab(wd)

    if brand_count != 0:
        click_brand_tab(wd)
        click_to_unlike_brand(wd)
        # 좋아요 해제 후 새로고침
        refresh_brand_like_tab(wd)

    if post_count != 0:
        click_post_tab(wd)
        click_to_unlike_post(wd)
        # 좋아요 해제 후 새로고침
        refresh_post_like_tab(wd)


def check_like_phases(wd):
    try:
        ial(wd, 'like_total_count')
        print('LIKE 탭 진입 확인')
    except NoSuchElementException:
        print('LIKE 탭 진입 확인 실패')
        raise Exception('LIKE 탭 진입 확인 실패')


# 비교하는 like 수를 like_count에 작성
def check_like_total_count(wd, like_count):
    like_total_count = ial(wd, 'like_total_count')
    if like_total_count.text == like_count:
        print(f'총 LIKE 개수 {like_count} 확인')
    else:
        print(f'총 LIKE 개수 {like_count} 확인 실패')
        raise Exception(f'총 LIKE 개수 {like_count} 확인 실패')


def click_product_tab(wd):
    ialc(wd, 'like_product_tab')


def click_brand_tab(wd):
    ialc(wd, 'like_brand_tab')


def click_post_tab(wd):
    ialc(wd, 'like_post_tab')


def check_no_product_like(wd):
    try:
        ial(wd, '좋아요한 상품이 없습니다. 마음에 드는 상품의 하트를 눌러보세요.')
        print('PRODUCT 좋아요 없음 문구 노출 확인')
    except NoSuchElementException:
        print('PRODUCT 좋아요 없음 문구 노출 확인 실패')
        raise Exception('PRODUCT 좋아요 없음 문구 노출 확인 실패')


def check_no_brand_like(wd):
    try:
        ial(wd, '좋아요한 브랜드가 없어요.')
        print('BRAND 좋아요 없음 문구 노출 확인')
    except NoSuchElementException:
        print('BRAND 좋아요 없음 문구 노출 확인 실패')
        raise Exception('BRAND 좋아요 없음 문구 노출 확인 실패')


def check_no_post_like(wd):
    try:
        ial(wd, '좋아요한 게시물이 없습니다. 다시 보고 싶은 게시물에 하트를 눌러보세요.')
        print('POST 좋아요 없음 문구 노출 확인')
    except NoSuchElementException:
        print('POST 좋아요 없음 문구 노출 확인')
        raise Exception('POST 좋아요 없음 문구 노출 확인')


def refresh_product_like_tab(wd):
    product_list = ial(wd, 'like_product_list')
    element_scroll_control(wd, product_list, 'U', 30)


def refresh_brand_like_tab(wd):
    product_list = ial(wd, 'like_brand_list')
    element_scroll_control(wd, product_list, 'U', 30)


def refresh_post_like_tab(wd):
    product_list = ial(wd, 'like_post_list')
    element_scroll_control(wd, product_list, 'U', 30)


def click_to_unlike_product(wd):
    product = wd.find_elements(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="icHeartLine"]')
    for product_like in product:
        product_like.click()


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
    like_product_name = wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="product_name"]').text
    print(f'좋아요 상품명 : {like_product_name}')
    return like_product_name


def click_product_like_btn(wd):
    wd.find_element(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="like_btn"]').click()


# like_product_name = 좋아요 상품 목록의 상품명과 비교할 상품명
def check_product_like(wd, like_product_name):
    liked_product = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_product_item')
    liked_product_name = liked_product.find_element(AppiumBy.XPATH,
                                                    '//XCUIElementTypeStaticText[@index="1"]').text
    if like_product_name == liked_product_name:
        print('좋아요 상품 노출 확인')
    else:
        print(f'좋아요 상품 노출 확인 실패: 좋아요 전-{like_product_name} / 좋아요 후-{liked_product_name}')
        raise Exception('좋아요 상품 노출 확인 실패')


def click_product_name(wd):
    liked_product = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_product_item')
    liked_product.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@index="1"]').click()
    sleep(3)


def click_liked_product_cart_btn(wd):
    liked_product = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_product_item')
    liked_product.find_element(AppiumBy.IOS_CLASS_CHAIN,
                               '**/XCUIElementTypeButton[`label == "장바구니 담기"`]').click()


def save_like_brand_name(wd):
    recommended_brand = wd.find_element(AppiumBy.XPATH,
                                        '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="3"]')
    like_brand_name = recommended_brand.find_element(AppiumBy.XPATH,
                                                     '//XCUIElementTypeStaticText[@index="1"]').text
    return like_brand_name


def check_brand_page_name(wd, like_brand_name):
    brand_page_name = wd.find_element(AppiumBy.CSS_SELECTOR, '[class="css-1uqcj9j ezghadi1"]').text
    # 브랜드 PLP에서는 브랜드명이 대문자로 노출되어 변환
    if brand_page_name == like_brand_name.upper():
        print('브랜드 PLP 진입 확인')
    else:
        print(f'브랜드 PLP 진입 확인 실패 : plp-{brand_page_name} / like-{like_brand_name.upper()}')
        raise Exception('브랜드 PLP 진입 확인 실패')


def click_brand_like_btn(wd):
    recommended_brand = wd.find_element(AppiumBy.XPATH,
                                        '//XCUIElementTypeCollectionView/XCUIElementTypeCell[@index="3"]')
    recommended_brand.find_element(AppiumBy.IOS_CLASS_CHAIN,
                                   '**/XCUIElementTypeButton[`label == "ic heart line"`]').click()


# like_brand_name = 좋아요 상품 목록의 브랜드명과 비교할 브랜드명
def check_brand_like(wd, like_brand_name):
    liked_brand = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_brand_item')
    liked_brand_name = liked_brand.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@index="1"]').text
    if like_brand_name == liked_brand_name:
        print('좋아요 브랜드 노출 확인')
    else:
        print(f'좋아요 브랜드 노출 확인 실패: 좋아요 전-{like_brand_name} / 좋아요 후-{liked_brand_name}')
        raise Exception('좋아요 브랜드 노출 확인 실패')


def click_liked_brand_name(wd):
    liked_brand = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_brand_item')
    liked_brand.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@index="1"]').click()
    sleep(2)


def click_brand_back_btn(wd):
    ialc(wd, 'common back icon black')


def save_liked_brand_product_name(wd):
    brand_product_name = ial(wd,
                             '//XCUIElementTypeCell[@name="like_brand_item"]/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeStaticText').text
    return brand_product_name


def click_liked_brand_porduct_name(wd):
    ialc(wd,
         '//XCUIElementTypeCell[@name="like_brand_item"]/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther')


def move_to_welove_page(wd):
    wd.find_element(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "인기 게시물 보기"`]').click()


# like_post_name = 좋아요 상품 목록의 포스트 제목과 비교할 포스트 제목
def check_post_like(wd, like_post_name):
    liked_post = wd.find_element(AppiumBy.ACCESSIBILITY_ID, 'like_post_item')
    liked_post_name = liked_post.find_element(AppiumBy.XPATH, '//XCUIElementTypeStaticText').text
    if like_post_name == liked_post_name:
        print('좋아요 게시물 노출 확인')
    else:
        print(f'좋아요 게시물 노출 확인 실패 : 좋아요 전-{like_post_name} / 좋아요 후-{liked_post_name}')
        raise Exception('좋아요 게시물 노출 확인 실패')


def save_grid_image_size(wd):
    image_size = ial(wd,
                     '//XCUIElementTypeCell[@name="like_product_item"]/XCUIElementTypeOther/XCUIElementTypeImage').size
    return image_size


def save_list_image_size(wd):
    image_size = ial(wd,
                     '//XCUIElementTypeCollectionView[@name="like_product_list"]/XCUIElementTypeCell[2]/XCUIElementTypeOther/XCUIElementTypeImage').size
    return image_size


def click_change_view_type_to_list(wd):
    ialc(wd, 'ic like list')


def click_change_view_type_to_grid(wd):
    ialc(wd, 'ic like grid')


def check_veiw_image_size(grid_height, grid_width, list_height, list_width):
    if grid_height != list_height and grid_width != list_width:
        print("좋아요 상품 탭의 뷰 정렬 변경 확인")
    else:
        print("좋아요 상품 탭의 뷰 정렬 변경 확인 실패")
        raise Exception('좋아요 상품 탭의 뷰 정렬 변경 확인 실패')
