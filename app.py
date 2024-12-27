from flask import Flask, request, abort

#以下から
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.v3.webhooks import WebhookHandler

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
line_bot_api = MessagingApi(configuration)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

import os 
#ここまでkuratoの追記

from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage



app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = '2006728927'
LINE_CHANNEL_SECRET = '201b3a86cf6564bc78e022fcac1ac8e3'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"あなたのメッセージ: {event.message.text}")
    )

# 以下by kurato
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # 環境変数PORTがない場合はデフォルトで5000を使用
    app.run(host="0.0.0.0", port=port)  # ホストを0.0.0.0に設定して外部接続を許可

