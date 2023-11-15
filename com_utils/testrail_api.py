import requests
import json

from datetime import datetime

def create_plan(self):
    url = f"{self.econf['tr_host']}/index.php?/api/v2/add_plan/21"

    now = datetime.now()
    str_datetime = "[%04d-%02d-%02d %02d:%02d]" % (now.year, now.month, now.day, now.hour, now.minute)
    payload = json.dumps({
        "name": f"{str_datetime} Test Automation",
        "entries": [
            {
                "suite_id": 138,
                "name": "iOS Automation",
                "include_all": True,
                "case_ids": self.econf['tr_tc_ids']
            },
            {
                "suite_id": 138,
                "name": "Android Automation",
                "include_all": True,
                "case_ids": self.econf['tr_tc_ids']
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': self.econf['tr_auth'],
        'Cookie': self.econf['tr_cookie']
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def get_tests(self, os):
    url = f"{self.econf['tr_host']}/index.php?/api/v2/get_tests/{self.testcase_data['entries'][os]['runs'][0]['id']}"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': self.econf['tr_auth'],
        'Cookie': self.econf['tr_cookie']
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def send_test_result(self, os, test_result, case_name):
    url = f"{self.econf['tr_host']}/index.php?/api/v2/add_results_for_cases/{self.testcase_data['entries'][os]['runs'][0]['id']}"

    result = 1 if test_result == 'pass' else 5
    all_cases = self.ios_testcases if os == 0 else self.android_testcases

    payload = json.dumps({
        "results": [
            {
                "case_id": search_test(all_cases, case_name),
                "status_id": result,
                "comment": f"This test {test_result}",
                "defects": ""
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': self.econf['tr_auth'],
        'Cookie': self.econf['tr_cookie']
    }

    response = requests.request("POST", url, headers=headers, data=payload)


def search_test(tr_testcases, run_case):
    for i in range(len(tr_testcases)):
        if tr_testcases['tests'][i]['title'] == run_case:
            case_id = tr_testcases['tests'][i]['case_id']
            break
        else:
            case_id = None
    return case_id

def close_plan(self):
    url = f"{self.econf['tr_host']}/index.php?/api/v2/close_plan/{self.testcase_data['id']}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': self.econf['tr_auth'],
        'Cookie': self.econf['tr_cookie']
    }

    response = requests.request("POST", url, headers=headers)


