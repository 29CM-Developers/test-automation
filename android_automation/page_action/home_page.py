from time import sleep
from selenium.common import NoSuchElementException
import com_utils.element_control
from android_automation.page_action.bottom_sheet import close_bottom_sheet
from com_utils.api_control import home_banner_info
from com_utils.element_control import aal, aalc, aals, scroll_control, swipe_control


def check_home_logo(wd):
    logo = aal(wd, 'com.the29cm.app29cm:id/imgLogo')
    if logo == None:
        print('HOME 탭으로 이동 확인 실패')
    else:
        print('HOME 탭으로 이동 확인')


def click_search_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/imgSearch')
    print("상단 검색 아이콘 선택")


def click_close_life_tab(wd):
    # 디폴트 선택 화면 확인
    top_tabs = aal(wd, 'com.the29cm.app29cm:id/tabs')
    culture_tab = aal(top_tabs, '//android.view.View[@index=4]/android.widget.TextView')
    if culture_tab.text == '푸드':
        print("푸드 탭 존재")
        aalc(wd, 'life_tab')
        print("라이프 탭 해제")
    else:
        print('라이프 탭 디폴트 아님')


# click_tab_name : 선택하려는 상단 탭 이름 입력
def click_tab_name(wd, click_tab_name):
    aalc(wd, click_tab_name)
    print(f'{click_tab_name} 탭 선택')


# tab : 탭을 보여주는 카테고리 / 전체 : 'home' / 라이프 선택 상태 : 'life'
# tab_list : 비교할 탭 이름 리스트
def check_tab_names(wd):
    # sleep(2)
    try:
        women_tab = aal(wd, 'women_tab')
        men_tab = aal(wd, 'men_tab')
        life_tab = aal(wd, 'life_tab')
        best_tab = aal(wd, 'best_tab')
        if all(tab is not None for tab in [women_tab, men_tab, life_tab, best_tab]):
            print("홈 상단 탭 확인 성공")
        else:
            print(f'홈 상단 탭 확인 실패')
            raise Exception(f'홈 상단 탭 확인 실패')
    except NoSuchElementException:
        print(f'홈 상단 탭 확인 실패')
        raise Exception(f'홈 상단 탭 확인 실패')


def click_dynamic_gate(wd):
    # 큐레이션 확인
    #sleep(1)
    curation = aal(wd, 'com.the29cm.app29cm:id/frontItems')
    if curation == None:
        pass
    else:
        swipe_control(wd, curation, 'left', 50)

    # 4. 다이나믹 게이트 2번째 줄, 2번째 선택
    #sleep(1)
    dynamic_layer = aal(wd, 'com.the29cm.app29cm:id/dynamicItems')
    dynamic_button_title = aal(wd, 'dynamic_button_gift')
    if dynamic_button_title == None:
        swipe_control(wd, dynamic_layer, 'left', 50)
        dynamic_button_title = aal(wd, 'dynamic_button_gift')
    button_title = dynamic_button_title.text
    dynamic_button_title.click()
    #sleep(3)
    return button_title


def check_dynamic_gate_gift_page(wd, dynamic_gate_btn_name):
    gift_title = aal(wd, 'com.the29cm.app29cm:id/txtPageTitle').text

    if gift_title == dynamic_gate_btn_name:
        print(f'다이나믹 게이트 타이틀 확인 : {gift_title}/{dynamic_gate_btn_name}')
    else:
        print(f'다이나믹 게이트 타이틀 확인 실패 : {gift_title}/{dynamic_gate_btn_name}')
        raise Exception('다이나믹 게이트 타이틀 확인 실패')


def check_for_duplicate_banner_contents(self):
    # 홈화면 배너 API 호출
    banner_data = home_banner_info(self)
    banner_ids = banner_data['banner_ids']
    banner_contents = banner_data['banner_contents']

    # 모든 홈 배너의 id와 contents의 중복 여부를 확인
    check_id = len(banner_ids) != len(set(banner_ids))
    check_contents = len(banner_contents) != len(set(banner_contents))

    if not check_id:
        if not check_contents:
            print('중복된 홈 배너 id와 컨텐츠 없음 확인')
        else:
            print('중복된 홈 배너 id는 없으나, 동일한 컨텐츠 있음 확인')
    else:
        print(f'중복된 홈 배너 없음 확인 실패')
        raise Exception('중복된 홈 배너 없음 확인 실패')


def save_banner_title(wd):
    banner_title_set = []

    try:
        #sleep(3)
        for i in range(0, 5):
            sleep(2.5)
            home_banner_title = aal(wd, 'com.the29cm.app29cm:id/title')
            if home_banner_title == None:
                print("타이틀 없는 배너")
            else:
                home_banner_title = home_banner_title.text
            banner_title_set.append(home_banner_title)
    except NoSuchElementException:
        print("타이틀 없는 배너")
        pass

    banner_title_set = set(banner_title_set)
    # API 호출 배너 리스트와 저장된 홈 배너 리스트 비교 (저장한 홈 배너 리스트 안에 호출한 리스트가 포함되면 pass)
    return banner_title_set


def check_home_banner_title(self, home_banner_title):
    # 홈화면 배너 api 호출하여 타이틀 저장
    api_banner_title = home_banner_info(self)['banner_titles']

    # API 호출 배너 리스트와 저장된 홈 배너 리스트 비교 (저장한 홈 배너 리스트 안에 호출한 리스트가 포함되면 pass)
    if any(banner in api_banner_title for banner in home_banner_title):
        print('홈 배너 확인')
    else:
        print(f'홈 배너 확인 실패: {set(home_banner_title).difference(set(api_banner_title))}')
        raise Exception('홈 배너 확인 실패')


