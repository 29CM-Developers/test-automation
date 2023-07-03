from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions


# def mpark_setup():
#     android_options = {}
#     android_options['platformName'] = 'Android'
#     android_options['platformVersion'] = '{{os version}}'
#     android_options['deviceName'] = '{{device name}}'
#     android_options['automationName'] = 'UIAutomator2'
#     android_options['newCommandTimeout'] = 300
#     android_options['appPackage'] = '{{apppackage_name}}'
#     android_options['appActivity'] = '{{appactivity_name}}'
#     android_options['noReset'] = True
#     android_options['udid'] = '{{udid_string}}'
#     android_options['goog:chromeOptions'] = {'androidPackage': 'app package name', 'androidUseRunningApp': True,
#                                           'w3c': False}
#     wd = webdriver.Remote('http://0.0.0.0:4723/wd/hub', capabilities=android_options)
#
#     return wd, android_options


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
    wd = webdriver.Remote('http://0.0.0.0:4723/wd/hub', options=android_options)

    return wd, android_options
