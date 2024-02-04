from keep_alive import keep_alive
from flask import Flask, request, abort
from linebot.models import TextSendMessage
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

app = Flask(__name__)

line_bot_api = LineBotApi('1usGYDtiwI34A0MKb1GXLCCyGwuRZU94aMudOpYFKn7Ukh4myraC+3zBeydwJG1gF2538K50MxppMl/oLneNGH5JCqHvS//WbEMDpSXpNzsshnOb00rkUh4gPqjxk52+d3g7NWNr1IRHHK/gsfUUwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1fe31b6cf315e140a224dd406652a94f')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text
    if input_text.isdigit() and len(input_text) == 6:
        url = f"https://hifumin.app/h/{input_text}/1"  # เปลี่ยน URL ตามที่ต้องการ
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=url)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="กรุณาส่งตัวเลข 6 หลักเท่านั้น")
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


