#from linebot import (LineBotApi, WebhookHandler)
#from linebot.exceptions import (InvalidSignatureError)
#from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from datetime import datetime
import requests


URL = 'https://notify-api.line.me/api/notify'
TOKEN = 'iOZ9loBzZ5kCPFGCynEPYQ2mU1LYzFkI2FO6P3ZGn6a'

def send_message(sf_code, container_name):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M")
    msg = sf_code + ' from ' + container_name + ' container progress has been updated at ' + current_time
    """Send a LINE Notify message (with or without an image)."""
    headers = {'Authorization': 'Bearer ' + TOKEN}
    payload = {'message': msg}
    #files = {'imageFile': open(img, 'rb')} if img else None
    r = requests.post(URL, headers=headers, params=payload)
    #if files:
    #    files['imageFile'].close()    
    return r.status_code

