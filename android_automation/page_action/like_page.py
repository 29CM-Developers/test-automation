from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from android_automation.page_action.bottom_sheet import close_bottom_sheet, close_pdp_bottom_sheet
from com_utils.element_control import aal, aalc, element_scroll_control
from com_utils.api_control import my_heart_count


def close_brand_recommended_page(wd):
    try:
        # 관심 브랜드 선택 화면 발생
        brands_of_interest = aal(wd, 'com.the29cm.app29cm:id/recommendBrandRecyclerView')
        if brands_of_interest == None:
            print('관심 브랜드 선택 팝업 미발생')
            pass
        else:
            print('관심 브랜드 선택 팝업 발생')
            aalc(wd, 'com.the29cm.app29cm:id/iconClose')
    except NoSuchElementException:
        pass


def set_like_zero(self, wd):
    # 좋아요 api 호출하여 각 탭의 좋아요 수 확인
    my_heart = my_heart_count(self.pconf['LOGIN_SUCCESS_ID_1'], self.pconf['LOGIN_SUCCESS_PW'])
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

    # if post_count != 0:
    #     print(f'좋아요 포스트 수 : {post_count}')
    #     click_post_tab(wd)
    #     click_to_unlike_post(wd)
    #     # 좋아요 해제 후 새로고침
    #     refresh_post_like_tab(wd)


# 비교하는 like 수를 like_count에 작성
def check_like_total_count(wd, like_count):
    txtHeartCount = aal(wd, 'com.the29cm.app29cm:id/txtHeartCount').text
    if txtHeartCount == like_count:
        print(f'총 LIKE 개수 {like_count} 확인')
    else:
        print(f'총 LIKE 개수 {like_count} 확인 실패')
        raise Exception(f'총 LIKE 개수 {like_count} 확인 실패')


def click_product_tab(wd):
    aalc(wd, 'com.the29cm.app29cm:id/layoutProduct')


def click_brand_tab(wd):
    aalc(wd, 'com.the29cm.app29cm:id/layoutBrand')


def click_post_tab(wd):
    aalc(wd, 'like_post_tab')


def check_no_product_like(wd):
    txtInfo = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtInfo').text
    if txtInfo in '좋아요한 상품이 없습니다.\n마음에 드는 상품에 하트를 눌러보세요.':
        print('PRODUCT 좋아요 없음 문구 노출 확인')
    else:
        print('PRODUCT 좋아요 없음 문구 노출 확인 실패')
        raise Exception('PRODUCT 좋아요 없음 문구 노출 확인 실패')


def check_no_brand_like(wd):
    txtInfo = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtInfo').text
    if txtInfo in '좋아요한 브랜드가 없습니다.\n마음에 드는 브랜드에 하트를 눌러보세요.':
        print('BRAND 좋아요 없음 문구 노출 확인')
    else:
        print('BRAND 좋아요 없음 문구 노출 확인 실패')
        raise Exception('BRAND 좋아요 없음 문구 노출 확인 실패')


def check_no_post_like(wd):
    try:
        aal(wd, '좋아요한 게시물이 없습니다. 다시 보고 싶은 게시물에 하트를 눌러보세요.')
        print('POST 좋아요 없음 문구 노출 확인')
    except NoSuchElementException:
        print('POST 좋아요 없음 문구 노출 확인')
        raise Exception('POST 좋아요 없음 문구 노출 확인')

def refresh_product_like_tab(wd):
    product_list = aal(wd, 'com.the29cm.app29cm:id/layoutInfo')
    element_scroll_control(wd, product_list, 'U', 30)


def refresh_brand_like_tab(wd):
    aalc(wd, 'com.the29cm.app29cm:id/layoutShowBrand')


def refresh_post_like_tab(wd):
    product_list = aal(wd, 'com.the29cm.app29cm:id/layoutInfo')
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
    aalc(wd, 'com.the29cm.app29cm:id/layoutHeart')
    txtBrandCount = wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/txtBrandCount').text
    if txtBrandCount == '(0)':
        print('Brand Count 감소 확인')
    else:
        print('Brand Count 감소 확인 실패')


