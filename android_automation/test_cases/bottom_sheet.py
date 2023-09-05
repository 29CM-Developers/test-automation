from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
def test_bottom_sheet(wd):
    try:
        wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/com_braze_inappmessage_html')
        wd.find_element(AppiumBy.XPATH, "//*[contains(@text, '닫기')]").click()
        print('바텀 시트 노출되어 닫기 동작')

    except NoSuchElementException:
        print('바텀 시트 미노출')
        pass
