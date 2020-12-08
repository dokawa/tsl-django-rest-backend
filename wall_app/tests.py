import configparser
import os

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIRequestFactory, force_authenticate

from django_rest_backend import settings
from wall_app.views import UserCreate, WallPostViewSet


user_data_1 = {'username': 'user1', 'first_name': 'user', 'last_name': 1, 'email': 'user1@email.com', 'password': 'password'}
user_data_2 = {'username': 'user2', 'first_name': 'user', 'last_name': 2, 'email': 'user2@email.com', 'password': 'password'}


class APITest(TestCase):

    def setUp(self):
        super().setUpClass()
        self.factory = APIRequestFactory()
        self.user = User(**user_data_1)
        self.user.set_password(user_data_1['password'])
        self.user.save()
        self.user.auth_token = Token.objects.create(user=self.user)

    def test_register_already_created_user(self):
        request = self.factory.post('/register', user_data_1)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.data['username'][0], 'A user with that username already exists.')
        self.assertEqual(response.data['username'][0].code, 'unique')
        self.assertEqual(response.status_code, 400)             # 400 bad request

    def test_register_new_user(self):
        request = self.factory.post('/register', user_data_2)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 201)  # 201 status created

    def test_post_message(self):
        request = self.factory.post('/message', {'message': 'Hello World'})
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = WallPostViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        request = self.factory.post('/token', user_data_1)
        response = ObtainAuthToken.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        token = response.data["token"]
        self.assertIsInstance(token, str)

        request = self.factory.post('/token', {'username': 'user1', 'password': 'wrong_password'})
        response = ObtainAuthToken.as_view()(request)
        self.assertEquals(str(response.data['non_field_errors'][0]), 'Unable to log in with provided credentials.')
        self.assertEquals(response.data['non_field_errors'][0].code, 'authorization')
        self.assertEqual(response.status_code, 400)







