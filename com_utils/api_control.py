import json
import random
import requests
import com_utils.cookies_control


def home_banner_info(self):
    banner_data = {}
    response = requests.get(
        f'https://content-api.29cm.co.kr/api/v4/banners?bannerDivision=HOME_MOBILE&gender={self.pconf["gender"]}')
    if response.status_code == 200:
        banner_api_data = response.json()
        banner_count = int(banner_api_data['data']['count'])

        # 배너 ID, 컨텐츠, 타이틀 모두 저장
        banner_ids = []
        banner_contents = []
        banner_titles = []
        for i in range(0, banner_count):
            banner_id_api = banner_api_data['data']['bannerList'][i]['bannerId']
            banner_ids.append(banner_id_api)

            banner_contents_api = banner_api_data['data']['bannerList'][i]['bannerContents']
            banner_contents.append(banner_contents_api)

            banner_title_api = banner_api_data['data']['bannerList'][i]['bannerTitle']
            if banner_title_api == 'ㅤ':
                pass
            else:
                banner_title_api = banner_title_api.replace('\n', ' ')
                banner_titles.append(banner_title_api)

        banner_data['banner_ids'] = banner_ids
        banner_data['banner_contents'] = banner_contents
        banner_data['banner_titles'] = banner_titles
    else:
        print('홈 배너 API 불러오기 실패')
    return banner_data


def feed_contents_info(id, password):
    cookies = com_utils.cookies_control.cookie_29cm(id, password)
    feed_contents_titles = {}
    # 우먼 탭 컨텐츠 API 호출
    response = requests.get(
        'https://content-api.29cm.co.kr/api/v5/feeds?experiment=&feed_sort=WOMEN&home_type=APP_HOME&limit=20&offset=0',
        cookies=cookies)
    if response.status_code == 200:
        contents_api_data = response.json()
        feed_item_contents = contents_api_data['data']['results']

        first_feed_title = ''
        second_feed_title = ''
        first_title_with_item = ''

        for i in range(0, 10):
            feed_contents_type = feed_item_contents[i]['feedType']
            related_feed_item = feed_item_contents[i]['relatedFeedItemList']

            # feedType이 contents인 첫번째, 두번째 컨텐츠의 타이틀 저장
            if feed_contents_type == 'contents':
                if not first_feed_title:
                    first_feed_title = feed_item_contents[i]['feedTitle']
                    feed_contents_titles['first_feed_title'] = first_feed_title
                elif not second_feed_title and first_title_with_item:
                    second_feed_title = feed_item_contents[i]['feedTitle']
                    feed_contents_titles['second_feed_title'] = second_feed_title

            # 연결된 상품이 있는 첫번째 컨텐츠의 타이틀 저장
            if related_feed_item and not first_title_with_item:
                first_title_with_item = feed_item_contents[i]['feedTitle']
                feed_contents_titles['first_title_with_item'] = first_title_with_item

            # 모든 컨텐츠 타이틀명이 저장되었을 때, break
            if first_feed_title and first_title_with_item and second_feed_title:
                break
    else:
        print('피드 컨텐츠 API 불러오기 실패')

    return feed_contents_titles


'''
기존 배너, 피드 컨텐츠 정보 확장하도록 수정하여 아래 함수 권장
'''


def home_banners_info(self, type, tab_name):
    tab = self.conf['banner_data']
    if type == 'gender':
        response = requests.get(
            f'https://content-api.29cm.co.kr/api/v4/banners?bannerDivision=HOME_MOBILE&gender={tab[tab_name]}')
    elif type == 'life':
        response = requests.get(
            f'https://content-api.29cm.co.kr/api/v4/banners/home?bannerDivision=HOME_MOBILE&homeCategoryType={tab[tab_name]}')

    banner_data = {}
    if response.status_code == 200:
        banner_api_data = response.json()
        banner_count = int(banner_api_data['data']['count'])

        # 배너 ID, 컨텐츠, 타이틀 모두 저장
        banner_ids = []
        banner_contents = []
        banner_titles = []
        for i in range(0, banner_count):
            banner_id_api = banner_api_data['data']['bannerList'][i]['bannerId']
            banner_ids.append(banner_id_api)

            banner_contents_api = banner_api_data['data']['bannerList'][i]['bannerContents']
            banner_contents.append(banner_contents_api)

            banner_title_api = banner_api_data['data']['bannerList'][i]['bannerTitle']
            if banner_title_api == 'ㅤ':
                pass
            else:
                banner_title_api = banner_title_api.replace('\n', ' ')
                banner_titles.append(banner_title_api)

        banner_data['banner_ids'] = banner_ids
        banner_data['banner_contents'] = banner_contents
        banner_data['banner_titles'] = banner_titles
    else:
        print(f'{tab_name} 배너 API 불러오기 실패')
    return banner_data


