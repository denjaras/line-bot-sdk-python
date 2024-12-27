import os
from flask import Flask, request, abort
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging.models import TextMessage
from linebot.v3.webhooks.models import MessageEvent

# 環境変数からLINE Botの設定を取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# LINE Bot API設定
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
line_bot_api = MessagingApi(configuration)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Flaskアプリの設定
app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    # X-Line-Signatureヘッダーを取得
    signature = request.headers['X-Line-Signature']
    
    # リクエストボディを取得
    body = request.get_data(as_text=True)
    
    try:
        # Webhookイベントを処理
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        reply_message = f"あなたのメッセージ: {event.message.text}"
        app.logger.info(f"Replying to message: {reply_message}")  # ログ出力
        line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=[TextMessage(text=reply_message)]
        )
    except Exception as e:
        app.logger.error(f"Error while replying to message: {str(e)}")  # エラーログ

if __name__ == "__main__":
    # Heroku用のポート設定
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
