from rest_framework import serializers
from . models import Message


class MessageSerializer(serializers.ModelSerializer):
  sender = serializers.StringRelatedField()
  receiver = serializers.StringRelatedField()
  class Meta:
    model = Message
    fields = ('id', 'content', 'subject', 'timestamp', 'sender', 'receiver', 'is_read')
    read_only_fields = ['id', 'timestamp', 'sender', 'receiver', 'is_read']
