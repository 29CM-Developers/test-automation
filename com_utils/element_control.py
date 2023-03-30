from selenium.webdriver.common.by import By


def class_find_click(wd, class_name):
    wd.find_element(By.CLASS_NAME, f'{class_name}').click()


def id_find_click(wd, id_name):
    wd.find_element(By.ID, f'{id_name}').click()


def id_find_sendkeys(wd, id_name, sendkey):
    wd.find_element(By.ID, f'{id_name}').send_keys(f'{sendkey}')


def class_find(wd, class_name):
    wd.find_element(By.CLASS_NAME, f'{class_name}')


def id_find(wd, id_name):
    wd.find_element(By.ID, f'{id_name}')


def classes_find(wd, class_name):
    wd.find_elements(By.CLASS_NAME, f'{class_name}')


def xpath_find(wd, xpath):
    wd.find_element(By.XPATH, f'{xpath}')


def css_find(wd, css):
    wd.find_element(By.CSS_SELECTOR, f'{css}')


def tag_find(wd, tag):
    wd.find_element(By.CSS_SELECTOR, f'{tag}')