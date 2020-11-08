import os
from flask import request
import json

from flask_restful import Resource, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    TextSendMessage, ImageSendMessage, VideoSendMessage, TextMessage, MessageEvent, JoinEvent, LeaveEvent
)
from linebot.models.events import UnsendEvent, VideoPlayCompleteEvent

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


class LineGroupController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        body = request.get_data(as_text=True)
        signature = request.headers['X-Line-Signature']
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        return 'OK'

    @handler.add(VideoPlayCompleteEvent)
    def handle_follow(event):
        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

        line_bot_api.reply_message(
            event.reply_token,
            messages=[TextSendMessage(text='喔齁齁齁看完了喔波波波')]
        )

    @handler.add(UnsendEvent)
    def unsend_event(event):
        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        line_type = event.source.type
        group, room, user = None, None, None
        if line_type == 'group':
            group = event.source.group_id
        elif line_type == 'room':
            room = event.source.room_id
        user = event.source.user_id

        profile = line_bot_api.get_profile(user_id=user)
        msg = f'{profile.display_name} 剛剛偷收回訊息！(抓)'
        line_bot_api.push_message(to=group or room, messages=[TextSendMessage(text=msg)])
        return 'OK'

    @handler.add(JoinEvent)
    def join_event(event):
        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        token = event.reply_token

        line_bot_api.reply_message(token, TextSendMessage(text='偶來囉～～！'))
        return 'OK'

    @handler.add(MessageEvent or LeaveEvent, message=TextMessage)
    def message_event(event):
        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

        line_type = event.source.type
        group, room, user = None, None, None
        if line_type == 'group':
            group = event.source.group_id
        elif line_type == 'room':
            room = event.source.room_id
        user = event.source.user_id

        token = event.reply_token
        message = event.message.text

        if message == '你走吧':
            msg = '走了88'
            if group:
                line_bot_api.reply_message(token, TextSendMessage(text=msg))
                line_bot_api.leave_group(group_id=group)
            elif room:
                line_bot_api.reply_message(token, TextSendMessage(text=msg))
                line_bot_api.leave_room(room_id=room)
            else:
                msg = '為什麼不是你走？'
                line_bot_api.reply_message(token, TextSendMessage(text=msg))
        elif group:
            if message == '群組資訊':
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
            elif message == '我是誰':
                profile = line_bot_api.get_group_member_profile(group_id=group, user_id=user)
                text = f'你是➡️ {profile.display_name}\nID➡️ {profile.user_id}'
                line_bot_api.reply_message(
                    token, messages=[
                        TextSendMessage(text=text),
                        ImageSendMessage(
                            original_content_url=profile.picture_url,
                            preview_image_url=profile.picture_url,
                        )]
                )
            elif message == 'v1':
                result = line_bot_api.set_webhook_endpoint(
                    webhook_endpoint=f"{os.getenv('MY_DOMAIN')}/v1/webhooks/line"
                )
                if result == {}:
                    message = '降版！'
            else:
                message = '請邀請我進群組喔\n指令為: \n1. 我是誰\n2.群組資訊\n3. 你走吧\n3. 輸入 v1 降版'

        elif room:
            if message == '聊天室資訊':
                count = line_bot_api.get_room_members_count(room_id=room)
                text = f'聊天室人數為: {count}'
                line_bot_api.reply_message(token, TextSendMessage(text=text))
            elif message == '我是誰':
                profile = line_bot_api.get_room_member_profile(room_id=room, user_id=user)
                text = f'你是➡️ {profile.display_name}\nID➡️ {profile.user_id}'
                line_bot_api.reply_message(
                    token, messages=[
                        TextSendMessage(text=text),
                        ImageSendMessage(
                            original_content_url=profile.picture_url,
                            preview_image_url=profile.picture_url,
                        )]
                )
            elif message == 'v1':
                result = line_bot_api.set_webhook_endpoint(
                    webhook_endpoint=f"{os.getenv('MY_DOMAIN')}/v1/webhooks/line"
                )
                if result == {}:
                    message = '降版！'
            else:
                message = '請邀請我進群組喔\n指令為: \n1. 我是誰\n2.群組資訊\n3. 你走吧\n3. 輸入 v1 降版'
        else:
            if message == 'video':
                line_bot_api.reply_message(
                    token,
                    messages=VideoSendMessage(
                        original_content_url='https://i.imgur.com/BhBshUO.mp4',
                        preview_image_url='https://i.imgur.com/MW0Mpb6.jpg',
                        tracking_id='duck')
                )
            else:
                message = '請邀請我進群組喔\n指令為: \n1. 我是誰\n2.群組資訊\n3. 你走吧\n3. 輸入 v1 降版'
        line_bot_api.reply_message(token, TextSendMessage(text=message))

        response = {
            "statusCode": 200,
            "body": json.dumps({"message": 'ok'})
        }

        return response
