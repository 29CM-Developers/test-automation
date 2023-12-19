from time import sleep
from ios_automation.page_action.bottom_sheet import find_icon_and_close_bottom_sheet, close_bottom_sheet
from ios_automation.page_action import like_page
from android_automation.page_action import bottom_sheet


# Home 탭으로 이동 딥링크
def move_to_home_iOS(self, wd):
    wd.get(self.conf['deeplink']['home'])
    find_icon_and_close_bottom_sheet(wd)


def move_to_home(self, wd):
    wd.get(self.conf['deeplink']['home'])
    find_icon_and_close_bottom_sheet(wd)


def move_to_category(self, wd):
    wd.get(self.conf['deeplink']['category'])
    find_icon_and_close_bottom_sheet(wd)


def move_to_like(self, wd):
    wd.get(self.conf['deeplink']['like'])
    # LIKE 탭 진입 후, 바텀시트, 노티 바텀시트, 브랜드 추천 페이지 노출 여부 순차적으로 확인
    close_bottom_sheet(wd)
    like_page.close_noti_bottom_sheet(wd)
    like_page.close_brand_recommended_page(wd)


def move_to_my(self, wd):
    wd.get(self.conf['deeplink']['my'])
    find_icon_and_close_bottom_sheet(wd)


def move_to_welove(self, wd):
    wd.get(self.conf['deeplink']['welove'])


def move_to_pdp(wd, product_item_no):
    sleep(5)
    wd.get(f'app29cm://product/{product_item_no}')
    sleep(3)


# Home 탭으로 이동 딥링크
def move_to_home_Android(self, wd):
    wd.get('app29cm://home')
    bottom_sheet.close_bottom_sheet(wd)


def move_to_my_Android(self, wd):
    sleep(5)
    wd.get('app29cm://mypage')
    sleep(1)
    print("홈 > 마이페이지 화면 진입")
    bottom_sheet.close_bottom_sheet(wd)
