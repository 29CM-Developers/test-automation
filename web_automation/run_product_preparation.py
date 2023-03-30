import json
import requests
import unittest

from nose.tools import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from web_testcases import product_preparation, test_repeat_cases
from selenium.webdriver.support.wait import WebDriverWait

class WebTestAutomation(unittest.TestCase):

    def setUp(self):
        # get test data and Chrome browser auth cookies
        with open('../info.json') as js:
            self.conf = json.load(js)
        # token 갱신 시 json 파일의 _frtn_qa 값 변경
        with open('../cookies.json') as ck:
            self.test_cookies = json.load(ck)

        # set ChromeDriver
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        service = ChromeService(executable_path='/usr/local/bin/chromedriver')
        self.wd = webdriver.Chrome(service=service, options=options)

        # set authority
        self.account = 'partner'
        if self.account == 'admin':
            # admin page
            self.wd.get('https://qa-internal.29cm.co.kr')
        else:
            # partner page
            self.wd.get('https://qa-seller.29cm.co.kr')

        # set auth cookies
        for ck in self.test_cookies:
            self.wd.add_cookie(ck)
        # set hold time
        self.wd.implicitly_wait(5)
        self.wait = WebDriverWait(self.wd, 10)
        self.wd.maximize_window()

    def tearDown(self):
        self.wd.quit()

    def test_open_page(self):
        test_msg, err_msg = product_preparation.product_preparation_testcase(self, self.wd)
        for msg in test_msg:
            print(msg)

    def test_repeat_run(self):
        test_repeat_cases.create_item(self, self.wd)


if __name__ == '__main__':
    unittest.main()