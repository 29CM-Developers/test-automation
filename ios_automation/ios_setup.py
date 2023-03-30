from appium import webdriver


def mpark_setup():
    iOS_caps = {}
    iOS_caps['platformName'] = 'iOS'
    iOS_caps['platformVersion'] = '15.5'
    iOS_caps['deviceName'] = 'iPhone'
    iOS_caps['automationName'] = 'XCUITest'
    iOS_caps['newCommandTimeout'] = 300
    iOS_caps['bundleId'] = '{{bundle id}}'
    iOS_caps['noReset'] = True
    iOS_caps['udid'] = '{{udid_string}}'
    iOS_caps['xcodeSigningId'] = 'iPhone Developer'
    iOS_caps['xcodeOrgId'] = '{{developer team id}}'
    iOS_caps['simpleIsVisibleCheck'] = True
    iOS_caps['useJSONSource'] = True
    wd = webdriver.Remote('http://0.0.0.0:4724/wd/hub', capabilities=iOS_caps)

    return wd, iOS_caps