def save_like_product_name(wd):
    # like_layer = aal(wd, 'com.the29cm.app29cm:id/likeRecyclerView')
    # productItem = aal(like_layer,
    #                   '//android.view.ViewGroup[2]/android.widget.TextView[@resource-id="com.the29cm.app29cm:id/contentsDescription"]').text
    productItem = aal(wd, 'com.the29cm.app29cm:id/txtBody').text
    print(f"productItem : {productItem}")
    # like_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[2]/android.widget.ImageView[@resource-id="com.the29cm.app29cm:id/contentsHeart"]').click()
    return productItem


def save_like_product_name_in_like(wd):
    like_layer = aal(wd, 'com.the29cm.app29cm:id/likeRecyclerView')
    productItem = aal(like_layer,
                      '//android.view.ViewGroup[2]/android.widget.TextView[@resource-id="com.the29cm.app29cm:id/contentsDescription"]').text

    print(f"productItem : {productItem}")
    # like_layer.find_element(AppiumBy.XPATH,'//android.view.ViewGroup[2]/android.widget.ImageView[@resource-id="com.the29cm.app29cm:id/contentsHeart"]').click()
    return productItem

    # try:
    #     like_product_name = aal(wd, 'com.the29cm.app29cm:id/txtBody').text
    #     print(f'좋아요 상품명 : {like_product_name}')
    # except NoSuchElementException:
    #     print('상품명 못찾음')
    # return like_product_name


def click_product_like_btn(wd):
    like_layer = aal(wd, 'com.the29cm.app29cm:id/likeRecyclerView')
    aalc(like_layer,
         '//android.view.ViewGroup[2]/android.widget.ImageView[@resource-id="com.the29cm.app29cm:id/contentsHeart"]')



# like_product_name = 좋아요 상품 목록의 상품명과 비교할 상품명
def check_product_like(wd, like_product_name):
    like_layer = aal(wd, 'com.the29cm.app29cm:id/likeRecyclerView')
    aalc(wd, 'com.the29cm.app29cm:id/layoutShowProduct')
    like_productItem = aal(like_layer, 'com.the29cm.app29cm:id/txtBody').text
    print(f"like_productItem : {like_productItem}")
    if like_productItem in like_product_name:
        print('좋아요 상품 노출 확인')
    else:
        print(f'좋아요 상품 노출 확인 실패: 좋아요 전-{like_product_name} / 좋아요 후-{like_productItem}')
        raise Exception('좋아요 상품 노출 확인 실패')


def click_product_name(wd):
    like_layer = aal(wd, 'com.the29cm.app29cm:id/likeRecyclerView')
    aalc(like_layer, 'com.the29cm.app29cm:id/txtBody')
    close_bottom_sheet(wd)


def click_liked_product_cart_btn(wd):
    # 장바구니 버튼 선택하여 PDP 진입 확인 (바텀시트 확인, 상품명 확인)
    aalc(wd, 'com.the29cm.app29cm:id/txtCart')


def check_open_to_purchase_modal(wd, like_productItem):
    # like_layer = aal(wd, 'com.the29cm.app29cm:id/likeRecyclerView')
    # like_productItem = aal(like_layer, 'com.the29cm.app29cm:id/txtBody').text
    item_name = aal(wd, 'com.the29cm.app29cm:id/txtItemName').text
    if item_name in like_productItem:
        print('좋아요 상품명 장바구니 모달 확인')
    else:
        print('좋아요 상품명 장바구니 모달 확인 실패')
        raise Exception('좋아요 상품명 장바구니 모달 확인 실패')


def close_purchase_modal(wd):
    # sleep(1)
    # aalc(wd, 'android:id/content')
    wd.find_element(AppiumBy.ID, 'android:id/content').click()
    print('모달 닫기 선택')


def save_like_brand_name(wd):
    like_layer = aal(wd, 'com.the29cm.app29cm:id/likeRecyclerView')
    BrandName = aal(like_layer, 'com.the29cm.app29cm:id/txtBrandName').text
    print(f"브랜드 이름 : {BrandName} 확인")

    return BrandName