def home_feed_contents_info(self, id, password, tab_name):
    cookies = com_utils.cookies_control.cookie_29cm(id, password)
    tab = self.conf['feed_data']
    feed_contents_titles = {}
    # 우먼 탭 컨텐츠 API 호출
    response = requests.get(
        f'https://content-api.29cm.co.kr/api/v5/feeds?experiment=&feed_sort={tab[tab_name]}&home_type=APP_HOME&limit=20&offset=0',
        cookies=cookies)
    if response.status_code == 200:
        contents_api_data = response.json()
        feed_item_contents = contents_api_data['data']['results']

        first_feed_title = ''
        second_feed_title = ''
        first_title_with_item = ''

        for i in range(0, 10):
            feed_contents_type = feed_item_contents[i]['feedType']
            related_feed_item = feed_item_contents[i]['relatedFeedItemList']

            # feedType이 contents인 첫번째, 두번째 컨텐츠의 타이틀 저장
            if feed_contents_type == 'contents':
                if not first_feed_title:
                    first_feed_title = feed_item_contents[i]['feedTitle']
                    feed_contents_titles['first_feed_title'] = first_feed_title
                elif not second_feed_title and first_title_with_item:
                    second_feed_title = feed_item_contents[i]['feedTitle']
                    feed_contents_titles['second_feed_title'] = second_feed_title

            # 연결된 상품이 있는 첫번째 컨텐츠의 타이틀 저장
            if related_feed_item and not first_title_with_item:
                first_title_with_item = feed_item_contents[i]['feedTitle']
                feed_contents_titles['first_title_with_item'] = first_title_with_item

            # 모든 컨텐츠 타이틀명이 저장되었을 때, break
            if first_feed_title and first_title_with_item and second_feed_title:
                break
    else:
        print('피드 컨텐츠 API 불러오기 실패')

    return feed_contents_titles


def large_categories_info(category, large_category_name):
    category_info = {}

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
                    if category_item_group_name == large_category_name:
                        category_info['large_category_code'] = category_group_item_list[v]['categoryCode']
                        category_info['large_category_name'] = category_group_item_list[v]['categoryName']
                        break
                    else:
                        pass
            else:
                pass
    else:
        print('카테고리 그룹 API 호출 실패')
    return category_info


def medium_categories_code(large_category_code, medium_category_name):
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


def large_category_list():
    api_large_list = []
    response = requests.get('https://recommend-api.29cm.co.kr/api/v5/best/categories/groups')
    if response.status_code == 200:
        large_category_data = response.json()
        # api에서 호출한 대 카테고리 리스트 저장
        for i in range(0, len(large_category_data['data'])):
            api_large_category = large_category_data['data'][i]['categoryName']
            api_large_list.append(api_large_category)
    else:
        print('대 카테고리 API 불러오기 실패')
    return api_large_list


# rank : 확인하고자하는 상품 순위 작성 (1위일 경우, 1로 작성)
# sort : 정렬 (new, popularity 등)
def category_plp_product(large_category_code, medium_category_code, rank, sort):
    response = requests.get(
        f'https://search-api.29cm.co.kr/api/v4/products/category?categoryLargeCode={large_category_code}&categoryMediumCode={medium_category_code}&count=50&sort={sort}')
    category_products = {}
    if response.status_code == 200:
        category_products_data = response.json()
        category_products['item_name'] = category_products_data['data']['products'][rank - 1]['itemName']
    else:
        print('피드 컨텐츠 API 불러오기 실패')
    return category_products


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


def my_heart_item(id, password):
    cookies = com_utils.cookies_control.cookie_29cm(id, password)

    like_response = requests.get('https://front-api.29cm.co.kr/api/v2/heart/my-heart/product', cookies=cookies)
    if like_response.status_code == 200:
        like = like_response.json()
        like_item = like['data']['content'][0]['item_name']
        return like_item
    else:
        print('좋아요 상품 불러오기 실패')


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
                coupons.append(coupon_name)
        return coupons

    else:
        print('보유 중인 쿠폰 목록 불러오기 실패')


