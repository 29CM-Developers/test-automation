from selenium.common import NoSuchElementException
from com_utils.element_control import ial, ialc


def click_close_selection_pop_up(wd):
    try:
        ial(wd, 'c_셀렉션 만들기')
        ialc(wd, '다음에 하기')
    except NoSuchElementException:
        pass
