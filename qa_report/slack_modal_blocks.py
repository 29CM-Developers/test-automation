def block(feature_name):
    block = [
        {
            "type": "input",
            "block_id": "feature_name",
            "element": {
                "type": "plain_text_input",
                "action_id": "feature_name",
                "initial_value": f"{feature_name}"
            },
            "label": {
                "type": "plain_text",
                "text": "진행 중인 Feature명"
            }
        },
        {
            "type": "input",
            "block_id": "mention_user",
            "optional": True,
            "element": {
                "type": "multi_users_select",
                "action_id": "mention_user",
                "placeholder": {
                    "type": "plain_text",
                    "text": "멘션을 걸 팀원을 선택해 주세요.",
                    "emoji": True
                }
            },
            "label": {
                "type": "plain_text",
                "text": "멘션 팀원 선택",
                "emoji": True
            }
        },
        {
            "type": "input",
            "element": {
                "type": "radio_buttons",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Testrail"
                        },
                        "value": "testrail"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Manual"
                        },
                        "value": "manual"
                    }
                ],
                "action_id": "testcase"
            },
            "label": {
                "type": "plain_text",
                "text": "테스트케이스 진행 방식을 선택해주세요."
            }
        },
        {
            "type": "input",
            "block_id": "test_rate",
            "element": {
                "type": "number_input",
                "is_decimal_allowed": False,
                "action_id": "testrail_no",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Testrail로 테스트 중이면 Plan No, Manual로 테스트 중이면 진행률 작성"
                }
            },
            "label": {
                "type": "plain_text",
                "text": "테스트 진행률"
            }
        },
        {
            "type": "input",
            "block_id": "significant",
            "optional": True,
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                "action_id": "significant",
                "placeholder": {
                    "type": "plain_text",
                    "text": "특이사항을 작성해 주세요."
                }
            },
            "label": {
                "type": "plain_text",
                "text": "특이사항",
                "emoji": True
            }
        },
        {
            "type": "input",
            "block_id": "dashboard",
            "optional": True,
            "element": {
                "type": "url_text_input",
                "action_id": "dashboard"
            },
            "label": {
                "type": "plain_text",
                "text": "이슈 대시보드 링크",
                "emoji": True
            }
        }
    ]

    return block


def modal_block(ack, body, client, feature_name):
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": 'modal-id',
            'title': {
                'type': 'plain_text',
                'text': 'Daily Report 작성'
            },
            'blocks': block(feature_name),
            'submit': {
                'type': 'plain_text',
                'text': '확인'
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel"
            }
        }
    )


def update_modal_block(ack, body, client, feature_name):
    client.views_update(
        view_id=body["view"]["id"],
        hash=body["view"]["hash"],
        view={
            "type": "modal",
            "callback_id": 'modal-id',
            'title': {
                'type': 'plain_text',
                'text': 'Daily Report 작성'
            },
            'blocks': block(feature_name),
            'submit': {
                'type': 'plain_text',
                'text': '확인'
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel"
            }
        }
    )


def feature_check_modal(client, body, feature_name):
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": 'feature_check',
            'title': {
                'type': 'plain_text',
                'text': 'Daily Report 작성'
            },
            'blocks': [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"검색 결과가 없습니다. \n입력한 카테고리명이 '{feature_name}'이/가 맞습니까?",
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "입력한 카테고리명이 맞다면 아래 버튼을 눌러주시고, \n아니라면 모달을 닫은 뒤 다시 입력해 주세요.",
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": f'{feature_name} 확인',
                            },
                            "value": "feature_check",
                            "action_id": "feature_check"
                        }
                    ]
                }
            ]
        }
    )


def error_modal(client, body):
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": 'modal-id',
            'title': {
                'type': 'plain_text',
                'text': 'Daily Report 작성'
            },
            'blocks': [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Command와 카테고리명을 함께 입력해주세요",
                        "emoji": True
                    }
                }
            ]
        }
    )
