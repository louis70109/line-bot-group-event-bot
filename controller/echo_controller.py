import os
from flask import request

from flask_restful import Resource, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    TextSendMessage, TextMessage, MessageEvent
)

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


class EchoController(Resource):

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

    @handler.add(MessageEvent, message=TextMessage)
    def message_event(event):
        line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
        message = event.message.text
        if message == 'v2':
            result = line_bot_api.set_webhook_endpoint(webhook_endpoint=f"{os.getenv('MY_DOMAIN')}/v2/webhooks/line")
            if result == {}:
                message = '升版！'
        else:
            message = f"輸入的訊息：{message}\n\n*輸入: v2 升版"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

        return 'OK'
