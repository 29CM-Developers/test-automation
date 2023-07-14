import requests
import json


def slack_notification(self):
    headers = slack_headers_form(self.conf["slack_token"])
    if self.result_data['test_result'] == 'PASS':
        color = self.conf['pass_color']
        emoji = self.conf['pass_emoji']
    else:
        color = self.conf['fail_color']
        emoji = self.conf['fail_emoji']
    # slack noti 양식 가져오기
    attachment = slack_noti_form(self.conf['slack_channel'], color, emoji, self.result_data.get('test_result'), self.def_name)

    payload = json.dumps(attachment)
    response = requests.post(url=self.conf['slack_message_url'], headers=headers, data=payload)

    return response.json()


def slack_thread_notification(self):
    headers = slack_headers_form(self.conf["slack_token"])
    # attachment 양식 가져오기
    attachment = slack_thread_form(self.conf['slack_channel'], self.response['ts'])

    if self.result_data['test_result'] == 'PASS':
        color = self.conf['pass_color']
        attachment["attachments"][0]["color"] = color
        attachment["attachments"][0]["blocks"][0]["text"]["text"] = f"성공 쓰레드 테스트: *{self.result_data.get('test_name')}*"
        attachment["attachments"][0]["blocks"][1]["text"]["text"] = f"테스트 소요시간: *{self.result_data.get('run_time')} 초*"
        attachment = json.dumps(attachment)
        response = requests.post(url=self.conf['slack_message_url'], headers=headers, data=attachment)
    else:
        color = self.conf['fail_color']
        # 실패 내용 쓰레드
        code_attachment = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"error reason: *{self.result_data['error_texts'][1]}*"
            }
        }
        reason_attachment = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"error code: *{self.result_data['error_texts'][0]}*"
            }
        }
        attachment["attachments"][0]["color"] = color
        attachment["attachments"][0]["blocks"][0]["text"]["text"] = f"실패 쓰레드 테스트: *{self.result_data.get('test_name')}*"
        attachment["attachments"][0]["blocks"][1]["text"]["text"] = f"테스트 소요시간: *{self.result_data.get('run_time')} 초*"
        attachment["attachments"][0]["blocks"].append(code_attachment)
        attachment["attachments"][0]["blocks"].append(reason_attachment)
        attachment = json.dumps(attachment)
        response = requests.post(url=self.conf['slack_message_url'], headers=headers, data=attachment)
        # 이미지 업로드
        with open(self.result_data['img_src'], 'rb') as f:
            content = f.read()
        attachment = {"channels": self.conf['slack_channel'], "thread_ts": self.response['ts'], "title": 'pass result',
                      "content": content}
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'
        requests.post(url=self.conf['slack_file_upload_url'], headers=headers, data=attachment)
    return response.json()


def slack_noti_form(channel, color, emoji, test_result, def_name):
    attachment = {
        "channel": channel,
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"진행 테스트: *{def_name}*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"결과: *{emoji} {test_result}*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "테스트 진행률: *making now*"
                        }
                    }
                ]
            }
        ]
    }
    return attachment

def slack_thread_form(channel, ts):
    attachment = {
        "channel": channel,
        "thread_ts": ts,
        "attachments": [
            {
                "color": '',
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ""
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ""
                        }
                    }
                ]
            }
        ]
    }
    return attachment

def slack_headers_form(slack_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {slack_token}'
    }
    return headers