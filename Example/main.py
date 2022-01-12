
# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import os
import sys
import function
import time
import picamera
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = 'YOUR CHANNEL SECRET'
channel_access_token = 'YOUR CHANNEL ACCESS TOKEN'

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
line_bot_api.push_message('YOUR USER ID', TextSendMessage(text='你可以開始了'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        message = event.message.text
        reply = event.message.text

        if message.count('顯示現在溫度'):
            temperature = function.temperature()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="現在溫度是" + str(temperature) + "度C"))
        elif message.count('顯示溫濕度紀錄'):
            ngrok_url = function.get_ngrok_url()
            exec(open("download_graph_45.py").read())
            line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url = ngrok_url + "/static/cacti_graph_45.png" , preview_image_url = ngrok_url + "/static/cacti_graph_45.png"))


        elif message.count('拍張照'):
            exec(open("capture.py").read())
            ngrok_url = function.get_ngrok_url()
            line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url = ngrok_url + "/static/LiveImage.jpg" , preview_image_url = ngrok_url + "/static/LiveImage.jpg"))

        else:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
