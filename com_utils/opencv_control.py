import cv2
import pytesseract
import os

from time import sleep
from com_utils.element_control import ial


def screenshot_page(wd):
    device_size = wd.get_window_rect()
    directory = f'{os.getcwd()}/image/'
    screenshot = f'screenshot.png'
    wd.save_screenshot(directory + screenshot)

    # 디바이스 사이즈 기준으로 resize해서 저장
    image = cv2.imread(f'{os.getcwd()}/image/screenshot.png')
    image = cv2.resize(image, (device_size['width'], device_size['height']))
    cv2.imwrite(directory + screenshot, image)


def screenshot_keypad(wd):
    num = 0
    # 패스워드 입력 키패드의 index가 5부터 존재
    for i in range(5, 15):
        number = ial(wd, f'(//XCUIElementTypeImage[@name="키패드"])[{i}]')
        size = number.size
        number.screenshot(f'{os.getcwd()}/image/{num}.png')

        # 디바이스 사이즈 기준으로 resize 및 밝기 조절해서 저장
        image = cv2.imread(f'{os.getcwd()}/image/{num}.png')
        image = cv2.resize(image, (size['width'], size['height']))

        brightness_factor = 1.5
        image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)
        cv2.imwrite(f'{os.getcwd()}/image/{num}.png', image)

        num += 1


# 저장된 이미지에서 텍스트 추출
def return_keypad_text(num):
    image = cv2.imread(f'{os.getcwd()}/image/{num}.png')
    image = cv2.resize(image, (image.shape[1] * 2, image.shape[0] * 2), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    text = ''
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = image[y:y + h, x:x + w]

        text = pytesseract.image_to_string(roi, config='--psm 6 --oem 3')
        text = text.replace('\n', '')
    return text


# 전체 스크린샷과 키패드 스크린샷 비교하여 매핑
def password_mapping(wd, pw, i):
    # 저장한 이미지 흑백으로 불러 들이기
    image = cv2.imread(f'{os.getcwd()}/image/screenshot.png', 0)

    # 찾고자 하는 이미지 흑백으로 불러 들이기
    keypad = cv2.imread(f'{os.getcwd()}/image/{pw}.png', 0)

    # 찾는 이미지의 사이즈 저장하기
    w, h = keypad.shape[::-1]

    # opencv에서 이미지 매칭
    method = eval('cv2.TM_CCOEFF_NORMED')
    res = cv2.matchTemplate(image, keypad, method)

    # max_loc : 찾으려는 이미지의 왼쪽 위 모서리 좌표와 오른쪽 아래 모서리 좌표를 확인
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    center = (max_loc[0] + int(w / 2), max_loc[1] + int(h / 2))

    # 찾은 버튼 위치의 중앙 선택
    wd.tap([center])
    print(f"{i}번째 비밀번호 선택")
    sleep(1)


def click_credit_password(self, wd, i=1):
    password = self.pconf['credit_pw']
    for pw in password:
        for num in range(0, 10):
            text = return_keypad_text(num)
            if text == pw:
                password_mapping(wd, num, i)
                i += 1
                break
