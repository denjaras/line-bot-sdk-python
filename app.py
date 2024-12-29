import os
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

# 環境変数からLINE Botの設定を取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'



# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     user_id = event.source.user_id
#     received_message = event.message.text
#     app.logger.info(f"Message from user {user_id}: {received_message}")

#     try:
#         user_message = event.message.text
#         app.logger.info(f"Received message: {user_message}")
        
#         reply_message = f"あなたのメッセージ: {user_message}"
#         app.logger.info(f"Replying with message: {reply_message}")

#         with ApiClient(configuration) as api_client:
#             line_bot_api = MessagingApi(api_client)
#             line_bot_api.reply_message_with_http_info(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text=reply_message)]
#                 )
#             )
#         app.logger.info("Reply sent successfully")
#     except Exception as e:
#         app.logger.error(f"Error while handling message: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Heroku用のポート設定
    app.run(host="0.0.0.0", port=port)
