import logging
import datetime
import sys
import clipboard

from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from com_utils.element_control import *

def product_preparation_testcase(self, wd, err_msg=[]):
    try:
        # cookie 값 적용을 위한 새로 고침
        wd.refresh()

        # 주문/배송
        menu_lists = wd.find_elements(By.CLASS_NAME, 'css-0.e1bworxc6')
        for menu_list in menu_lists:
            if menu_list.text == '주문/배송':
                menu_list.click()
                break
        class_find_click(wd, 'css-gjb0gh.e1bworxc4')
        test_msg = ['주문/배송 클릭 성공']

        # 상품 준비
        sub_menu_area = wd.find_element(By.CLASS_NAME, 'css-1nlgohn.e1bworxc0')
        sub_menu_lists = sub_menu_area.find_elements(By.CLASS_NAME, 'css-a6b5ur.ea2s4ph0')
        for sub_menu_list in sub_menu_lists:
            if sub_menu_list.text == '상품 준비':
                sub_menu_list.click()
                break
        test_msg.append('상품 준비 클릭 성공')

        # 캘린더
        sleep(1)
        today_text = datetime.datetime.now()
        class_find_click(wd, 'css-10jlh5y.e1btawrq1')
        ## 일자 입력을 위해 기존 date값 삭제
        class_find_click(wd, 'css-1lqseu.e1d6ytke2')
        sleep(0.1)
        calendar_box = wd.find_element(By.CLASS_NAME, 'css-1lqseu.e1d6ytke2.focus-visible')
        calendar_box.send_keys(Keys.COMMAND, 'a')
        sleep(0.1)
        calendar_box.send_keys(Keys.BACKSPACE)
        ## 캘린더 날짜영역
        date_area = wd.find_element(By.CLASS_NAME, 'e6gwe01.css-1hhc1io.echu4tu1')
        date_lists = date_area.find_elements(By.CLASS_NAME, 'css-qziku3.e1vjyn3z3')
        ## 지난달로도 표시되는 일자일 경우 비교하여 이번달 날짜 선택하도록
        today_elements = [date_list for date_list in date_lists if date_list.text == str(today_text.day)]
        if len(today_elements) == 1:
            today_elements[0].click()
        else:
            today_elements[1].click()
        test_msg.append('캘린더 날짜 지정 성공')
        sleep(0.1)
        # 확인 클릭
        class_find_click(wd, 'css-1f7yrc3.e19bp7yq3')
        sleep(0.5)
        ## 날짜 정합성 체크
        class_find_click(wd, 'css-1lqseu.e1d6ytke2')
        sleep(0.1)
        calendar_box = wd.find_element(By.CLASS_NAME, 'css-1lqseu.e1d6ytke2.focus-visible')
        calendar_box.send_keys(Keys.COMMAND, 'a')
        calendar_box.send_keys(Keys.COMMAND, 'c')
        clipboard_text = clipboard.paste()
        date_text = str(today_text)[:10]
        date_text = date_text.replace('-', '.')
        if date_text + ' - ' + date_text == clipboard_text:
            test_msg.append('날짜 지정 성공')
        else:
            err_msg.append('날짜 지정 실패')
            Exception

        # 검색하기
        class_find_click(wd, 'css-1doqodw.e19bp7yq3')
        sleep(1)

        # 검색결과 table column 명 검증
        found_tables = []
        for num in range(len(self.conf['column_name'])):
            found_tables.append(wd.find_element(By.XPATH, '//*[@id="__next"]/section/section/main/div[2]/div[2]/div[1]'
                                                          f'/div[2]/div[1]/div/table/thead/tr/th[{num+2}]'))
        for num in range(len(found_tables)):
            if found_tables[num].text == self.conf['column_name'][num]:
                test_msg.append(f'검색결과 {found_tables[num].text} 컬럼명 확인')
            else:
                err_msg.append('컬럼명 불일치')
        found_tables.clear()

    except Exception:
        wd.save_screenshot(f'screenshot/{sys._getframe().f_code.co_name}.png')
        logging.exception('error log')

    finally:
        return test_msg, err_msg