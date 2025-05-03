from flask import Flask, request, abort
import os
import json
import sys
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

# 強制即時輸出 print()
sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)

# 從環境變數讀取 token 與 secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("❌ 環境變數未正確設定")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/line/webhook", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    print("📦 收到 webhook：", flush=True)
    try:
        payload = json.loads(body)
        print(json.dumps(payload, indent=2, ensure_ascii=False), flush=True)
    except Exception as e:
        print(f"❌ JSON 解碼錯誤: {e}", flush=True)
        print(body, flush=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ 簽章錯誤", flush=True)
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("🧪 進入訊息處理函式", flush=True)
    print("📨 來源類型：", event.source.type, flush=True)

    if event.source.type == 'group':
        print("✅ 這是一個群組訊息", flush=True)
        print("🔍 群組 ID:", event.source.group_id, flush=True)
    elif event.source.type == 'user':
        print("✅ 這是來自個人的訊息", flush=True)
        print("🔍 使用者 ID:", event.source.user_id, flush=True)
    elif event.source.type == 'room':
        print("📦 這是來自多人聊天室", flush=True)
        print("🔍 Room ID:", event.source.room_id, flush=True)
    else:
        print("❓ 來源未知", flush=True)

    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=f"你說的是：「{event.message.text}」")
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
