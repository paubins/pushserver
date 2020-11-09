from django.shortcuts import render

from django.http import HttpResponse
from django.views import View
from .models import Token, PushMessage
from .tasks import push_message

class PublishStreamToken(View):
    def post(self, request, *args, **kwargs):
        stream_token = kwargs['name']

        user_token = Token.objects.get(stream_token=stream_token)
        if user_token:
            user_token.stream_token = stream_token
            user_token.save()

            push_message_obj = PushMessage.objects.get(identifier="PublishStreamToken.post")
            push_message.delay(push_message_obj, user_token.device_token, custom={"streamToken" : stream_token})
        return HttpResponse('ok')

class StoreRetrieveDeviceToken(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs['userID']
        device_token = kwargs['deviceToken']

        user_token = Token.objects.get(user_id=user_id)
        if user_token:
            if user_token.device_token != device_token:
                user_token.device_token = device_token
                user_token.save()
        else:
            user_token = Token(user_id=user_id, device_token=device_token)
            user_token.save()
        return HttpResponse('ok')


class StoreRetrieveStreamToken(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs['userID']
        stream_token = kwargs['streamToken']

        user_token = Token.objects.get(user_id=user_id)
        if user_token:
            user_token.stream_token = stream_token
            user_token.save()
        return HttpResponse('ok')


class ResetStreamToken(View):
    def post(self, request, *args, **kwargs):
        stream_token = kwargs['name']

        user_token = Token.objects.get(stream_token=stream_token)
        if user_token:
            user_token.stream_token = ""
            user_token.save()

            push_message_obj = PushMessage.objects.get(identifier="ResetStreamToken.post")
            push_message.delay(push_message_obj, user_token.device_token)
        return HttpResponse('ok')


class CheckStreamStatus(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs['userID']
        device_token = kwargs['deviceToken']
        is_streaming = False

        user_token = Token.objects.get(user_id=user_id)
        if user_token and user_token.stream_token:
            is_streaming = True
        return HttpResponse({"streaming" : is_streaming})
