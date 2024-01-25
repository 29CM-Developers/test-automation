from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions


def dajjeong_setup():
    android_options = AppiumOptions()
    android_options.set_capability('platformName', 'Android')
    android_options.set_capability('platformVersion', '13')
    android_options.set_capability('deviceName', 'Flip3')
    android_options.set_capability('udid', 'R5CR80MX0WZ')
    android_options.set_capability('automationName', 'UIAutomator2')
    android_options.set_capability('newCommandTimeout', 300)
    android_options.set_capability('appPackage', 'com.the29cm.app29cm')
    android_options.set_capability('appActivity', 'com.the29cm.app29cm.intro.IntroActivity')
    android_options.set_capability('noReset', True)
    android_options.set_capability("goog:chromeOptions", {"androidPackage": "com.the29cm.app29cm",
                                                          "androidUseRunningApp": True, "w3c": False})
    wd = webdriver.Remote('http://0.0.0.0:4923/wd/hub', options=android_options)

    return wd, android_options

def mpark_setup():
    android_options = AppiumOptions()
    android_options.set_capability("platformName", "Android")
    android_options.set_capability("platformVersion", "13")
    android_options.set_capability("deviceName", "Galaxy S21 5G")
    android_options.set_capability("automationName", "UIAutomator2")
    android_options.set_capability("appPackage", "com.the29cm.app29cm")
    android_options.set_capability("appActivity", "com.the29cm.app29cm.intro.IntroActivity")
    android_options.set_capability("udid", "R3CRC0NFQEZ")
    android_options.set_capability("newCommandTimeout", 300)
    android_options.set_capability("noReset", True)
    android_options.set_capability("unlockType", "pin")
    android_options.set_capability("unlockKey", "292929")
    android_options.set_capability("goog:chromeOptions", {"androidPackage": "com.the29cm.app29cm", "androidUseRunningApp": True, "w3c": False})

    wd = webdriver.Remote('http://0.0.0.0:4723/wd/hub', options=android_options)

    return wd, android_options

def hhj2008_setup():

    android_options = AppiumOptions()
    android_options.set_capability("platformName", "Android")
    android_options.set_capability("platformVersion", "13")
    android_options.set_capability("deviceName", "ZFilp4")
    android_options.set_capability("automationName", "UIAutomator2")
    android_options.set_capability("appPackage", "com.the29cm.app29cm")
    android_options.set_capability("appActivity", "com.the29cm.app29cm.intro.IntroActivity")
    android_options.set_capability("newCommandTimeout", 300)
    android_options.set_capability("udid", 'R3CT70R2QFF')
    android_options.set_capability("noReset", True)
    android_options.set_capability("goog:chromeOptions",
                                   {"androidPackage": "com.the29cm.app29cm", "androidUseRunningApp": True,
                                    "w3c": False})
    android_options.set_capability("unlockType", "pin")
    android_options.set_capability("unlockKey", "292929")

    wd = webdriver.Remote('http://0.0.0.0:4823/wd/hub', options=android_options)

    #android_options.set_capability("platformName", "Android")
    return wd, android_options

def note20_setup():
    android_options = AppiumOptions()
    android_options.set_capability("platformName", "Android")
    android_options.set_capability("platformVersion", "13")
    android_options.set_capability("deviceName", "Galaxy Note20 5G")
    android_options.set_capability("automationName", "UIAutomator2")
    android_options.set_capability("systemPort", "8201")
    android_options.set_capability("appPackage", "com.the29cm.app29cm")
    android_options.set_capability("appActivity", "com.the29cm.app29cm.intro.IntroActivity")
    android_options.set_capability("udid", "192.168.103.13:7401")
    android_options.set_capability("newCommandTimeout", 300)
    android_options.set_capability("noReset", True)
    android_options.set_capability("unlockType", "pin")
    android_options.set_capability("unlockKey", "292929")
    android_options.set_capability("goog:chromeOptions", {"androidPackage": "com.the29cm.app29cm", "androidUseRunningApp": True, "w3c": False})

    wd = webdriver.Remote('http://0.0.0.0:4733/wd/hub', options=android_options)

    return wd, android_options

def s22_setup():
    android_options = AppiumOptions()
    android_options.set_capability("platformName", "Android")
    android_options.set_capability("platformVersion", "13")
    android_options.set_capability("deviceName", "Galaxy S22")
    android_options.set_capability("automationName", "UIAutomator2")
    android_options.set_capability("systemPort", "8202")
    android_options.set_capability("appPackage", "com.the29cm.app29cm")
    android_options.set_capability("appActivity", "com.the29cm.app29cm.intro.IntroActivity")
    android_options.set_capability("udid", "192.168.103.13:7405")
    android_options.set_capability("newCommandTimeout", 300)
    android_options.set_capability("noReset", True)
    android_options.set_capability("unlockType", "pin")
    android_options.set_capability("unlockKey", "292929")
    android_options.set_capability("goog:chromeOptions", {"androidPackage": "com.the29cm.app29cm", "androidUseRunningApp": True, "w3c": False})

    wd = webdriver.Remote('http://0.0.0.0:4734/wd/hub', options=android_options)

    return wd, android_options