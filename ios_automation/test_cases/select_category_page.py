from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException


def test_select_category(wd):
    try:
        wd.find_element(AppiumBy.ACCESSIBILITY_ID, '관심있는 카테고리를 고르세요')
        wd.find_element(AppiumBy.XPATH, '(//XCUIElementTypeButton[@name="홈으로 건너뛰기"])[1]').click()
        wd.find_element(AppiumBy.XPATH, '(//XCUIElementTypeButton[@name="홈으로 건너뛰기"])[2]').click()
        print('카테고리 선택 페이지 노출되어 닫기')
    except NoSuchElementException:
        print('카테고리 선택 페이지 미노출')
        pass
