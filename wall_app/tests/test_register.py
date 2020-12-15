from unittest.mock import Mock

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

from rest_framework.authtoken.models import Token

from rest_framework.test import APIRequestFactory

from wall_app.views import UserCreate

user_data = {'username': 'user', 'first_name': 'main', 'last_name': 'user', 'email': 'main_user@email.com',
             'password': 'password'}


class APITest(TestCase):

    def setUp(self):
        super().setUpClass()
        self.factory = APIRequestFactory()
        self.user = User(**user_data)
        self.user.set_password(user_data['password'])
        self.user.save()
        self.user.auth_token = Token.objects.create(user=self.user)

        # Prevents from sending real e-mails on tests
        self.mock_mail = mail
        self.mock_mail.send_mail = Mock()
        self.factory = APIRequestFactory()

    def test_register_already_created_user(self):
        request = self.factory.post('/register', user_data)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.data['username'][0], 'A user with that username already exists.')
        self.assertEqual(response.data['username'][0].code, 'unique')
        self.assertEqual(response.status_code, 400)  # 400 bad request

    def test_register_new_user(self):
        other_user_data = {'username': 'other_user', 'first_name': 'other', 'last_name': "user",
                           'email': 'other_user@email.com', 'password': 'password'}
        request = self.factory.post('/register', other_user_data)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 201)  # 201 status created

    def test_register_with_missing_username(self):
        other_user_data = {'first_name': 'other', 'last_name': "user",
                           'email': 'other_user@email.com', 'password': 'password'}
        request = self.factory.post('/register', other_user_data)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)  # 400 status bad request
        self.assertEqual(str(response.data['username'][0]), 'This field is required.')
        self.assertEqual(response.data['username'][0].code, 'required')

    def test_register_with_missing_first_name(self):
        other_user = {'username': 'other_user', 'last_name': 'user', 'email': 'other_user@email.com', 'password': 'password'}
        request = self.factory.post('/register', other_user)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)  # 400 status bad request
        self.assertEqual(str(response.data['first_name'][0]), 'This field is required.')
        self.assertEqual(response.data['first_name'][0].code, 'required')

    def test_register_with_missing_last_name(self):
        other_user = {'username': 'other_user', 'first_name': 6, 'email': 'other_user@email.com', 'password': 'password'}
        request = self.factory.post('/register', other_user)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)  # 400 status bad request
        self.assertEqual(str(response.data['last_name'][0]), 'This field is required.')
        self.assertEqual(response.data['last_name'][0].code, 'required')

    def test_register_with_missing_email(self):
        other_user = {'username': 'other_user', 'first_name': 'other', 'last_name': 'user', 'password': 'password'}
        request = self.factory.post('/register', other_user)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)  # 400 status bad request
        self.assertEqual(str(response.data['email'][0]), 'This field is required.')
        self.assertEqual(response.data['email'][0].code, 'required')

    def test_register_with_missing_password(self):
        other_user = {'username': 'other_user', 'first_name': 'other', 'last_name': 'user', 'email': 'other_user@email.com'}
        request = self.factory.post('/register', other_user)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)  # 400 status bad request
        self.assertEqual(str(response.data['password'][0]), 'This field is required.')
        self.assertEqual(response.data['password'][0].code, 'required')

    def test_register_with_short_password(self):
        other_user = {'username': 'other_user', 'first_name': 'other', 'last_name': 'user',
                      'email': 'other_user@email.com', 'password': 'pass'}
        request = self.factory.post('/register', other_user)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)  # 400 status bad request
        self.assertEqual(str(response.data['password'][0]),
                         'This password is too short. It must contain at least 8 characters.')
        self.assertEqual(response.data['password'][0].code, 'password_too_short')
