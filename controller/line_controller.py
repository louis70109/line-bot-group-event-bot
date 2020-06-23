import os
from flask import request
import json

from flask_restful import Resource
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage, ImageSendMessage
)


class LineGroupController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        payload = request.get_json(force=True)

        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
        event = payload['events'][0]
        token = event['replyToken']
        message = event['message']['text']
        line_type = event['source'].get('type')
        group = event['source'].get('groupId')
        room = event['source'].get('roomId')

        if line_type == 'group' and message == '群組資訊':
            count = line_bot_api.get_group_members_count(group_id=group)
            summary = line_bot_api.get_group_summary(group_id=group)
            text = f'群組名稱➡️ {summary.group_name}\n當前群組人數為➡️ {count}'
            line_bot_api.reply_message(
                token, messages=[
                    TextSendMessage(text=text),
                    ImageSendMessage(
                        original_content_url=summary.picture_url,
                        preview_image_url=summary.picture_url,
                    )]
            )

        elif line_type == 'room' and message == '對話群資訊':
            count = line_bot_api.get_room_members_count(room_id=room)
            text = f'對話群組人數為: {count}'
            line_bot_api.reply_message(token, TextSendMessage(text=text))

        else:
            line_bot_api.reply_message(token, TextSendMessage(text=message))

        response = {
            "statusCode": 200,
            "body": json.dumps({"message": 'ok'})
        }

        return response
