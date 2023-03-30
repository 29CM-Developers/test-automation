from locust import HttpUser, between, task
import random


class UserBehavior(HttpUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_start(self):
        print('Now Shooting API')

    @task(1)
    def index(self):
        # self.headers = {'Cookie': "_frtn_qa=eyJ2ZXIiOiJWMSIsImFsZyI6IkVTMjU2In0.eyJqdGkiOiJhMTg5ZDQ1Mi1lZjcwLTQ4NTgtOTA2NC1kNzI4YzQyYTk1ZTYiLCJpc3MiOiIyOWNtLWF1dGhlbnRpY2F0aW9uIiwic3ViIjoiMjljbS1SRUZSRVNILVRPS0VOIiwiYXVkIjoic2VsbGVyIiwibmJmIjoxNjc5ODc3MjM2LCJpYXQiOjE2Nzk4NzcyMzYsImV4cCI6MTY3OTg5NTIzNn0.K4aHoHgPoXqhPOUYP78cOJcfEw-qouvL3n8pPz6dVG-cNOjkThZ9UqAGE2QAUNsSvoNSbvUT30v0dlk31MKBkw;"
        #                           "_fatn_qa=eyJ2ZXIiOiJWMSIsImFsZyI6IkVTMjU2In0.eyJqdGkiOiI3OTU3ZDVjZi05OTk4LTQ5MWItOWEzZS1hNmE4MTMwMGRkMjgiLCJpc3MiOiIyOWNtLWF1dGhlbnRpY2F0aW9uIiwic3ViIjoiMjljbS1BQ0NFU1MtVE9LRU4iLCJhdWQiOiJzZWxsZXIiLCJuYmYiOjE2Nzk4NzcyMzYsImlhdCI6MTY3OTg3NzIzNiwiZXhwIjoxNjc5ODkxNjM2LCJ1c2VySW5mbyI6eyJ1c2VyQWx0S2V5IjoiYWU4ZTA3NmEtNzZlOS00NjVjLTk5MzgtM2E0NzFmY2U0YTliIiwibG9naW5JZCI6Im1wYXJrX3BhcnRuZXIxIiwiYWRtaW5JZCI6MjY4NCwicGFydG5lcklkIjoxMDExOCwiZW1haWxWZXJpZmllZCI6ZmFsc2UsInJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwicGFydG5lciIsInVtYV9hdXRob3JpemF0aW9uIl19fQ.u51nJUTKM48ebi06v9ImCReXK_qn8VuedCAwUuFd-ia5yWfGjOjAz6JCKlQrEEIfco8025pCHI6q6HOpgrwdhw;"}
        self.headers = {'Authorization': "Bearer eyJ2ZXIiOiJWMSIsImFsZyI6IkVTMjU2In0.eyJqdGkiOiI3OTU3ZDVjZi05OTk4LTQ5MWItOWEzZS1hNmE4MTMwMGRkMjgiLCJpc3MiOiIyOWNtLWF1dGhlbnRpY2F0aW9uIiwic3ViIjoiMjljbS1BQ0NFU1MtVE9LRU4iLCJhdWQiOiJzZWxsZXIiLCJuYmYiOjE2Nzk4NzcyMzYsImlhdCI6MTY3OTg3NzIzNiwiZXhwIjoxNjc5ODkxNjM2LCJ1c2VySW5mbyI6eyJ1c2VyQWx0S2V5IjoiYWU4ZTA3NmEtNzZlOS00NjVjLTk5MzgtM2E0NzFmY2U0YTliIiwibG9naW5JZCI6Im1wYXJrX3BhcnRuZXIxIiwiYWRtaW5JZCI6MjY4NCwicGFydG5lcklkIjoxMDExOCwiZW1haWxWZXJpZmllZCI6ZmFsc2UsInJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwicGFydG5lciIsInVtYV9hdXRob3JpemF0aW9uIl19fQ.u51nJUTKM48ebi06v9ImCReXK_qn8VuedCAwUuFd-ia5yWfGjOjAz6JCKlQrEEIfco8025pCHI6q6HOpgrwdhw"}
        # endpoint 만 작성해주세요. base url은 locust 웹 창에서 입력합니다.
        self.url = '/inhouse-admin/v4/items/50'
        self.client.get(url=self.url, headers=self.headers)