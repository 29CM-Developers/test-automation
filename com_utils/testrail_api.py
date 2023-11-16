import requests
import json

from datetime import datetime

def create_plan(self, os_type, device, tc_list):
    url = f"{self.econf['tr_host']}/index.php?/api/v2/add_plan/21"

    now = datetime.now()
    str_datetime = "[%04d-%02d-%02d %02d:%02d]" % (now.year, now.month, now.day, now.hour, now.minute)
    payload = json.dumps({
        "name": f"{str_datetime} 29CM {os_type} Test Automation - {device}",
        "entries": [
            {
                "suite_id": 138,
                "name": f"{os_type} Device",
                "include_all": True,
                "case_ids": self.econf[f'{tc_list}']
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


def get_tests(self):
    url = f"{self.econf['tr_host']}/index.php?/api/v2/get_tests/{self.testcase_data['entries'][0]['runs'][0]['id']}"
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': self.econf['tr_auth'],
        'Cookie': self.econf['tr_cookie']
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def send_test_result(self, test_result, case_name):
    url = f"{self.econf['tr_host']}/index.php?/api/v2/add_results_for_cases/{self.testcase_data['entries'][0]['runs'][0]['id']}"
    result = 1 if test_result == 'PASS' else 5
    payload = json.dumps({
        "results": [
            {
                "case_id": search_test(self.testcases, case_name),
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
    for i in range(len(tr_testcases['tests'])):
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


