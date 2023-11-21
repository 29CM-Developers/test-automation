import requests
from requests.auth import HTTPBasicAuth

jira_token = requests.get(f"http://192.168.103.13:50/qa/personal/dajjeong").json()
id = jira_token['jira_token']['id']
password = jira_token['jira_token']['password']


def jira_total_issue(category):
    url = 'https://jira.musinsa.com/rest/api/2/search'
    auth = HTTPBasicAuth(id, password)
    headers = {"Accept": "application/json"}
    query = {
        'jql': f'project = CMQA AND status in (할일, "이슈 확인중", 수정완료, Re-Open) '
               f'AND cf[11709] in ({category})'
    }
    response = requests.get(
        url,
        headers=headers,
        params=query,
        auth=auth
    )
    total_data = response.json()
    total_count = total_data['total']
    high = 0
    mid = 0
    low = 0
    issue_total_count = {}
    for i in range(0, total_count):
        issue_priority = total_data['issues'][i]['fields']['priority']['id']
        if issue_priority == '1' or issue_priority == '2':
            high = high + 1
        elif issue_priority == '3':
            mid = mid + 1
        elif issue_priority == '4' or issue_priority == '5':
            low = low + 1
    issue_total_count['total'] = total_count
    issue_total_count['high'] = high
    issue_total_count['mid'] = mid
    issue_total_count['low'] = low
    return issue_total_count


def jira_today_issue(category):
    url = 'https://jira.musinsa.com/rest/api/2/search'
    auth = HTTPBasicAuth(id, password)
    headers = {"Accept": "application/json"}
    query = {
        'jql': f'project = CMQA AND status in (할일, Done, "이슈 확인중", 수정완료, Re-Open) '
               f'AND cf[11709] in ({category}) '
               f'AND createdDate > startOfDay()'
    }
    response = requests.get(
        url,
        headers=headers,
        params=query,
        auth=auth
    )

    today_data = response.json()
    today_count = today_data['total']
    high = 0
    mid = 0
    low = 0
    issue_today_count = {}
    for i in range(0, today_count):
        issue_priority = today_data['issues'][i]['fields']['priority']['id']
        if issue_priority == '1' or issue_priority == '2':
            high = high + 1
        elif issue_priority == '3':
            mid = mid + 1
        elif issue_priority == '4' or issue_priority == '5':
            low = low + 1
    issue_today_count['total'] = today_count
    issue_today_count['high'] = high
    issue_today_count['mid'] = mid
    issue_today_count['low'] = low
    return issue_today_count
