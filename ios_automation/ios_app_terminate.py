import unittest

from appium.webdriver.appium_service import AppiumService
from ios_automation.ios_setup import dajjeong_setup


class IOSAppTerminate(unittest.TestCase):
    def test_ios_app_terminate(self):
        # 포트번호와 셋업은 세팅에 맞게 변경해주세요

        self.appium = AppiumService()
        self.appium.start(args=['-p', '4924', '--base-path', '/wd/hub', '--default-capabilities',
                                '{"appium:chromedriverExecutable": "/usr/local/bin"}'])

        # webdriver
        self.wd, self.iOS_cap = dajjeong_setup()
        self.wd.implicitly_wait(3)

        # 앱, wd, appium 순차 종료
        self.wd.terminate_app('kr.co.29cm.App29CM')
        self.wd.quit()
        self.appium.stop()