def click_brand_like_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/layoutHeart')


# like_brand_name = 좋아요 상품 목록의 브랜드명과 비교할 브랜드명
def check_brand_like(wd, like_brand_name):
    like_BrandName = aal(wd, 'com.the29cm.app29cm:id/txtBrandName')
    print(f"좋아요한 브랜드 이름 : {like_BrandName.text} 확인")
    if like_brand_name in like_BrandName.text:
        print('좋아요 브랜드 노출 확인')
    else:
        print('좋아요 브랜드 노출 확인 실패')
        raise Exception('좋아요 브랜드 노출 확인 실패')


def check_brand_page_name(wd, like_brand_name):
    original_string = like_brand_name
    uppercase_string = original_string.upper()
    brand_name = aal(wd, '//*[@id="__next"]/section[1]/div[1]/div[1]/h3')
    print(f'브랜드 이름 : {brand_name.text} 확인')
    if uppercase_string in brand_name.text:
        print('좋아요 브랜드 노출 확인')
    else:
        print('좋아요 브랜드 노출 확인 실패')
        raise Exception('좋아요 브랜드 노출 확인 실패')
    sleep(1)


def click_liked_brand_name(wd):
    aalc(wd, 'com.the29cm.app29cm:id/txtBrandName')


def click_brand_back_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgBack')
    print("뒤로가기 선택")


def save_liked_brand_product_name(wd):
    like_BrandName = aal(wd, 'com.the29cm.app29cm:id/txtBrandName')
    print(f"좋아요한 브랜드 이름 : {like_BrandName.text} 확인")
    return like_BrandName


def save_liked_brand_product_name(wd):
    item_layer = aal(wd, 'com.the29cm.app29cm:id/recyclerView')
    item_name = aal(item_layer, '//android.widget.TextView[@resource-id="com.the29cm.app29cm:id/itemName"]').text
    print(f'좋아요한 브랜드 상품명 : {item_name} 확인')
    return item_name


def click_liked_brand_product_name(wd):
    item_layer = aal(wd, 'com.the29cm.app29cm:id/recyclerView')
    aalc(item_layer, '//android.widget.TextView[@resource-id="com.the29cm.app29cm:id/itemName"]')
    close_bottom_sheet(wd)
    close_pdp_bottom_sheet(wd)


def save_grid_image_size(wd):
    # 그리드 뷰 상태에서 이미지 사이즈 저장
    grid_size = aal(wd, '//android.widget.ImageView[@resource-id="com.the29cm.app29cm:id/imageThumbnail"]').size
    print(f'grid_size : {grid_size["height"]} / {grid_size["width"]}')

    return grid_size


def save_list_image_size(wd):
    list_size = aal(wd, '//android.widget.ImageView[@resource-id="com.the29cm.app29cm:id/imageThumbnail"]').size
    print(f'grid_size : {list_size["height"]} / {list_size["width"]}')
    return list_size


def click_change_view_type_to_list(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imageGrid')


def click_change_view_type_to_grid(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imageGrid')


def check_veiw_image_size(grid_height, grid_width, list_height, list_width):
    if grid_height != list_height and grid_width != list_width:
        print("좋아요 상품 탭의 뷰 정렬 변경 확인")
    else:
        print("좋아요 상품 탭의 뷰 정렬 변경 확인 실패")
        raise Exception('좋아요 상품 탭의 뷰 정렬 변경 확인 실패')


def check_like_phases(wd):
    like_title = aal(wd, 'com.the29cm.app29cm:id/txtTitle')
    if like_title == None:
        print('LIKE 탭 진입 확인 실패')
        raise Exception('LIKE 탭 진입 확인 실패')
    elif like_title.text == 'LIKE':
        print('HOME 탭에서 LIKE 탭 이동 확인')
    else:
        print(f'LIKE 탭 진입 확인 실패 : {like_title.text}')
        raise Exception('LIKE 탭 진입 확인 실패')