# 전체 기준 인기 브랜드 순위
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

        brand_names = []
        for i in range(0, len(brands)):
            brand_name = brands[i]['keyword']
            brand_names.append(brand_name)
        search_popular_brand_name['brand_names'] = brand_names

        return search_popular_brand_name
    else:
        print('베스트 PLP API 불러오기 실패')

"""
common_search_results 메스드 파라미터 중 price,attribute,sort 항목은 메소드 호출하는 부분에서 사전에 세팅 후 파라미터로 넘겨줘야 함
price,attribute,sort = {} -> dict 타입으로 선언 후 
price["max"] ="value", price["min"]="value" -> key값에 value 선언
attribute["typeId"]="value",, attribute["valueId"]="value",-> key값에 value 선언
sort["type"]="value",, sort["order"]="value",-> key값에 value 선언
하여 price,attribute,sort 를 파라미터로 넘겨줌
"""
# 검색 공용 api 조회
def common_search_results( id=None, password=None, keyword=None, largeId=None, middleId=None, smallId=None, brand=None, color=None, attribute=None, price=None, delivery=None, stock=None, discount=None, concierge=None,event=None, styleTag=None, sort=None):
    headers = {'Content-Type': 'application/json'}
    request_body = {}
    request_body["keyword"]=keyword
    request_body["pagination"] = {"page": 0,"size": 30}
    facetGroupInput = {}

    if id != None and password != None:
        cookies = com_utils.cookies_control.cookie_29cm(id, password)
    if largeId != None:
        facetGroupInput['categoryFacetInputs'] = [{"largeId": largeId, "middleId": middleId, "smallId": smallId}]
    if brand != None:
        facetGroupInput['brandFacetInputs'] = [{"frontBrandNo": brand}]
    if color != None:
        facetGroupInput['colorFacetInputs'] = [{"hex": color}]
    if attribute != None:
        facetGroupInput['attributeInputs'] = [{"typeId": attribute["typeId"], "valueId": attribute["valueId"]}]
    if price != None:
        facetGroupInput['priceFacetInput'] = {"max": price["max"], "min": price["min"]}
    if delivery != None:
        facetGroupInput['deliveryFacetInputs'] = [{"type": "FREE_SHIPPING"}]
    if stock != None:
        facetGroupInput['stockFacetInputs'] = [{"type": "IN_STOCK"}]
    if discount != None:
        facetGroupInput['discountFacetInputs'] = [{"type": "ONLY_DISCOUNT"}]
    if concierge != None:
        facetGroupInput['conciergeFacetInputs'] = [{"type": "ONLY_CONCIERGE"}]
    if event != None:
        facetGroupInput['eventFacetInputs'] = [{"tag": event}]
    if styleTag != None:
        facetGroupInput['styleTagFacetInputs'] = [{"tagId": styleTag}]
    if sort != None:
        facetGroupInput['sortFacetInput'] = {"type": sort["type"], "order": sort["order"]}
    else:
        facetGroupInput['sortFacetInput'] = {"type": "RECOMMEND", "order": "DESC"}

    request_body['facetGroupInput'] = facetGroupInput
    data = json.dumps(request_body)

    if id != None and password != None:
        search_response = requests.post('https://search-api.29cm.co.kr/api/v4/srp/:search',
                                        data=data,headers=headers,cookies=cookies)
    else:
        search_response = requests.post('https://search-api.29cm.co.kr/api/v4/srp/:search',
                                    headers=headers, data=data)
    if search_response.status_code == 200:
        search_result_data = search_response.json()
        return search_result_data
    else:
        print(f'검색 결과 API 불러오기 실패 : {search_response.status_code} 에러)')

# 연관 브랜드가 1개인 브랜드명
def search_brand_by_related_brand():
    brand_list = search_total_popular_brand_name()['brand_names']
    brand_name = ''
    for brand_name in brand_list:

        brand_response = requests.get(
            f'https://search-api.29cm.co.kr/api/v4/products/brand/keyword/?keyword={brand_name}')

        if brand_response.status_code == 200:
            brand_data = brand_response.json()
            search_data = common_search_results(keyword=brand_name)
            keyword_type = search_data['data']['keywordTypes']
            if len(brand_data['data']) == 1 and keyword_type == ['brand']:
                break
        else:
            print(f'검색 브랜드 정보 API 불러오기 실패 : {brand_response.status_code} 에러)')
    return brand_name


