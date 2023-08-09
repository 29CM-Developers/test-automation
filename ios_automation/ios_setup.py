from appium import webdriver
from appium.options.common import AppiumOptions


def mpark_setup():
    iOS_options = AppiumOptions()
    iOS_options.set_capability("platformName", "iOS")
    iOS_options.set_capability("platformVersion", "16.5.1")
    iOS_options.set_capability("deviceName", "iPhone")
    iOS_options.set_capability("automationName", "XCUITest")
    iOS_options.set_capability("bundleId", "kr.co.29cm.App29CM")
    iOS_options.set_capability("udid", "00008101-001230822151003A")
    iOS_options.set_capability("xcodeSigningId", "iPhone Developer")
    iOS_options.set_capability("xcodeOrgId", "323Z55V788")
    iOS_options.set_capability("newCommandTimeout", 300)
    iOS_options.set_capability("noReset", True)
    iOS_options.set_capability("simpleIsVisibleCheck", True)
    iOS_options.set_capability("useJSONSource", True)

    wd = webdriver.Remote('http://0.0.0.0:4724/wd/hub', options=iOS_options)

    return wd, iOS_options

def dajjeong_setup():
    iOS_options = AppiumOptions()
    iOS_options.set_capability('platformName', 'iOS')
    iOS_options.set_capability('platformVersion', '16.5.1')
    iOS_options.set_capability('deviceName', 'iphone12')
    iOS_options.set_capability('udid', '00008101-001C59593C80001E')
    iOS_options.set_capability('automationName', 'XCUITest')
    iOS_options.set_capability('newCommandTimeout', 300)
    iOS_options.set_capability('bundleId', 'kr.co.29cm.App29CM')
    iOS_options.set_capability('noReset', True)
    iOS_options.set_capability('xcodeSigningId', 'iPhone Developer')
    iOS_options.set_capability('xcodeOrgId', '323Z55V788')
    iOS_options.set_capability('simpleIsVisibleCheck', True)
    iOS_options.set_capability('useJSONSource', True)
    iOS_options.set_capability('usePrebuiltWDA', True)
    iOS_options.set_capability('skipServerInstallation', True)
    wd = webdriver.Remote('http://0.0.0.0:4924/wd/hub', options=iOS_options)

    return wd, iOS_options


def hhj2008_setup():

    iOS_options = AppiumOptions()
    iOS_options.set_capability("platformName", "iOS")
    iOS_options.set_capability("platformVersion", "16.5")
    iOS_options.set_capability("deviceName", "해진홍의 iPhone")
    iOS_options.set_capability("automationName", "XCUITest")
    iOS_options.set_capability("bundleId", "kr.co.29cm.App29CM")
    iOS_options.set_capability("udid", "00008110-0005242A2168401E")
    iOS_options.set_capability("newCommandTimeout", 300)
    iOS_options.set_capability("xcodeSigningId", 'iPhone')
    iOS_options.set_capability("xcodeOrgId", '323Z55V788')
    iOS_options.set_capability("simpleIsVisibleCheck", True)
    iOS_options.set_capability("useJSONSource", True)

    wd = webdriver.Remote('http://0.0.0.0:4824/wd/hub', options=iOS_options)

    return wd, iOS_options

def pro14_setup():
    iOS_options = AppiumOptions()
    iOS_options.set_capability("platformName", "iOS")
    iOS_options.set_capability("platformVersion", "16.6")
    iOS_options.set_capability("deviceName", "mpark iPhone")
    iOS_options.set_capability("automationName", "XCUITest")
    iOS_options.set_capability("systemPort", "8101")
    iOS_options.set_capability("bundleId", "kr.co.29cm.App29CM")
    iOS_options.set_capability("udid", "00008120-00010C640183C01E")
    iOS_options.set_capability("xcodeSigningId", "iPhone Developer")
    iOS_options.set_capability("xcodeOrgId", "323Z55V788")
    iOS_options.set_capability("newCommandTimeout", 300)
    iOS_options.set_capability("noReset", True)
    iOS_options.set_capability("simpleIsVisibleCheck", True)
    iOS_options.set_capability("useJSONSource", True)

    wd = webdriver.Remote('http://0.0.0.0:4743/wd/hub', options=iOS_options)

    return wd, iOS_options

def pro12_setup():
    iOS_options = AppiumOptions()
    iOS_options.set_capability("platformName", "iOS")
    iOS_options.set_capability("platformVersion", "16.5.1")
    iOS_options.set_capability("deviceName", "iPhone12pro")
    iOS_options.set_capability("automationName", "XCUITest")
    iOS_options.set_capability("systemPort", "8102")
    iOS_options.set_capability("bundleId", "kr.co.29cm.App29CM")
    iOS_options.set_capability("udid", "00008101-001230822151003A")
    iOS_options.set_capability("xcodeSigningId", "iPhone Developer")
    iOS_options.set_capability("xcodeOrgId", "323Z55V788")
    iOS_options.set_capability("newCommandTimeout", 300)
    iOS_options.set_capability("noReset", True)
    iOS_options.set_capability("simpleIsVisibleCheck", True)
    iOS_options.set_capability("useJSONSource", True)

    wd = webdriver.Remote('http://0.0.0.0:4744/wd/hub', options=iOS_options)

    return wd, iOS_options