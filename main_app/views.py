from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from . models import Message
from . serializers import MessageSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view

@api_view(http_method_names=['POST'])
def create_message(request, receiver_id):
    serializer = MessageSerializer(data=request.data)

    if serializer.is_valid(raise_exception=ValueError):
        receiver = get_object_or_404(User, id=receiver_id)
        serializer.save(sender=request.user, receiver=receiver)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
def read_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user not in [message.sender, message.receiver]:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = MessageSerializer(message)
    message.is_read = True
    message.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['DELETE'])
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.user not in [message.sender, message.receiver]:
        return Response(status=status.HTTP_403_FORBIDDEN)

    message.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def list_all_messages(request):
    messages = Message.objects.filter(receiver=request.user)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def list_unread_messages(request):
    messages = Message.objects.filter(receiver=request.user, is_read=False)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)