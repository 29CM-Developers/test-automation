from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from com_utils.element_control import aal, aalc, tap_control
from time import sleep


def close_bottom_sheet(wd):
    try:
        sleep(2)
        wd.find_element(AppiumBy.ID, 'com.the29cm.app29cm:id/com_braze_inappmessage_html')
        wd.find_element(AppiumBy.XPATH, "//*[contains(@text, '닫기')]").click()
        print('바텀 시트 노출되어 닫기 동작')

    except NoSuchElementException:
        print('바텀 시트 미노출')
        pass


def close_pdp_bottom_sheet(wd):
    try:
        bottom_sheet = aal(wd, 'c_유용한 기능을 소개해요')
        if bottom_sheet == None:
            print('바텀 시트 미노출')
        else:
            tap_control(wd)
            print('유용한 기능을 소개해요 바텀 시트 노출되어 닫기 동작')

    except NoSuchElementException:
        print('바텀 시트 미노출')
        pass



def close_like_bottom_sheet(wd):
    try:
        sleep(2)
        braze = aal(wd, 'com.the29cm.app29cm:id/design_bottom_sheet')
        if braze == None:
            print('바텀 시트 미노출')
        else:
            print('바텀 시트 노출확인')
            like_bottom_sheet = aal(wd, '다음에')
            if like_bottom_sheet == None:
                print('바텀 시트 다음에 문구 미노출')
                pass
            else:
                aalc(wd, '다음에')
                print('바텀 시트 노출되어 닫기 동작')

    except NoSuchElementException:
        print('바텀 시트 미노출')
        pass
