from django.shortcuts import render

from django.http import HttpResponse
from django.views import View
from .models import Token, PushMessage
from .tasks import push_message
import json

class PublishStreamToken(View):
    def post(self, request, *args, **kwargs):
        stream_token = request.POST['name']

        user_token = Token.objects.filter(stream_token=stream_token)
        if len(user_token) == 1:
            user_token = user_token[0]
            user_token.stream_token = stream_token
            user_token.save()

            push_message_obj = PushMessage.objects.get(identifier="PublishStreamToken.post")
            push_message.delay(push_message_obj.pk, user_token.device_token, custom={"streamToken" : stream_token})
        return HttpResponse('ok')

class ResetStreamToken(View):
    def post(self, request, *args, **kwargs):
        stream_token = request.POST['name']

        user_token = Token.objects.filter(stream_token=stream_token)
        if len(user_token) == 1:
            user_token = user_token[0]
            user_token.stream_token = ""
            user_token.save()

            push_message_obj = PushMessage.objects.get(identifier="ResetStreamToken.post")
            push_message.delay(push_message_obj.pk, user_token.device_token)
        return HttpResponse('ok')

class StoreRetrieveDeviceToken(View):
    def post(self, request, *args, **kwargs):
        received_json_data = json.loads(request.body)
        user_id = received_json_data['userID']
        device_token = received_json_data['deviceToken']

        user_token = Token.objects.filter(user_id=user_id)
        if len(user_token) == 1:
            user_token = user_token[0]
            if user_token.device_token != device_token:
                user_token.device_token = device_token
                user_token.save()
        else:
            user_token = Token(user_id=user_id, device_token=device_token)
            user_token.save()
        return HttpResponse('ok')

class StoreRetrieveStreamToken(View):
    def post(self, request, *args, **kwargs):
        received_json_data = json.loads(request.body)
        user_id = received_json_data['userID']
        stream_token = received_json_data['streamToken']

        user_token = Token.objects.filter(user_id=user_id)
        if len(user_token) == 1:
            user_token = user_token[0]
            user_token.stream_token = stream_token
            user_token.save()
        return HttpResponse('ok')

class CheckStreamStatus(View):
    def post(self, request, *args, **kwargs):
        received_json_data = json.loads(request.body)
        user_id = received_json_data['userID']
        is_streaming = False

        user_token = Token.objects.get(user_id=user_id)
        if user_token and user_token.stream_token:
            is_streaming = True

        # data = serializers.serialize('json', )
        return HttpResponse(json.dumps({"streaming" : is_streaming}))
