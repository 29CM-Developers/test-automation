from time import sleep
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc


def active_memo_app(wd):
    wd.activate_app('com.apple.mobilenotes')


def terminate_memo_app(wd):
    wd.terminate_app('com.apple.mobilenotes')


def click_add_memo_btn(wd):
    try:
        ial(wd, '공유')
        click_delete_memo_btn(wd)
        ialc(wd, '새로운 메모')
    except NoSuchElementException:
        ialc(wd, '새로운 메모')


def click_delete_memo_btn(wd):
    ialc(wd, '더 보기')
    ialc(wd, '삭제')


def paste_link(wd):
    text_field = ial(wd, '//XCUIElementTypeTextView')
    ialc(wd, text_field)
    ialc(wd, 'c_붙여넣기')
    click_complete_btn(wd)


def click_complete_btn(wd):
    ialc(wd, '완료')


def click_link(wd):
    ialc(wd, 'c_product.29cm.co.kr')
    sleep(3)
