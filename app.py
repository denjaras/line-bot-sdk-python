import os
import logging  # 追加

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

import openai

app = Flask(__name__)

# ログレベルをINFOに設定
logging.basicConfig(level=logging.INFO)  # ログ設定を明示
app.logger.setLevel(logging.INFO)

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

    # app.logger.info("Request body: " + body)
    app.logger.info("Vienna")

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# ChatGPT用の関数
def generate_reply(message):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, world!"}
            ],
            max_tokens=50
        )
        reply = response.choices[0].text.strip()
        return reply
    except Exception as e:
        app.logger.error(f"Error generating reply: {str(e)}")
        return "申し訳ありませんが、現在応答できません。"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text
    app.logger.info(f"User message: {user_message}")
    
    # ChatGPTからの返信を取得
    reply_message = generate_reply(user_message)
    app.logger.info(f"Reply message: {reply_message}")
    
    # ユーザーに返信
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )

# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=event.message.text)]
#             )
#         )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Heroku用のポート設定
    app.run(host="0.0.0.0", port=port)