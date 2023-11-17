import requests
import com_utils.cookies_control


def large_category_info(category, large_category_text):
    large_category_code = ''
    large_category_name = ''

    # 카테고리 그룹 API 호출
    response = requests.get('https://recommend-api.29cm.co.kr/api/v4/best/category-groups')
    if response.status_code == 200:
        category_group_data = response.json()
        category_group = category_group_data['data']

        # 찾고자 하는 카테고리 그룹의 아이템 리스트 확인
        for i in range(0, 2):
            category_group_name = category_group[i]['categoryGroupName']
            if category_group_name == category:
                category_group_item_list = category_group[i]['categoryGroupItemList']
                # 찾고자 하는 이름의 대 카테고리 코드 번호 저장
                for v in range(0, 10):
                    category_item_group_name = category_group_item_list[v]['categoryGroupItemName']
                    if category_item_group_name == large_category_text:
                        large_category_code = category_group_item_list[v]['categoryCode']
                        large_category_name = category_group_item_list[v]['categoryName']
                        break
                    else:
                        pass
            else:
                pass
    else:
        print('카테고리 그룹 API 호출 실패')

    return large_category_code, large_category_name


def medium_category_code(large_category_code, medium_category_name):
    medium_category_code = ''

    # 대 카테고리의 하위 카테고리 API 호출
    response = requests.get(
        f'https://recommend-api.29cm.co.kr/api/v4/best/categories?categoryList={large_category_code}')
    if response.status_code == 200:
        medium_category_data = response.json()

        # 찾고자 하는 이름의 중 카테고리 코드 번호 저장
        for i in range(0, 10):
            category_name = medium_category_data['data'][i]['categoryName']
            if category_name == medium_category_name:
                medium_category_code = medium_category_data['data'][i]['categoryCode']
                break
            else:
                pass
    else:
        print('중 카테고리 리스트 API 호출 실패')

    return medium_category_code


# rank : 확인하고자하는 여성의류 순위 작성 (1위일 경우, 1로 작성)
# period : NOW, ONE_DAY, ONE_WEEK, ONE_MONTH
def best_plp_women_clothes(rank, period):
    best_product = {}
    best_response = requests.get(
        f'https://recommend-api.29cm.co.kr/api/v4/best/items?categoryList=268100100&periodSort={period}&limit=100&offset=0')
    if best_response.status_code == 200:
        best_product_data = best_response.json()
        best_product_info = best_product_data['data']['content'][rank - 1]
        best_product['item_no'] = best_product_info['itemNo']
        best_product['item_name'] = best_product_info['itemName']
        best_product['item_prefix'] = best_product_info['subjectDescriptions']
        best_product['item_soldout'] = best_product_info['isSoldOut']
        print(f'여성 의류 베스트 상품 : {best_product}')
        return best_product
    else:
        print('베스트 PLP API 불러오기 실패')


# 테스트 하는 id, password 입력
def my_heart_count(id, password):
    cookies = com_utils.cookies_control.cookie_29cm(id, password)

    like_count = {}
    like_response = requests.get('https://front-api.29cm.co.kr/api/v4/heart/my-heart/count/', cookies=cookies)
    if like_response.status_code == 200:
        like = like_response.json()
        like_count['product_count'] = int(like['data']['product_count'])
        like_count['brand_count'] = int(like['data']['brand_count'])
        like_count['post_count'] = int(like['data']['post_count'])
        return like_count
    else:
        print('좋아요 수 불러오기 실패')


# 테스트 하는 id, password 입력
def my_coupon_list(id, password, coupon_type):
    cookies = com_utils.cookies_control.cookie_29cm(id, password)

    coupon_response = requests.get(
        f'https://promotion-api.29cm.co.kr/api/v5/coupons/issued/my-coupon?page=1&size=100&couponType={coupon_type}',
        cookies=cookies)
    if coupon_response.status_code == 200:
        coupon = coupon_response.json()

        if coupon_type == 'CART':
            coupon_count = int(coupon['data']['cartCouponCount'])
        else:
            coupon_count = int(coupon['data']['itemCouponCount'])

        coupons = []
        if coupon_count == 0:
            pass
        else:
            for i in range(0, coupon_count):
                coupon_name = coupon['data']['resultList'][i]['couponName']
                print(f'coupon_name : {coupon_name}')
                coupons.append(coupon_name)
            print(f'coupons : {coupons}')
        return coupons

    else:
        print('보유 중인 쿠폰 목록 불러오기 실패')


def search_total_popular_brand_name():
    search_popular_brand_name = {}
    response = requests.get(
        'https://search-api.29cm.co.kr/api/v4/popular?gender=all&keywordLimit=100&brandLimit=30')
    if response.status_code == 200:
        api_data = response.json()
        brands = api_data['data']['brand']['results'][0]['keywords']
        search_popular_brand_name['category_name'] = api_data['data']['brand']['results'][0]['categoryName']
        search_popular_brand_name['api_1st_brand_name'] = brands[0]['keyword']
        search_popular_brand_name['api_30th_brand_name'] = brands[29]['keyword']
        print(
            f"api_1st_brand_name : {search_popular_brand_name['api_1st_brand_name']}, api 30th_brand_name : {search_popular_brand_name['api_30th_brand_name']}, category_name : {search_popular_brand_name['category_name']}")
        return search_popular_brand_name
    else:
        print('베스트 PLP API 불러오기 실패')


def search_woman_popular_brand_name():
    response = requests.get(
        'https://search-api.29cm.co.kr/api/v4/popular?gender=female&keywordLimit=100&brandLimit=30')
    if response.status_code == 200:
        api_data = response.json()
        brands = api_data['data']['brand']['results'][0]['keywords']
        api_1st_brand_name = brands[0]['keyword']
        print(f"api 1st_brand_name : {api_1st_brand_name}")
        return api_1st_brand_name
    else:
        print('여성 인기 브랜드 API 불러오기 실패')


def search_popular_keyword():
    search_popular_keyword = {}
    response = requests.get('https://search-api.29cm.co.kr/api/v4/keyword/popular?limit=100&brandLimit=30')
    if response.status_code == 200:
        api_data = response.json()
        keywords = api_data['data']['popularKeyword']
        search_popular_keyword['api_1st_keyword_name'] = keywords[0]
        search_popular_keyword['api_25th_keyword_name'] = keywords[24]
        return search_popular_keyword
    else:
        print('인기 검색어 API 불러오기 실패')


# keyword : 검색어 / order : 노출 순서
def search_result(keyword, order):
    result = {}
    search_response = requests.get(
        f'https://search-api.29cm.co.kr/api/v4/products/search?keyword={keyword}&excludeSoldOut=false')
    if search_response.status_code == 200:
        search_result_data = search_response.json()
        result['product_item_no'] = search_result_data['data']['products'][order - 1]['itemNo']
        return result
    else:
        print('검색 결과 API 불러오기 실패')


# product_item_no : 상품의 item_no
def product_detail(product_item_no):
    product_detail = {}
    response = requests.get(f'https://cache.29cm.co.kr/item/detail/{product_item_no}/')
    if response.status_code == 200:
        product_data = response.json()
        product_detail['item_name'] = product_data['item_name']
        product_detail['option_items_list'] = product_data['option_items']['list']
        if product_data['option_items']['list']:
            product_detail['option_items_layout'] = product_data['option_items']['layout']
        return product_detail
    else:
        print('PDP 상세 정보 API 불러오기 실패')
