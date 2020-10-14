from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from datetime import datetime


def send_message(sf_code, container_name):      
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")
    line_bot_api = LineBotApi('LqzzZREWJQl3tZ80owftCeC6UFzgW47s4Y/ZgFEj5SANQPC8s8m6XPZRNAAaeboSOofX1PUhP8Bby9+yZciQW3A9rajXAkjYHIf9dw3VK5peiAxrqd6OdMAOjsf5zeJZlmKI4L0/URAYsNY0liiKCgdB04t89/1O/w1cDnyilFU=')
    handler = WebhookHandler('1bedc1daf1ea4c0119a4b9b86f46b5af')
    line_bot_api.push_message('U7965381d1b871ed0f2ac9a06c1a9f88e', TextSendMessage(text=current_time + ' > ' + sf_code + ' from ' + container_name + ' container progress has been updated'))     
    #print('{} product from {} container progress has been updated'.format(instance.sf_code, instance.container_name))
    