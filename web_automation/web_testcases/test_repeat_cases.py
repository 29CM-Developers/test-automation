import logging
import datetime
import sys
import clipboard

from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from com_utils.element_control import *

def create_item(self, wd, err_msg=[]):
    try:
        # cookie 값 적용을 위한 새로 고침
        wd.refresh()
        test_msg = ['페이지 새로고침 성공']

        # 상품 메뉴 클릭
        class_find_click(wd, 'css-0.e1bworxc6')
        # 상품 등록 클릭
        class_find_click(wd, 'css-x1kjqb.ea2s4ph1')
        sleep(1)

        # 대카테고리 클릭
        id_find_click(wd, 'react-select-instance-1st_category-placeholder')
        # 대카테고리 목록 클릭
        id_find_click(wd, 'react-select-instance-1st_category-option-0')
        # 중카테고리 클릭
        id_find_click(wd, 'react-select-instance-2nd_category-placeholder')
        # 중카테고리 목록 클릭
        id_find_click(wd, 'react-select-instance-2nd_category-option-1')
        # 소카테고리 클릭
        id_find_click(wd, 'react-select-instance-3rd_category-placeholder')
        # 소카테고리 목록 클릭
        id_find_click(wd, 'react-select-instance-3rd_category-option-1')

        # 상품명 입력
        id_find_sendkeys(wd, 'product_name', '이것은 상품명 입니다')
        # 브랜드 클릭
        id_find_click(wd, 'brand_name')
        sleep(1)
        # 브랜드 선택
        brand = id_find(wd, 'react-select-instance-brand_name-option-0')
        for num in range(10):
            if id_find(wd, f'react-select-instance-brand_name-option-{num}').text == 'mpark brand':
                id_find_click(wd, f'react-select-instance-brand_name-option-{num}')
                break

        sleep(1)
        test_msg = ['주문/배송 클릭 성공']

    except Exception:
        wd.save_screenshot(f'screenshot/{sys._getframe().f_code.co_name}.png')
        logging.exception('error log')

    finally:
        return test_msg, err_msg