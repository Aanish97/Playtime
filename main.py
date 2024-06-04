from flask import Flask, request
from pymessenger.bot import Bot
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
    return "Message Processed"

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message():
    return "Hello, this is a test message from your bot!"

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "Success"

if __name__ == "__main__":
    app.run(port=5000, debug=True)


