from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

import os

app = Flask(__name__)

# 用你自己的 token 與 secret 替換
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")



line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/line/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'




@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("🧪 有進來 webhook！")  # 這行是新增的

    if event.source.type == 'group':
        print("✅ 接收到群組訊息！")
        print("🔍 群組 ID:", event.source.group_id)
    elif event.source.type == 'user':
        print("✅ 接收到個人訊息")
        print("🔍 userId:", event.source.user_id)
