from time import sleep
from com_utils.element_control import aal, aalc


def test_select_category(wd):
    try:
        aal(wd, 'c_관심있는 카테고리를 고르세요')
        aalc(wd, 'c_홈으로 건너뛰기')
        sleep(1)
        aalc(wd, 'c_홈으로 건너뛰기')
        print('카테고리 선택 페이지 노출되어 닫기')
    except Exception:
        print('카테고리 선택 페이지 미노출')
        pass