# 여성 기준 인기 브랜드 순위
def search_woman_popular_brand_name():
    response = requests.get(
        'https://search-api.29cm.co.kr/api/v4/popular?gender=female&keywordLimit=100&brandLimit=30')
    if response.status_code == 200:
        api_data = response.json()
        brands = api_data['data']['brand']['results'][0]['keywords']
        api_1st_brand_name = brands[0]['keyword']
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


# 검색 결과 페이지의 연관 검색어 호출
def search_relate_keyword(api_keyword_1st):
    response = requests.get(
        f'https://search-api.29cm.co.kr/api/v4/keyword/related?keyword={api_keyword_1st}')
    if response.status_code == 200:
        relate_keyword_data = response.json()
        relate_keyword_list = relate_keyword_data['data']['relatedKeywords']
        return relate_keyword_list
    else:
        print('연관 검색어 API 호출 실패')


# keyword : 검색어 / order : 노출 순서
def search_result(keyword, order):
    result = {}
    search_result_data = common_search_results(keyword=keyword)
    result['product_item_no'] = search_result_data['data']['products'][order - 1]['itemNo']
    return result


def search_brand_category_info(keyword):
    category_no = {}
    category_response = requests.get(f'https://search-api.29cm.co.kr/api/v4/filters/product?keyword={keyword}')
    if category_response.status_code == 200:
        category_data = category_response.json()
        categories = category_data['data']['categories']
        category_no['large_code'] = categories[0]['categoryCode']
        category_no['large_name'] = categories[0]['categoryName']
        category_no['medium_code'] = categories[0]['categories'][0]['categoryCode']
        category_no['medium_name'] = categories[0]['categories'][0]['categoryName']
        category_no['small_code'] = categories[0]['categories'][0]['categories'][0]['categoryCode']
        category_no['small_name'] = categories[0]['categories'][0]['categories'][0]['categoryName']
        return category_no
    else:
        print('검색 결과 브랜드 정보 API 불러오기 실패')


def filter_brand_search_results_by_category(id, password, keyword):
    categories = com_utils.api_control.search_brand_category_info(keyword)
    filter_result = {}
    search_result_data = common_search_results(id, password, keyword, categories["large_code"], categories["medium_code"], categories["small_code"] )
    filter_brand = search_result_data['data']['products']
    filter_result['item_name'] = filter_brand[0]['itemName']
    return filter_result


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


def product_item_option_no(product_item_no):
    option_id = ''
    option = product_detail(product_item_no)['option_items_list']
    if not option:
        option_id = None
    else:
        option_list = product_no_soldout_option(product_item_no)
        for list, value in option_list.items():
            if list.startswith('id'):
                option_id = value
    return option_id


def product_no_soldout_option(product_item_no):
    option_layout = product_detail(product_item_no)['option_items_layout']
    option_item_list = product_detail(product_item_no)['option_items_list']
    option_list = {}

    option_break = False
    for j in range(len(option_item_list)):
        option_item_list = product_detail(product_item_no)['option_items_list']
        for i, layout in enumerate(option_layout):
            option_list[f'layout{i}'] = layout
            if i < len(option_layout) - 1:
                option_list[f'option{i}'] = option_item_list[j]["title"]
                option_item_list = option_item_list[j].get('list', [])
            else:
                for option in option_item_list:
                    option_name = option["title"].strip()
                    if option['limited_qty'] > 3:
                        option_break = True
                        option_list[f'option{i}'] = option_name
                        option_list['id'] = option["option_no"]
                        break
        if option_break:
            break
    return option_list


def order_product_random_no():
    price={}
    price["max"] = 1500
    price["min"] = 0
    product_data = common_search_results(keyword="양말", stock=True, price=price)
    item_count = product_data['data']['products']
    random_no = random.randint(0, len(item_count) - 1)
    item_no = None
    for _ in range(len(item_count)):
        if not product_data['data']['products'][random_no]['isSoldOut']:
            item_no = product_data['data']['products'][random_no]['itemNo']
            break
        random_no = (random_no + 1) % len(item_count)
    return item_no


