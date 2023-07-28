import logging

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


def class_find_click(wd, class_name):
    wd.find_element(By.CLASS_NAME, f'{class_name}').click()


def id_find_click(wd, id_name):
    wd.find_element(By.ID, f'{id_name}').click()


def id_find_sendkeys(wd, id_name, sendkey):
    wd.find_element(By.ID, f'{id_name}').send_keys(f'{sendkey}')


def class_find(wd, class_name):
    wd.find_element(By.CLASS_NAME, f'{class_name}')


def id_find(wd, id_name):
    wd.find_element(By.ID, f'{id_name}')


def classes_find(wd, class_name):
    wd.find_elements(By.CLASS_NAME, f'{class_name}')


def xpath_find(wd, xpath):
    wd.find_element(By.XPATH, f'{xpath}')


def css_find(wd, css):
    wd.find_element(By.CSS_SELECTOR, f'{css}')


def tag_find(wd, tag):
    wd.find_element(By.CSS_SELECTOR, f'{tag}')

def scroll_to_element_id(wd, element_id):

    while True:
        try:
            # 원하는 요소를 찾으면 스크롤 종료
            element = wd.find_element(AppiumBy.ID, element_id)
            break
        except:
            # 요소를 찾지 못하면 아래로 스크롤
            size = wd.get_window_size()
            start_x = size["width"] / 2
            start_y = size["height"] * 0.8
            end_y = size["height"] * 0.2
            duration_ms = 1000  # 스크롤 동작 시간 (밀리초)
            wd.swipe(start_x, start_y, start_x, end_y, duration_ms)

def scroll_to_element_xpath(wd, element_xpath):

    while True:
        try:
            # 원하는 요소를 찾으면 스크롤 종료
            element = wd.find_element(AppiumBy.XPATH, element_xpath)
            break
        except:
            # 요소를 찾지 못하면 아래로 스크롤
            size = wd.get_window_size()
            start_x = size["width"] / 2
            start_y = size["height"] * 0.8
            end_y = size["height"] * 0.2
            duration_ms = 1000  # 스크롤 동작 시간 (밀리초)
            wd.swipe(start_x, start_y, start_x, end_y, duration_ms)

def scroll(wd):
        # 요소를 찾지 못하면 아래로 스크롤
        size = wd.get_window_size()
        start_x = size["width"] / 2
        start_y = size["height"] * 0.8
        end_y = size["height"] * 0.2
        duration_ms = 1000  # 스크롤 동작 시간 (밀리초)
        wd.swipe(start_x, start_y, start_x, end_y, duration_ms)