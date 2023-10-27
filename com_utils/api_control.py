import requests


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


def best_plp_women_clothes(rank):
    best_product = {}
    best_response = requests.get(
        'https://recommend-api.29cm.co.kr/api/v4/best/items?categoryList=268100100&periodSort=NOW&limit=100&offset=0')
    if best_response.status_code == 200:
        best_product_data = best_response.json()
        best_product_info = best_product_data['data']['content'][rank]
        best_product['item_no'] = best_product_info['itemNo']
        best_product['item_name'] = best_product_info['itemName']
        print(f'여성 의류 베스트 상품 : {best_product}')
        return best_product
    else:
        print('베스트 PLP API 불러오기 실패')