def check_scroll_to_recommended_contents(wd):
    for _ in range(10):
        try:
            element = aal(wd, 'c_추천 상품')
            if element == None:
                pass
            elif element.is_displayed():
                break
        except:
            pass
        # 요소를 찾지 못하면 아래로 스크롤
        scroll_control(wd, "D", 50)
        #sleep(2)

    guide_text = aal(wd, 'com.the29cm.app29cm:id/title')

    if guide_text.text == '당신을 위한 추천 상품':
        print('홈화면 추천 타이틀 확인')
    else:
        print(f'홈화면 추천 타이틀 확인 실패: {guide_text.text}')
        raise Exception('홈화면 추천 타이틀 확인 실패')


def scroll_to_feed_contents_feed_title_1st(wd, feed_title):
    found_element = None
    for _ in range(15):
        try:
            # 첫번째 피드 타이틀와 일치하는 요소 찾기
            element = aal(wd, 'com.the29cm.app29cm:id/txtFeedTitle')
            if element == None:
                pass
            elif element.text == feed_title:
                found_element = element
                print(f"첫번째 피드 타이틀  : {feed_title} 확인")
                print(f"피드 컨텐츠 추가 노출 확인 : {element.text}")
                break
        except NoSuchElementException:
            pass
        # 스크롤 액션 수행
        scroll_control(wd, 'D', 50)

    if found_element is None:
        print('피드 컨텐츠 노출 확인 실패')
        raise Exception('피드 컨텐츠 노출 확인 실패')


def scroll_to_feed_contents_feed_contain_item(wd):
    # 스크롤
    while True:
        # 원하는 요소를 찾으면 스크롤 종료
        element = aal(wd, 'com.the29cm.app29cm:id/products')
        if element == None:
            pass
        else:
            scroll_control(wd, 'D', 10)
            break
        # 스크롤 액션 수행
        scroll_control(wd, 'D', 50)
        #sleep(2)


def check_heartIcon_is_selected(wd):
    # 하트 이미 선택되었는지 확인
    heart_element = aal(wd, 'com.the29cm.app29cm:id/heartIcon')
    is_selected = heart_element.is_selected()
    if is_selected:
        print("하트 선택된 상태 확인")
        heart_element.click()
        print("하트 선택 해제")
    else:
        print("하트 선택되지 않은 상태 확인")


def save_contents_like_count(wd):
    before_like_count_element = aal(wd, 'com.the29cm.app29cm:id/heartCount')
    if before_like_count_element == None:
        com_utils.element_control.scroll_control(wd, 'D', 50)
        com_utils.element_control.scroll_control(wd, 'D', 40)
    before_like_count_element = aal(wd, 'com.the29cm.app29cm:id/heartCount')
    before_like_count = before_like_count_element.text
    print(f'하트갯수 확인 : {before_like_count}')
    # 쉼표를 제거한 문자열 생성
    before_like_count = before_like_count.replace(',', '')
    # 문자열을 정수로 변환
    before_like_count = int(before_like_count)
    return before_like_count


def click_contents_like_btn(wd):
    aalc(wd, 'com.the29cm.app29cm:id/heartCount')


def check_increase_like_count(heart_count, heart_select):
    if heart_select == heart_count + 1:
        print('피드 아이템 좋아요 개수 증가 확인')
    else:
        print(f'피드 아이템 좋아요 개수 증가 확인 실패: {heart_count} / {heart_select}')
        raise Exception('피드 아이템 좋아요 개수 증가 확인 실패')


def check_decrease_like_count(heart_count, heart_unselect):
    if heart_unselect == heart_count:
        print('피드 아이템 좋아요 개수 차감 확인')
    else:
        print(f'피드 아이템 좋아요 개수 차감 확인 실패: {heart_count} / {heart_unselect}')
        raise Exception('피드 아이템 좋아요 개수 차감 확인 실패')


def save_contents_product_name(wd):
    # 우먼 탭의 첫번째 피드의 첫번째 상품 선택
    first_product_title = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/productName"]')
    print(f'첫번째 상품명 : {first_product_title[0].text}')
    first_product_title_text = first_product_title[0].text

    return first_product_title_text


def save_contents_product_price(wd):
    first_product_price = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/lastSalePrice"]')
    print(f'첫번째 상품가격 : {first_product_price[0].text}')
    first_product_price_text = first_product_price[0].text
    first_product_price = first_product_price_text.replace(",", "")
    first_product_price = int(first_product_price)

    return first_product_price


def click_contents_product(wd):
    first_product_title = aals(wd, '//*[@resource-id="com.the29cm.app29cm:id/productName"]')
    print(f'첫번째 상품명 : {first_product_title[0].text}')
    first_product_title[0].click()
    close_bottom_sheet(wd)


def check_app_evaluation_popup(wd):
    # 앱평가 발생 시 팝업 제거
    app_evaluation = aals(wd, "//*[contains(@text, '29CM 앱을 어떻게 생각하시나요?')]")
    if len(app_evaluation) == 0:
        pass
    else:
        aalc(wd, "//*[contains(@text, '좋아요')]")
        aalc(wd, "//*[contains(@text, '나중에 하기')]")
