import requests
import matplotlib.pyplot as plt

from testrail import APIClient

client = APIClient("https://musinsa.testrail.io/")
testrail_token = requests.get(f"http://192.168.103.13:50/qa/personal/dajjeong").json()
client.user = testrail_token['testrail_token']['id']
client.password = testrail_token['testrail_token']['password']


def get_plan(plan_id):
    plan = client.send_get(f"get_plan/{plan_id}")
    return plan


def plan_result(plan_id):
    plan = get_plan(plan_id)
    passed_count = plan['passed_count']
    failed_count = plan['failed_count']
    untested_count = plan['untested_count']
    na_count = plan['custom_status2_count']
    inprogress_count = plan['custom_status4_count']
    fixed_count = plan['custom_status3_count']
    blocked_count = plan['blocked_count']
    change_failed_count = plan['custom_status5_count']
    script_failed_count = plan['custom_status1_count']
    retest_count = plan['retest_count']

    total_count = passed_count + untested_count + failed_count + na_count + fixed_count + inprogress_count \
                  + blocked_count + change_failed_count + script_failed_count + retest_count
    progress_count = total_count - untested_count - inprogress_count

    test_rate = {
        'progress_rate': round(progress_count / total_count * 100, 1),
        'pass_rate': round(passed_count / total_count * 100, 1),
        'fail_rate': round(failed_count / total_count * 100, 1),
        'na_rate': round(na_count / total_count * 100, 1)
    }

    labels = []
    count = []
    color = []
    explode = []

    if passed_count > 0:
        labels.append(f'Pass')
        count.append(passed_count)
        color.append('#2EB67D')
        explode.append(0.05)
    if failed_count > 0:
        labels.append(f'Fail')
        count.append(failed_count)
        color.append('#E01E5A')
        explode.append(0.05)
    if untested_count > 0:
        labels.append(f'Untest')
        count.append(untested_count)
        color.append('#CCCCCC')
        explode.append(0)
    if na_count > 0:
        labels.append(f'N/A')
        count.append(na_count)
        color.append('#E585CF')
        explode.append(0)
    if inprogress_count > 0:
        labels.append(f'In Progress')
        count.append(inprogress_count)
        color.append('#36C4F0')
        explode.append(0)
    if fixed_count > 0:
        labels.append('Fix')
        count.append(fixed_count)
        color.append('#A0AFFF')
        explode.append(0)
    if blocked_count > 0:
        labels.append('Block')
        count.append(blocked_count)
        color.append('#282828')
        explode.append(0)
    if change_failed_count > 0:
        labels.append('Change Fail')
        count.append(change_failed_count)
        color.append('#7F00FF')
        explode.append(0)
    if script_failed_count > 0:
        labels.append('Script Fail')
        count.append(script_failed_count)
        color.append('#C8C8FF')
        explode.append(0)
    if retest_count > 0:
        labels.append('Retest')
        count.append(retest_count)
        color.append('#FFDC3C')
        explode.append(0)

    plt.figure(figsize=(3.5, 2.5))
    plt.pie(count, labels=labels, autopct='%.1f%%', colors=color, explode=explode)
    plt.title(f'Total TestCase Count : {total_count}', fontsize=12)

    plt.savefig(f'chart.png')

    return test_rate
