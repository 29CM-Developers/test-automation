import requests
from requests.auth import HTTPBasicAuth

jira_token = requests.get(f"http://192.168.103.13:50/qa/personal/dajjeong").json()
id = jira_token['jira_token']['id']
password = jira_token['jira_token']['password']


def jira_total_priority_issue(category, priority):
    url = 'https://jira.musinsa.com/rest/api/2/search'
    auth = HTTPBasicAuth(id, password)
    headers = {"Accept": "application/json"}
    query = {
        'jql': f'project = CMQA AND status in (할일, "이슈 확인중", 수정완료, Re-Open) '
               f'AND cf[11709] in ({category}) AND priority in ({priority})'
    }
    response = requests.get(
        url,
        headers=headers,
        params=query,
        auth=auth
    )
    total_data = response.json()
    issue_total_count = total_data['total']
    return issue_total_count


def jira_today_priority_issue(category, priority):
    url = 'https://jira.musinsa.com/rest/api/2/search'
    auth = HTTPBasicAuth(id, password)
    headers = {"Accept": "application/json"}
    query = {
        'jql': f'project = CMQA AND status in (할일, Done, "이슈 확인중", 수정완료, Re-Open) '
               f'AND cf[11709] in ({category}) AND priority in ({priority}) '
               f'AND createdDate > startOfDay()'
    }
    response = requests.get(
        url,
        headers=headers,
        params=query,
        auth=auth
    )
    today_data = response.json()
    issue_today_count = today_data['total']
    return issue_today_count
