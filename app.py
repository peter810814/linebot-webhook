from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
import os

app = Flask(__name__)

# 從環境變數讀取 Channel token 和 secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("❌ 請確認環境變數 LINE_CHANNEL_ACCESS_TOKEN 和 LINE_CHANNEL_SECRET 都已設定")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/line/webhook", methods=['POST'])
def callback():
    print("📡 收到 LINE webhook 請求")  # 確認 webhook 有進來
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 簽章驗證失敗")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("🧪 有進來 webhook！")
    print("📨 來源類型：", event.source.type)

    if event.source.type == 'group':
        print("✅ 接收到群組訊息")
        print("🔍 群組 ID:", event.source.group_id)
    elif event.source.type == 'user':
        print("✅ 接收到個人訊息")
        print("🔍 userId:", event.source.user_id)

    # 回覆收到的訊息（可選）
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=f"你說的是：「{event.message.text}」")
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
