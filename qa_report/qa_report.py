import os
import ssl
import certifi
import slack_modal_blocks

from slack_bolt import App
from slack_sdk import WebClient
from slack_bolt.adapter.socket_mode import SocketModeHandler
from jira_issue import jira_today_priority_issue, jira_total_priority_issue
from testrail_test_result import plan_result

ssl._create_default_https_context = ssl._create_unverified_context
ssl_context = ssl.create_default_context(cafile=certifi.where())

SLACK_BOT_TOKEN = "xoxb-2161493444-5496041376176-zCb88TG1CWz9LlYCYZhPo6lj"
SLACK_APP_TOKEN = "xapp-1-A05DKES5728-6057216249874-e1908a745b084f96c0cdb58c9162827338172074017ca7354acfbd5cefe7b6a9"

slack_client = WebClient(token=SLACK_BOT_TOKEN, ssl=ssl_context)
app = App(client=slack_client)


@app.event("app_mention")
def bot_mention(event, client, message, say):
    print('event:', event)
    print('client:', client)
    print('message:', message)

    say(f'<@{event["user"]}>님, /report를 불러주세요.')


@app.command("/qa_report")
def slash_command(ack, command, body, client):
    ack()
    print(f'커맨드 : {command}')

    global channel_id
    channel_id = body['channel_id']

    global feature_name, today_issue_high_count, today_issue_mid_count, today_issue_low_count, today_total_count
    feature_name = body['text']
    print(feature_name)

    if feature_name != "":
        today_issue_high_count = jira_today_priority_issue(feature_name, '가장높음,높음')
        today_issue_mid_count = jira_today_priority_issue(feature_name, '중간')
        today_issue_low_count = jira_today_priority_issue(feature_name, '가장낮음,낮음')
        today_total_count = today_issue_high_count + today_issue_mid_count + today_issue_low_count
        if today_total_count == 0:
            open_check_feature_name(ack, client, body)
        else:
            open_modal(ack, body, client)
    else:
        open_error_modal(ack, client, body)


@app.shortcut('open_modal')
def open_check_feature_name(ack, client, body):
    ack()
    slack_modal_blocks.feature_check_modal(client, body, feature_name)


@app.shortcut("open_modal")
def open_error_modal(ack, client, body):
    ack()
    slack_modal_blocks.error_modal(client, body)


@app.shortcut("open_modal")
def open_modal(ack, body, client):
    ack()
    slack_modal_blocks.modal_block(ack, body, client, feature_name)


@app.action("feature_check")
def feature_check_open_modal(ack, body, client):
    ack()
    slack_modal_blocks.update_modal_block(ack, body, client, feature_name)


@app.view("modal-id")
def slack_message(ack, body, logger, client):
    ack()
    logger.info(body)

    input_data = body['view']['state']['values']
    print(f'확인 : {input_data}')
    data_key = []
    for k in input_data.keys():
        data_key.append(k)

    # 멘션 걸 유저 확인
    mention_users = input_data['mention_user']['mention_user']['selected_users']
    mention_user = [f'<@{user_id}>' for user_id in mention_users]
    mention_user = ', '.join(mention_user)

    # 테스트 진행 피쳐명
    feature_name = input_data['feature_name']['feature_name']['value']

    # 오늘 등록한 이슈
    if today_total_count == 0:
        today_issue = "• 금일 등록된 이슈는 없습니다."
    else:
        today_issue = f"• 금일 등록된 이슈는 *{today_total_count}건* (:priority_high:높음 이상: {today_issue_high_count}건, " \
                      f":priority_mid:중간: {today_issue_mid_count}건, :priority_low:낮음 이하: {today_issue_low_count}건)"

    # 잔여 이슈
    total_issue_high_count = jira_total_priority_issue(feature_name, '가장높음,높음')
    total_issue_mid_count = jira_total_priority_issue(feature_name, '중간')
    total_issue_low_count = jira_total_priority_issue(feature_name, '가장낮음,낮음')
    total_count = total_issue_high_count + total_issue_mid_count + total_issue_low_count

    # 테스트케이스 방식 선택
    testcase = input_data[data_key[2]]['testcase']['selected_option']['value']
    if testcase == 'testrail':
        testrail_no = input_data['test_rate']['testrail_no']['value']
        testrail = plan_result(testrail_no)
        test_rate = testrail['progress_rate']
        passed_rate = testrail['pass_rate']
        failed_rate = testrail['fail_rate']
        test_rate_text = f'• 진행률 : {test_rate}% (:green_check:Pass : {passed_rate}%, :red_check:Fail : {failed_rate}%)'
        image_url = os.path.dirname(os.path.realpath(__file__)) + '/chart.png'
    else:
        test_rate = input_data['test_rate']['testrail_no']['value']
        test_rate_text = f'• 진행률 : {test_rate}%'
        image_url = ""

    # 대시보드 링크 여부 확인
    try:
        dashboard_link = body['view']['state']['values']['dashboard']['dashboard']['value']
        dashboard = f"\n• <{dashboard_link}|이슈 대시보드를 참고해주세요.>"
    except:
        dashboard = ""

    # 특이사항 여부 확인
    significant_text = input_data['significant']['significant']['value']
    if significant_text is None:
        significant = ' '
    else:
        significant = f"*`특이사항`* \n{significant_text}"

    # 메시지 전송 Block
    attachments = [
        {
            "color": "#36C5F0",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*`Today`*\n"
                                f"{test_rate_text} \n"
                                f"{today_issue}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*`Total`*\n"
                                f"• 전체 이슈 중 완료되지 않은 이슈는 *{total_count}건* (:priority_high:높음 이상: {total_issue_high_count}건, "
                                f":priority_mid:중간: {total_issue_mid_count}건, :priority_low:낮음 이하: {total_issue_low_count}건)"
                                f"{dashboard}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{significant}"
                    }
                }
            ]
        }
    ]

    response = client.chat_postMessage(
        channel=channel_id,
        text=f"*[{feature_name}]* 테스트 진행상황 공유 {mention_user} cc.<!subteam^S058C8XCU7R>",
        attachments=attachments
    )

    if image_url == "":
        pass
    else:
        slack_thread(client, response['ts'], image_url)


def slack_thread(client, message_ts, image_url):
    response = client.files_upload_v2(
        channel=channel_id,
        file=image_url,
        thread_ts=message_ts
    )
    return response


@app.view_closed("modal-id")
def handle_view_closed(ack, body, logger):
    ack()
    logger.info(body)


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
