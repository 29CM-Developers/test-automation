from locust import HttpUser, between, task
import random


class UserBehavior(HttpUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_start(self):
        print('Now Shooting API')
        # 60초 후 100 유저 증가
        # self.user.wait_and_increase_users(60, 100)

    @task(1)
    def index(self):
        # self.headers = {'Cookie': "_frtn_qa={}"
        #                           "_fatn_qa={}"}
        self.headers = {'Authorization': "Bearer {}"}

        # endpoint 만 작성해주세요. base url은 locust 웹 창에서 입력합니다.
        self.url = '/inhouse-admin/v4/items/50'
        self.client.get(url=self.url, headers=self.headers)

    '''일정 시간(wait_time) 이후에 일정 유저 수(user_count) 증가'''
    def wait_and_increase_users(self, wait_time, user_count):
        self.environment.runner.user_count = user_count
        self.environment.runner.spawn_missing_workers()
        self.wait_time = between(wait_time, wait_time)
        self.wait()