from ios_automation.page_action.bottom_sheet import find_icon_and_close_bottom_sheet, close_bottom_sheet
from com_utils.element_control import ialc
from ios_automation.page_action import like_page, selection_page
from ios_automation.page_action.select_category_page import test_select_category


def move_to_home(wd):
    ialc(wd, 'c_HOME')
    find_icon_and_close_bottom_sheet(wd)


def logout_and_move_to_home(wd):
    ialc(wd, 'c_HOME')
    test_select_category(wd)
    find_icon_and_close_bottom_sheet(wd)


def move_to_category(wd):
    ialc(wd, 'c_CATEGORY')
    find_icon_and_close_bottom_sheet(wd)


def move_to_search(wd):
    ialc(wd, 'c_SEARCH')
    close_bottom_sheet(wd)


def move_to_like(wd):
    ialc(wd, 'c_LIKE')
    selection_page.click_close_selection_pop_up(wd)
    close_bottom_sheet(wd)
    like_page.close_noti_bottom_sheet(wd)
    like_page.close_brand_recommended_page(wd)


def move_to_my(wd):
    ialc(wd, 'c_MY')
    find_icon_and_close_bottom_sheet(wd)
