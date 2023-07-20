from selenium.webdriver.common.by import By

class LoginPageLocators(object):

    my_page_not_login = 'com.the29cm.app29cm:id/txtLogin'
    login_page_title = '//*[@resource-id="__next"]/android.widget.TextView[1]'
    id_field = '//android.widget.EditText[1]'
    password_field = '//android.widget.EditText[2]'
    login_btn = '//android.widget.Button'
    guide_text = '//*[@resource-id="__next"]/android.view.View/android.widget.TextView'
    wrong_password_guide_text = '//*[@resource-id="__next"]/android.view.View[1]/android.widget.TextView'
    sns_login_apple = '//*[@resource-id="__next"]/android.widget.Button[4]'
    apple_login_pop_up = ''
    my_page_login_name = 'com.the29cm.app29cm:id/txtUserName'
    logout_btn = 'com.the29cm.app29cm:id/btnLogout'
