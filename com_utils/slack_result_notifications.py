import re
from datetime import datetime
import requests
import json


def slack_notification(self):
    headers = slack_headers_form(self.conf["slack_token"])
    if self.result_data['test_result'] == 'PASS':
        color = self.conf['pass_color']
        emoji = self.conf['pass_emoji']
    elif self.result_data['test_result'] == 'WARN':
        color = self.conf['warn_color']
        emoji = self.conf['warn_emoji']
    else:
        color = self.conf['fail_color']
        emoji = self.conf['fail_emoji']

    if self.device_platform == 'iOS':
        device_emoji = ':ios:'
    elif self.device_platform == 'Android':
        device_emoji = ':android:'
    else: device_emoji = self.device_platform

    device_name = self.device_name
    digit = re.sub(r'[^0-9]', '', device_name)
    text = list(filter(str.isalpha, device_name))
    text = ''.join(text)
    device_name = f'{text} {digit}'

    # slack noti 양식 가져오기
    attachment = slack_noti_form(channel=self.conf['slack_channel'], color=color, emoji=emoji,
                                 test_result=self.result_data.get('test_result'), def_name=self.def_name,
                                 count='-', total_time='-', device_platform=device_emoji, device_name=device_name)

    payload = json.dumps(attachment)
    response = requests.post(url=self.conf['slack_message_url'], headers=headers, data=payload)

    return response.json()


def slack_update_notification(self):
    try:
        total_time = float(self.total_time)
    except ValueError:
        total_time = 0.00
    total_time += float(self.result_data.get('run_time'))

    headers = slack_headers_form(self.conf["slack_token"])
    if self.result_data['test_result'] == 'PASS':
        if self.slack_result == 'FAIL':
            test_result = 'FAIL'
            color = self.conf['fail_color']
            emoji = self.conf['fail_emoji']
        elif self.slack_result == 'WARN':
            test_result = 'WARN'
            color = self.conf['warn_color']
            emoji = self.conf['warn_emoji']
        else:
            test_result = 'PASS'
            color = self.conf['pass_color']
            emoji = self.conf['pass_emoji']
    elif self.result_data['test_result'] == 'WARN':
        if self.slack_result == 'FAIL':
            test_result = 'FAIL'
            color = self.conf['fail_color']
            emoji = self.conf['fail_emoji']
        else:
            test_result = 'WARN'
            color = self.conf['warn_color']
            emoji = self.conf['warn_emoji']
            self.slack_result = self.result_data.get('test_result')
    else:
        color = self.conf['fail_color']
        emoji = self.conf['fail_emoji']
        self.slack_result = self.result_data.get('test_result')

    if self.slack_result == 'FAIL':
        test_result = 'FAIL'
        color = self.conf['fail_color']
        emoji = self.conf['fail_emoji']
    else:
        pass

    if self.device_platform == 'iOS':
        device_emoji = ':ios:'
    elif self.device_platform == 'Android':
        device_emoji = ':android:'
    else:
        device_emoji = self.device_platform

    device_name = self.device_name
    digit = re.sub(r'[^0-9]', '', device_name)
    text = list(filter(str.isalpha, device_name))
    text = ''.join(text)
    device_name = f'{text} {digit}'
    minutes = total_time // 60
    seconds = total_time % 60
    if minutes > 0:
        str_total_time = f"{int(minutes)} 분 {seconds:.2f} 초"
    else:
        str_total_time = f"{total_time:.2f} 초"

    # slack noti 양식 가져오기
    attachment = slack_noti_form(channel=self.conf['slack_channel'], color=color, emoji=emoji,
                                 test_result=test_result, def_name=self.def_name,
                                 count=self.count, total_time=str_total_time,
                                 device_platform=device_emoji, device_name=device_name)

    attachment['ts'] = self.response['ts']
    payload = json.dumps(attachment)
    response = requests.post(url=self.conf['slack_update_message_url'], headers=headers, data=payload)
    return f"{total_time:.2f}", self.slack_result


def slack_thread_notification(self):
    headers = slack_headers_form(self.conf["slack_token"])
    self.count += 1
    # attachment 양식 가져오기
    attachment = slack_thread_form(self.conf['slack_channel'], self.response['ts'])

    if self.result_data['test_result'] == 'PASS':
        color = self.conf['pass_color']
        attachment["attachments"][0]["color"] = color
        attachment["attachments"][0]["blocks"][0]["text"]["text"] = f"성공 쓰레드 테스트: *{self.result_data.get('test_name')}*"
        attachment["attachments"][0]["blocks"][1]["text"]["text"] = f"테스트 시간: *{self.result_data.get('start_time')}*"
        attachment["attachments"][0]["blocks"][2]["text"]["text"] = f"테스트 소요시간: *{self.result_data.get('run_time')} 초*"
        attachment = json.dumps(attachment)
        response = requests.post(url=self.conf['slack_message_url'], headers=headers, data=attachment)
    elif self.result_data['test_result'] == 'WARN':
        color = self.conf['warn_color']
        warn_attachment = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*추가 확인 필요*: \n{self.result_data.get('warning_texts')}"
            }
        }
        attachment["attachments"][0]["color"] = color
        attachment["attachments"][0]["blocks"][0]["text"]["text"] = f"성공 쓰레드 테스트: *{self.result_data.get('test_name')}*"
        attachment["attachments"][0]["blocks"][1]["text"]["text"] = f"테스트 시간: *{self.result_data.get('start_time')}*"
        attachment["attachments"][0]["blocks"][2]["text"]["text"] = f"테스트 소요시간: *{self.result_data.get('run_time')} 초*"
        attachment["attachments"][0]["blocks"].append(warn_attachment)
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
        attachment["attachments"][0]["blocks"][1]["text"]["text"] = f"테스트 시간: *{self.result_data.get('start_time')}*"
        attachment["attachments"][0]["blocks"][2]["text"]["text"] = f"테스트 소요시간: *{self.result_data.get('run_time')} 초*"
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

    return self.count


def slack_noti_form(channel, color, emoji, test_result, def_name, count, total_time, device_platform, device_name):
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
                            "text": f"테스트 디바이스: *{device_platform} {device_name}*"
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
                            "text": f"테스트 진행률: *{count} 개 / 총 {total_time}*"
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