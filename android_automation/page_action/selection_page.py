from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc


def click_close_selection_pop_up(wd):
    try:
        selection = aal(wd, 'c_셀렉션 만들기')
        if selection == None:
            pass
        else :
            aalc(wd, '다음에 하기')
    except NoSuchElementException:
        pass
