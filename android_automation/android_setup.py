from appium import webdriver


def mpark_setup():
    android_caps = {}
    android_caps['platformName'] = 'Android'
    android_caps['platformVersion'] = '{{os version}}'
    android_caps['deviceName'] = '{{device name}}'
    android_caps['automationName'] = 'UIAutomator2'
    android_caps['newCommandTimeout'] = 300
    android_caps['appPackage'] = '{{apppackage_name}}'
    android_caps['appActivity'] = '{{appactivity_name}}'
    android_caps['noReset'] = True
    android_caps['udid'] = '{{udid_string}}'
    android_caps['goog:chromeOptions'] = {'androidPackage': 'app package name', 'androidUseRunningApp': True,
                                          'w3c': False}
    wd = webdriver.Remote('http://0.0.0.0:4723/wd/hub', capabilities=android_caps)

    return wd, android_caps