def my_order_status(id, password, order_serial_no):
    order_status = ''
    # response = requests.post('https://apihub.29cm.co.kr/qa/user/login/', data={"user_id":id, "user_password":password})
    # cookies = response.cookies
    # response = requests.get('https://apihub.29cm.co.kr/qa/order/orders/my-order/?limit=20&offset=0', cookies=cookies)
    cookies = com_utils.cookies_control.cookie_29cm(id, password)
    response = requests.get('https://apihub.29cm.co.kr/order/orders/my-order/?limit=20&offset=0', cookies=cookies)
    if response.status_code == 200:
        order_data = response.json()
        for i in range(0, order_data['count']):
            order = order_data['results'][i]
            order_serial = order['order_serial']
            if order_serial == order_serial_no:
                order_status = order['order_status_description']
                break
    else:
        print('주문배송조회 API 불러오기 실패')
    return order_status


def my_order_info(id, password, order_serial_no):
    my_order_data = {}
    # response = requests.post('https://apihub.29cm.co.kr/qa/user/login/', data={"user_id":id, "user_password":password})
    # cookies = response.cookies
    # response = requests.get('https://apihub.29cm.co.kr/qa/order/orders/my-order/?limit=20&offset=0', cookies=cookies)
    cookies = com_utils.cookies_control.cookie_29cm(id, password)
    response = requests.get('https://apihub.29cm.co.kr/order/orders/my-order/?limit=20&offset=0', cookies=cookies)
    if response.status_code == 200:
        order_data = response.json()
        for i in range(0, order_data['count']):
            order = order_data['results'][i]
            order_serial = order['order_serial']
            if order_serial == order_serial_no and order['manages'] != []:
                my_order_data['order_no'] = order['order_no']
                my_order_data['order_manage_no'] = order['manages'][0]['order_item_manage_no']
                my_order_data['order_count'] = order['manages'][0]['order_count']
                break
    else:
        print('주문배송조회 API 불러오기 실패')
    return my_order_data


def my_order_cancel(id, password, order_serial_no):
    my_order_data = my_order_info(id, password, order_serial_no)
    order_no = my_order_data['order_no']
    order_manage_no = my_order_data['order_manage_no']
    order_count = my_order_data['order_count']

    headers = {'Content-Type': 'application/json'}
    # response = requests.post('https://apihub.29cm.co.kr/qa/user/login/', data={"user_id": id,"user_password": password})
    # cookies = response.cookies
    cookies = com_utils.cookies_control.cookie_29cm(id, password)
    data = json.dumps({
        "cancelItemList": [
            {
                "orderItemManageId": order_manage_no,
                "cancelCount": order_count
            }
        ],
        "cancelReasonCode": "SIMPLE_REMORSE",
        "cancelReasonMessage": None,
        "orderNo": order_no,
        "refundBankAccount": None
    })
    # response = requests.post('https://apihub.29cm.co.kr/qa/api/v1/order-cancel/user-cancel/', headers=headers,
    #                          cookies=cookies, data=data)
    response = requests.post('https://apihub.29cm.co.kr/api/v1/order-cancel/user-cancel/',
                             headers=headers, cookies=cookies, data=data)
    if response.status_code == 200:
        cancel_data = response.json()
        if cancel_data['result'] == 'SUCCESS':
            print(f'{order_serial_no} API로 주문취소 완료')
        else:
            print(f'{order_serial_no} API로 주문취소 실패!!')
    else:
        print(response.status_code)
        print('주문 취소 API 불러오기 실패')


def cart_product_count(id, password):
    cookies = com_utils.cookies_control.cookie_29cm(id, password)
    response = requests.get('https://commerce-api.29cm.co.kr/api/v4/cart-item/item-count', cookies=cookies)
    if response.status_code == 200:
        cart_data = response.json()
        cart_count = cart_data['data']['count']
        return cart_count
    else:
        print('장바구니 상품 개수 조회 API 불러오기 실패')


def add_product_to_cart(id, password):
    item_id = order_product_random_no()
    option_id = product_item_option_no(item_id)

    headers = {'Content-Type': 'application/json'}
    cookies = com_utils.cookies_control.cookie_29cm(id, password)
    data = json.dumps({
        "cartItemList": [
            {
                "itemId": item_id,
                "optionId": option_id,
                "orderCount": 1,
                "requestComment": None,
                "isOrderCheck": False,
                "isNaverAccess": False
            }
        ]
    })

    response = requests.post('https://commerce-api.29cm.co.kr/api/v4/cart-item/',
                             headers=headers, cookies=cookies, data=data)
    if response.status_code == 200:
        cart_data = response.json()
        if cart_data['result'] == 'SUCCESS':
            print('장바구니에 상품 담기 성공 확인')
        else:
            print('장바구니에 상품 담기 실패 확인')
    else:
        print('장바구니 상품 담기 API 불러오기 실패')
