from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from time import gmtime, strftime, localtime, time
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

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
    if event.message.text == '選擇日期':
        message = TemplateSendMessage(
            alt_text = '選擇日期',
            template = ButtonsTemplate(
                thumbnailImageUrl = 'https://familylivingtoday.com/wp-content/uploads/2018/09/beach-umbrella.jpg',
                imageAspectRation = "rectangle",
                imageSize = "cover",
                title = '選擇日期',
                text = '請選擇您出發的日期',
                actions = [
                    {
                        "type": "datetimepicker",
                        "label": "選擇出發日期",
                        "data": "setOutDate",
                        "mode": "date",
                        "initial": strftime("%Y-%m-%d", gmtime()),
                        "max": strftime("%Y-%m-%d", localtime(time() + 60*60*24*365)),
                        "min": strftime("%Y-%m-%d", gmtime()),
                    }
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text == '投保試算':
        message = TextSendMessage(
            text='請選擇投保人數',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="label1", text="1人")),
                    QuickReplyButton(action=MessageAction(label="label2", text="2人")),
                    QuickReplyButton(action=MessageAction(label="label3", text="3人")),
                    QuickReplyButton(action=MessageAction(label="label4", text="4人")),
                    QuickReplyButton(action=MessageAction(label="label5", text="5人")),
                    QuickReplyButton(action=MessageAction(label="label6", text="6人")),
                    QuickReplyButton(action=MessageAction(label="label7", text="7人")),
                    QuickReplyButton(action=MessageAction(label="label8", text="8人")),
                    QuickReplyButton(action=MessageAction(label="label9", text="9人")),
                    QuickReplyButton(action=MessageAction(label="label10", text="10人"))
                ]))
    else:
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)

# 處理User postback的資訊
@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'setOutDate':
        message = TextSendMessage(text=event.postback.params['date'])
        line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
