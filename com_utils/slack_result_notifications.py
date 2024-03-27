import re
import datetime
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

    if self.device_platform == 'iOS':
        device_emoji = ':ios:'
    elif self.device_platform == 'Android':
        device_emoji = ':android:'
    else: device_emoji = self.device_platform

    # slack noti 양식 가져오기
    if self.device_platform == "iOS" and self.user == "pipeline":
        slack_channel = self.conf['ios_slack_channel']
    # Android는 알림 길이가 길어 기존 내용 파악에 영향을 줄 수 있어 알림 채널 변동은 하지 않도록 한다.
    # elif self.device_platform == "Android" and self.user == "pipeline":
    #     slack_channel = self.conf['android_slack_channel']
    else:
        slack_channel = self.conf['slack_channel']
    attachment = slack_noti_form(channel=slack_channel, color=color, emoji=emoji,
                                 test_result=self.result_data.get('test_result'), def_name=self.def_name,
                                 count='-', total_time='-', device_platform=device_emoji, device_name=self.device_name)

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
        else:
            test_result = 'PASS'
            color = self.conf['pass_color']
            emoji = self.conf['pass_emoji']
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

    minutes = total_time // 60
    seconds = total_time % 60
    if minutes > 0:
        str_total_time = f"{int(minutes)} 분 {seconds:.2f} 초"
    else:
        str_total_time = f"{total_time:.2f} 초"

    self.result_lists.append(self.result_data['test_result'])
    pass_count = self.result_lists.count("PASS")
    fail_count = self.result_lists.count("FAIL")

    if self.result_data['test_result'] in {'PASS', 'FAIL'}:
        # slack noti 양식 가져오기
        if self.device_platform == "iOS" and self.user == "pipeline":
            slack_channel = self.conf['ios_slack_channel']
        # Android는 알림 길이가 길어 기존 내용 파악에 영향을 줄 수 있어 알림 채널 변동은 하지 않도록 한다.
        # elif self.device_platform == "Android" and self.user == "pipeline":
        #     slack_channel = self.conf['android_slack_channel']
        else:
            slack_channel = self.conf['slack_channel']
        attachment = slack_noti_form(channel=slack_channel, color=color, emoji=emoji,
                                     test_result=test_result, def_name=self.def_name,
                                     count=self.count, total_time=str_total_time,
                                     device_platform=device_emoji, device_name=self.device_name, pass_count=pass_count,
                                     fail_count=fail_count)

        attachment['ts'] = self.response['ts']
        payload = json.dumps(attachment)
        response = requests.post(url=self.conf['slack_update_message_url'], headers=headers, data=payload)
    return f"{total_time:.2f}", self.slack_result


def slack_thread_notification(self):
    headers = slack_headers_form(self.conf["slack_token"])
    self.count += 1
    # attachment 양식 가져오기
    if self.device_platform == "iOS" and self.user == "pipeline":
        slack_channel = self.conf['ios_slack_channel']
    # Android는 알림 길이가 길어 기존 내용 파악에 영향을 줄 수 있어 알림 채널 변동은 하지 않도록 한다.
    # elif self.device_platform == "Android" and self.user == "pipeline":
    #     slack_channel = self.conf['android_slack_channel']
    else:
        slack_channel = self.conf['slack_channel']

    attachment = slack_thread_form(slack_channel, self.response['ts'])

    if self.result_data['test_result'] == 'PASS':
        color = self.conf['pass_color']
        attachment["attachments"][0]["color"] = color
        attachment["attachments"][0]["blocks"][0]["text"]["text"] = f"성공 쓰레드 테스트: *{self.result_data.get('test_name')}*"
        attachment["attachments"][0]["blocks"][1]["text"]["text"] = f"테스트 소요시간: *{self.result_data.get('run_time')} 초*"
        attachment = json.dumps(attachment)
        response = requests.post(url=self.conf['slack_message_url'], headers=headers, data=attachment)
    else:
        try:
            color = self.conf['fail_color']
            # 실패 내용 쓰레드
            attachment["attachments"][0]["color"] = color
            attachment["attachments"][0]["blocks"][0]["text"][
                "text"] = f"실패 쓰레드 테스트: *{self.result_data.get('test_name')}*"
            attachment["attachments"][0]["blocks"][1]["text"][
                "text"] = f"테스트 소요시간: *{self.result_data.get('run_time')} 초*"

            error_texts = self.result_data.get('error_texts', [])
            error_code = error_texts[0]
            if len(error_texts) > 1 and error_texts[1] is not None:
                index = 1
            else:
                index = 2
            error_reason = error_texts[index] if index > 0 else None

            code_attachment = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"error code: *{error_code}*"
                }
            }

            reason_attachment = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"error reason: *{error_reason}*"
                }
            }

            attachment["attachments"][0]["blocks"].append(reason_attachment)
            attachment["attachments"][0]["blocks"].append(code_attachment)
            attachment = json.dumps(attachment)
            response = requests.post(url=self.conf['slack_message_url'], headers=headers, data=attachment)

            # 현재 날짜와 시간을 가져오기
            current_datetime = datetime.datetime.now()
            # 날짜와 시간을 원하는 형식으로 문자열로 변환
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            # 이미지 업로드
            try:
                with open(self.result_data['img_src'], 'rb') as f:
                    content = f.read()
            except FileNotFoundError:
                content = None
            if content is not None:

                attachment = {"channels": slack_channel, "thread_ts": self.response['ts'],
                              "title": formatted_datetime, "content": content}
                headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'
                requests.post(url=self.conf['slack_file_upload_url'], headers=headers, data=attachment)
        except IndexError:
            self.result_data['test_result'] = 'None'
            self.count -= 1

    return self.count


def slack_add_end_emoji(self):
    if self.device_platform == "iOS" and self.user == "pipeline":
        slack_channel = self.conf['ios_slack_channel']
    # Android는 알림 길이가 길어 기존 내용 파악에 영향을 줄 수 있어 알림 채널 변동은 하지 않도록 한다.
    # elif self.device_platform == "Android" and self.user == "pipeline":
    #     slack_channel = self.conf['android_slack_channel']
    else:
        slack_channel = self.conf['slack_channel']
    attachment = {"channel": slack_channel, "thread_ts": self.response['ts'],
                  "name": self.conf["done_emoji"], "timestamp": self.response['ts']}
    headers = slack_headers_form(self.conf["slack_token"])
    headers['Content-Type'] = 'application/x-www-form-urlencoded;'
    response = requests.post(url=self.conf["slack_add_reaction_url"], headers=headers, data=attachment)


def slack_noti_form(channel, color, emoji, test_result, def_name, count, total_time, device_platform, device_name,
                    pass_count=0, fail_count=0):
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
                            "text": f"테스트 진행률: *총 {count} 개 / PASS {pass_count} 개 - FAIL {fail_count} 개 / 총 {total_time}*"
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