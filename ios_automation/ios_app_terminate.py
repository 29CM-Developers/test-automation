import unittest

from appium.webdriver.appium_service import AppiumService
from ios_automation.ios_setup import pro12_setup, pro14_setup


class IOSAppTerminate(unittest.TestCase):
    def test_pro12_app_terminate(self):
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4744', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin"}'])

        # webdriver
        self.wd, self.iOS_cap = pro12_setup()
        self.wd.implicitly_wait(3)

        # 앱, wd, appium 순차 종료
        self.wd.terminate_app('kr.co.29cm.App29CM')
        self.wd.quit()
        self.appium.stop()

    def test_pro14_app_terminate(self):
        self.appium = AppiumService()
        self.appium.start(args=['-p', '4743', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin"}'])

        # webdriver
        self.wd, self.iOS_cap = pro14_setup()
        self.wd.implicitly_wait(3)

        # 앱, wd, appium 순차 종료
        self.wd.terminate_app('kr.co.29cm.App29CM')
        self.wd.quit()
        self.appium.stop()
