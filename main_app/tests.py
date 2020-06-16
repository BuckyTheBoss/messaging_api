import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from main_app.models import Message
from main_app.serializers import MessageSerializer


class MessagesTest(APITestCase):

    data = {'subject': 'test message 1', 'content': 'A bunch of lorem ipsum'}

    def setUp(self):
        self.user = User.objects.create(username='TestUser1', password='SuperStrongPW')
        self.user2 = User.objects.create(username='TestUser2', password='SuperStrongPW')
        self.user3 = User.objects.create(username='TestUser3', password='SuperStrongPW')
        self.token = Token.objects.create(user=self.user)
        self.token2 = Token.objects.create(user=self.user2)
        self.token3 = Token.objects.create(user=self.user3)

    def authenticate_user_1(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token  ' + self.token.key)

    def authenticate_user_2(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token  ' + self.token2.key)

    def authenticate_user_3(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token  ' + self.token3.key)

    def send_authenticated_message_from_user1_to_user2(self):
        self.authenticate_user_1()
        response = self.client.post(f'/messages/new/{self.user2.id}', self.data)
        return response

    def test_message_send_authenticated(self):
        response = self.send_authenticated_message_from_user1_to_user2()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 1)

    def test_message_send_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(f'/messages/new/{self.user2.id}', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_message_is_marked_as_read_when_viewed_by_receiver(self):
        message_id = self.send_authenticated_message_from_user1_to_user2().data["id"]
        self.authenticate_user_2()
        self.client.get(f'/messages/read/{message_id}/')
        self.assertTrue(Message.objects.get(id=message_id).is_read)

    def test_message_is_not_marked_as_read_when_viewed_by_sender(self):
        message_id = self.send_authenticated_message_from_user1_to_user2().data["id"]
        self.client.get(f'/messages/read/{message_id}/')
        self.assertFalse(Message.objects.get(id=message_id).is_read)

    def test_message_cannot_be_deleted_by_non_owners(self):
        message_id = self.send_authenticated_message_from_user1_to_user2().data["id"]
        self.authenticate_user_3()
        response = self.client.delete(f'/messages/delete/{message_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_message_can_be_deleted_by_owners(self):
        message_id = self.send_authenticated_message_from_user1_to_user2().data["id"]
        self.authenticate_user_2()
        self.client.delete(f'/messages/delete/{message_id}/')
        self.assertFalse(Message.objects.filter(id=message_id).exists())

    def test_receiver_seeing_messages_in_list_view(self):
        self.send_authenticated_message_from_user1_to_user2()
        self.authenticate_user_2()
        response = self.client.get(f'/messages/')
        self.assertTrue(response.data)

    def test_receiver_seeing_messages_in_list_unread_view(self):
        self.send_authenticated_message_from_user1_to_user2()
        self.authenticate_user_2()
        response = self.client.get(f'/messages/unread')
        self.assertTrue(response.data)

    def test_others_not_seeing_messages_in_list_view(self):
        self.send_authenticated_message_from_user1_to_user2()
        self.authenticate_user_3()
        response = self.client.get(f'/messages/')
        self.assertFalse(response.data)

    def test_others_not_seeing_messages_in_list_unread_view(self):
        self.send_authenticated_message_from_user1_to_user2()
        self.authenticate_user_3()
        response = self.client.get(f'/messages/unread')
        self.assertFalse(response.data)
