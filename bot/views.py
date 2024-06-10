import json
import os

from django.http.response import HttpResponse
from pymessenger.bot import Bot
from rest_framework.views import APIView


class BotView(APIView):
    def __init__(self):
        # loading the .env variables
        self.PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
        self.VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

        self.bot = Bot(self.PAGE_ACCESS_TOKEN)
        super().__init__()

    def send_message(self, recipient_id, response):
        self.bot.send_text_message(recipient_id, response)
        return "Success"

    def get(self, request):
        # Webhook verification
        if request.GET.get("hub.mode") == "subscribe" and request.GET.get("hub.challenge"):
            if request.GET.get("hub.verify_token") == self.VERIFY_TOKEN:
                return HttpResponse(request.GET["hub.challenge"], status=200)
            return HttpResponse("Verification token mismatch", status=403)
        return HttpResponse("Hello world", status=200)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print(data)  # You may want to log the incoming data for debugging
        if data['object'] == 'page':
            for entry in data['entry']:
                for messaging_event in entry['messaging']:
                    if messaging_event.get('message'):
                        # Handle received message
                        sender_id = messaging_event['sender']['id']
                        message_text = messaging_event['message'].get('text')

                        response = "You said: " + message_text
                        self.bot.send_text_message(sender_id, response)

        return HttpResponse("ok", status=200)


