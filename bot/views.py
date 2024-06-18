import json
import os
import openai

from django.http.response import HttpResponse
from pymessenger.bot import Bot
from pymessenger.user_profile import UserProfileApi
from rest_framework import status
from rest_framework.views import APIView

from bot.utils import get_user, add_chat


class BotView(APIView):

    def __init__(self):
        # loading the .env variables
        self.PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
        self.VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
        openai.api_key = os.getenv('OPEN_AI_KEY')

        self.fb_user_obj = UserProfileApi(self.PAGE_ACCESS_TOKEN)
        self.bot = Bot(self.PAGE_ACCESS_TOKEN)
        super().__init__()

    def get_chatgpt_response(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=[{
                    "role": "system",
                    "content": "You are a helpful assistant."
                }, {
                    "role": "user",
                    "content": prompt
                }])
            return response['choices'][0]['message']['content'].strip()
        except openai.error.OpenAIError as e:
            if "quota" in str(e).lower():
                return "Error: Quota exceeded. Please check your plan and billing details."
            else:
                return f"Error: {str(e)}"

    def get(self, request):
        # Webhook verification
        if request.GET.get("hub.mode") == "subscribe" and request.GET.get(
                "hub.challenge"):
            if request.GET.get("hub.verify_token") == self.VERIFY_TOKEN:
                return HttpResponse(request.GET["hub.challenge"], status=200)
            return HttpResponse("Verification token mismatch", status=403)
        return HttpResponse(request.GET.get('hub.challenge'),
                            status=status.HTTP_200_OK)

    def post(self, request):
        """
        sample = {
            'object': 'page',
            'entry': [{
                'time': 1718721508391,
                'id': '314121181792314',
                'messaging': [{
                    'sender': {
                        'id': '7661864127265279'
                    },
                    'recipient': {
                        'id': '314121181792314'
                    },
                    'timestamp': 1718721507059,
                    'message': {
                        'mid': 'm_lhPvCASDriMqvIs13TFNFlQZPFjfUoIne9YQEL2laE045XogpBWgBccc_HRgmVcYpmTGENQM3OivjQ-1WN-CRw',
                        'text': 'hi'
                    }
                }]
            }]
        }
        """
        data = json.loads(request.body.decode('utf-8'))
        # print(data)  # You may want to log the incoming data for debugging
        if data['object'] == 'page':
            for entry in data['entry']:
                for messaging_event in entry['messaging']:
                    if messaging_event.get('message'):
                        sender_id = messaging_event['sender']['id']
                        message_text = messaging_event['message'].get('text')
                        fb_user_json = self.fb_user_obj.get(sender_id)

                        user_obj = get_user(fb_user_json)

                        response = self.get_chatgpt_response(message_text)

                        add_chat(message_text, response, user_obj)

                        self.bot.send_text_message(
                            sender_id,
                            response
                        )

        return HttpResponse("OK", status=200)
