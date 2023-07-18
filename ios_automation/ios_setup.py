from appium import webdriver
from appium.options.common import AppiumOptions


# def mpark_setup():
#     iOS_caps = {}
#     iOS_caps['platformName'] = 'iOS'
#     iOS_caps['platformVersion'] = '15.5'
#     iOS_caps['deviceName'] = 'iPhone'
#     iOS_caps['automationName'] = 'XCUITest'
#     iOS_caps['newCommandTimeout'] = 300
#     iOS_caps['bundleId'] = '{{bundle id}}'
#     iOS_caps['noReset'] = True
#     iOS_caps['udid'] = '{{udid_string}}'
#     iOS_caps['xcodeSigningId'] = 'iPhone Developer'
#     iOS_caps['xcodeOrgId'] = '{{developer team id}}'
#     iOS_caps['simpleIsVisibleCheck'] = True
#     iOS_caps['useJSONSource'] = True
#     wd = webdriver.Remote('http://0.0.0.0:4724/wd/hub', capabilities=iOS_caps)
#
#     return wd, iOS_caps


def dajjeong_setup():
    iOS_options = AppiumOptions()
    iOS_options.set_capability('platformName', 'iOS')
    iOS_options.set_capability('platformVersion', '16.2')
    iOS_options.set_capability('deviceName', '14pro')
    iOS_options.set_capability('udid', '00008120-001C25A83A9BC01E')
    iOS_options.set_capability('automationName', 'XCUITest')
    iOS_options.set_capability('newCommandTimeout', 300)
    iOS_options.set_capability('bundleId', 'kr.co.29cm.App29CM')
    iOS_options.set_capability('noReset', True)
    iOS_options.set_capability('xcodeSigningId', 'iPhone Developer')
    iOS_options.set_capability('xcodeOrgId', '323Z55V788')
    iOS_options.set_capability('simpleIsVisibleCheck', True)
    iOS_options.set_capability('useJSONSource', True)
    wd = webdriver.Remote('http://0.0.0.0:4724/wd/hub', options=iOS_options)

    return wd, iOS_options
