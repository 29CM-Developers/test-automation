from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
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
            start_y = size["height"] * 0.5
            end_y = size["height"] * 0.2
            duration_ms = 1000  # 스크롤 동작 시간 (밀리초)
            wd.swipe(start_x, start_y, start_x, end_y, duration_ms)
            sleep(2)

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
            start_y = size["height"] * 0.5
            end_y = size["height"] * 0.2
            duration_ms = 1000  # 스크롤 동작 시간 (밀리초)
            wd.swipe(start_x, start_y, start_x, end_y, duration_ms)
            sleep(2)

def scroll(wd):
        # 요소를 찾지 못하면 아래로 스크롤
        size = wd.get_window_size()
        start_x = size["width"] / 2
        start_y = size["height"] * 0.5
        end_y = size["height"] * 0.2
        duration_ms = 1000  # 스크롤 동작 시간 (밀리초)
        wd.swipe(start_x, start_y, start_x, end_y, duration_ms)
        sleep(2)

# 특정 영역 스와이프 동작 -> 좌우, 중앙으로부터 몇 % 스와이프 지정
def swipe_control(wd, element, direction, percent):
    # 특정 요소의 위치와 사이즈 값
    location = element.location
    size = element.size

    # 특정 요소의 중앙을 시작점으로 지정
    start_x = location['x'] + (size['width'] / 2)
    start_y = location['y'] + (size['height'] / 2)

    # 디바이스 사이즈
    window_size = wd.get_window_size()

    # 움직을 x값을 디바이스 사이즈의 30%로 지정
    move_x = window_size['width'] * (percent / 100)

    # x축 기준 시작점에서 디바이스 사이즈의 30%만큼 좌측으로 이동
    actions = ActionChains(wd)
    actions.w3c_actions = ActionBuilder(wd, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    if direction == 'left':
        actions.w3c_actions.pointer_action.move_to_location((start_x - move_x), start_y)
    elif direction == 'right':
        actions.w3c_actions.pointer_action.move_to_location((start_x + move_x), start_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


# 좌우로 스와이프 함수 정의
def swipe_right_to_left(wd, element):
    # 특정 요소의 위치와 사이즈 값
    location = element.location
    size = element.size

    # 특정 요소의 중앙을 시작점으로 지정
    start_x = location['x'] + (size['width'] / 2)
    start_y = location['y'] + (size['height'] / 2)

    # 디바이스 사이즈
    window_size = wd.get_window_size()

    # 움직을 x값을 디바이스 사이즈의 30%로 지정
    move_x = window_size['width'] * 0.3

    # x축 기준 시작점에서 디바이스 사이즈의 30%만큼 좌측으로 이동
    actions = ActionChains(wd)
    actions.w3c_actions = ActionBuilder(wd, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location((start_x - move_x), start_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


def swipe_left_to_right(wd, element):
    location = element.location
    size = element.size

    start_x = location['x'] + (size['width'] / 2)
    start_y = location['y'] + (size['height'] / 2)

    window_size = wd.get_window_size()

    move_x = window_size['width'] * 0.3

    # x축 기준 시작점에서 디바이스 사이즈의 30%만큼 우측으로 이동
    actions = ActionChains(wd)
    actions.w3c_actions = ActionBuilder(wd, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location((start_x + move_x), start_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()

def scroll_to_element_with_text(wd,text):
    for _ in range(10):
        try:
            element = wd.find_element(By.XPATH, f"//*[contains(@text, '{text}')]")
            print(f"element : {element.text}")
            if element.is_displayed():
                print("아이템 발견")
                return element
        except:
            pass

        # 요소를 찾지 못하면 아래로 스크롤
        size = wd.get_window_size()
        start_x = size["width"] / 2
        start_y = size["height"] * 0.5
        end_y = size["height"] * 0.2
        duration_ms = 1000  # 스크롤 동작 시간 (밀리초)
        wd.swipe(start_x, start_y, start_x, end_y, duration_ms)
        sleep(2)

    return element

def scroll_up_to_element_id(wd, element_id):
    for _ in range(10):
        try:
            element = wd.find_element(AppiumBy.ACCESSIBILITY_ID, element_id)
            print(f"element : {element.get_attribute('content-desc')}")
            if element.is_displayed():
                print("아이템 발견")
                return element
        except:
            pass

        # 요소를 찾지 못하면 아래로 스크롤
        size = wd.get_window_size()
        start_x = size["width"] / 2
        start_y = size["height"] * 0.2
        end_y = size["height"] * 0.5
        duration_ms = 1000  # 스크롤 동작 시간 (밀리초)
        wd.swipe(start_x, start_y, start_x, end_y, duration_ms)
        sleep(2)

    return element
def scroll_control(wd, direction, percent):

    size = wd.get_window_size()
    start_x = size["width"] / 2
    duration_ms = 1000  # 스크롤 동작 시간 (밀리초)

    # x축 기준 시작점에서 디바이스 사이즈의 30%만큼 좌측으로 이동
    if direction == 'U':
        start_y = size["height"] * 0.5
        end_y = (size["height"] * 0.5) + (size["height"] * 0.01 * percent)
        wd.swipe(start_x, start_y, start_x, end_y, duration_ms)
    elif direction == 'D':
        start_y = size["height"] * 0.5
        end_y = (size["height"] * 0.5) - (size["height"] * 0.01 * percent)
        wd.swipe(start_x, start_y, start_x, end_y, duration_ms)
    sleep(2)


def element_scroll_control(wd, element, direction, percent):
    # 특정 요소의 위치와 사이즈 값
    location = element.location
    size = element.size

    # 특정 요소의 중앙을 시작점으로 지정
    start_x = location['x'] + (size['width'] / 2)
    start_y = location['y'] + (size['height'] / 2)

    # 디바이스 사이즈
    window_size = wd.get_window_size()
    move_y = window_size['height'] * (percent / 100)

    duration_ms = 1000

    if direction == 'U':
        end_y = start_y + move_y
        wd.swipe(start_x, start_y, start_x, end_y, duration_ms)
    elif direction == 'D':
        end_y = start_y - move_y
        wd.swipe(start_x, start_y, start_x, end_y, duration_ms)
    sleep(2)
