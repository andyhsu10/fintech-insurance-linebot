from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from state.insurance_state import InitState
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

insurance = None

class InsuranceBot(object):
    def __init__(self):
        """ Initialize the components. """

        # Start with a default state.
        self.state = InitState()
        self.msg = self.state.message

    def on_event(self, event, data):
        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event, data)
        self.msg = self.state.message

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global insurance
    if event.message.text == '開始使用':
        insurance = InsuranceBot()
        line_bot_api.reply_message(event.reply_token, insurance.msg)
    else:
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)

# 處理User postback的資訊
@handler.add(PostbackEvent)
def handle_postback(event):
    global insurance
    if event.postback.data.split('&')[0]:
        insurance.on_event(event.postback.data.split('&')[0], event.postback.params)
        line_bot_api.reply_message(event.reply_token, insurance.msg)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
