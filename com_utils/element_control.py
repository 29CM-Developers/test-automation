import logging

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
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
# 좌우로 스와이프 함수 정의
def swipe_right_to_left(wd):
    # 화면 크기 가져오기
    window_size = wd.get_window_size()
    width = window_size['width']
    height = window_size['height']

    # 시작점과 끝점 계산
    start_x = int(width * 0.6)
    end_x = int(width * 0.4)
    y = int(height * 0.3)

    # Swipe 동작 설정
    actions = ActionChains(wd)
    actions.w3c_actions = ActionBuilder(wd, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(end_x, y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()

def swipe_left_to_right(wd):
    # 화면 크기 가져오기
    window_size = wd.get_window_size()
    width = window_size['width']
    height = window_size['height']

    # 시작점과 끝점 계산
    start_x = int(width * 0.4)
    end_x = int(width * 0.6)
    y = int(height * 0.3)
    # Swipe 동작 설정
    actions = ActionChains(wd)
    actions.w3c_actions = ActionBuilder(wd, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(end_x, y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()

