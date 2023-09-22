import requests


def cookie_29cm(user_id, user_password):
    response = requests.post('https://apihub.29cm.co.kr/user/login/', data={
        "user_id": user_id,
        "user_password": user_password})
    return response.cookies
