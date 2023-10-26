from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from time import time


def al_click(wd, xpath, text):
    try:
        find_element = wd.find_element(By.XPATH, f'{xpath}')
        print('element 찾음')
        print(find_element.text)
        find_element.screenshot('child.png')
        if find_element.text == text:
            find_element.click()
            print(find_element.text)
        else:
            # other_find_element = find_element.find_elements(By.XPATH, f'{xpath}//following-sibling::*')
            # 형제 element 찾기
            other_find_element = find_element.find_elements(By.XPATH, './/*')
            print(f'형제 element 개수: {len(other_find_element)}')
            print(f'형제 element text: {other_find_element[0].text}')
            if len(other_find_element) > 1:
                for element in other_find_element:
                    if element.text == text:
                        element.click()
                        print('형제 element 찾음')
                        break
            else:
                # 부모 element 찾기
                # parent_find_element = find_element.find_elements(By.XPATH, f'{xpath}/parent::*')
                parent_find_element = wd.find_elements(By.XPATH, f'{xpath}/..')
                print(f'부모 element 개수: {len(parent_find_element)}')
                if len(parent_find_element) > 1:
                    pass
                else:
                    parent_find_element = wd.find_elements(By.XPATH, f'{xpath}/../..')
                    parent_find_element[0].screenshot('second_parent.png')
                    parent_find_element = wd.find_elements(By.XPATH, f'{xpath}/../../..')
                    parent_find_element[0].screenshot('third_parent.png')
    except NoSuchElementException:
        print('element 못찾음')
        try:
            # find_element = wd.find_elements(By.XPATH, f'{xpath}//following-sibling::*')
            find_element = wd.find_elements(By.XPATH, './/*')
            for element in find_element:
                if element.text == text:
                    element.click()
                    print('형제 element 찾음')
                    break
        except NoSuchElementException:
            print('형제 element 중에 못찾음')
            find_element = None

    return find_element


def ial(wd, element_value):
    """
    iOS_all_in_one_locator
    """
    locators = ["ACCESSIBILITY_ID", "IOS_CLASS_CHAIN", "XPATH"]
    for locator in locators:
        try:
            start_time = time()
            element = wd.find_element(getattr(AppiumBy, locator), element_value)
            run_time = f"{time() - start_time:.2f}"
            print(locator + "로 찾은 시간: " + run_time)
            break
        except NoSuchElementException:
            run_time = f"{time() - start_time:.2f}"
            print(locator + "로 못찾은 시간: " + run_time)
            wd.implicitly_wait(0)
            pass
    wd.implicitly_wait(3)
    return element


def ialc(wd, element_value):
    """
    iOS_all_in_one_locator_click
    """
    element = ial(wd, element_value)
    element.click()


def ialk(wd, element_value, text):
    """
    iOS_all_in_one_locator_sendkeys
    """
    element = ial(wd, element_value)
    element.send_keys(text)


def aal(wd, element_value):
    """
    android_all_in_one_locator
    """
    locators = ["ACCESSIBILITY_ID", "ID", "XPATH"]
    for locator in locators:
        try:
            element = wd.find_element(getattr(AppiumBy, locator), element_value)
        except NoSuchElementException:
            pass
        try:
            element = wd.find_element(AppiumBy.XPATH, f"//*[contains(@text, '{element_value}')]")
        except NoSuchElementException:
            pass

    return element


def aalc(wd, element_value):
    """
    android_all_in_one_locator
    """
    element = aal(wd, element_value)
    element.click()


def aalk(wd, element_value, text):
    """
    android_all_in_one_locator
    """
    element = aal(wd, element_value)
    element.send_keys(text)


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
