from time import sleep
from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc, scroll_control


def click_safari_menu(wd):
    wd.activate_app('com.apple.Preferences')
    for i in range(0, 5):
        try:
            element = ial(wd, 'Safari')
            if element.is_displayed():
                ialc(wd, element)
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, "D", 50)


def click_safari_clean_data(wd):
    for i in range(0, 5):
        try:
            element = ial(wd, 'c_데이터 지우기')
            if element.is_displayed():
                ialc(wd, element)
                ialc(wd, 'c_방문 기록 및 데이터 지우기')
                ialc(wd, 'c_탭 유지')
                break
        except NoSuchElementException:
            pass
        scroll_control(wd, "D", 50)
    sleep(2)
    wd.terminate_app('com.apple.Preferences')
