from unittest.mock import Mock

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.test import APIRequestFactory

from wall_app.views import UserCreate, AnonymousUserCreate

from django.core import mail

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

    def test_register_new_user_and_get_token(self):
        other_user_data = {'username': 'other_user', 'first_name': 'other', 'last_name': "user",
                           'email': 'other_user@email.com', 'password': 'password'}
        request = self.factory.post('/register', other_user_data)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 201)  # 201 status created

        request = self.factory.post('/token', other_user_data)
        response = ObtainAuthToken.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        token = response.data["token"]
        self.assertIsInstance(token, str)

    def test_register_anonymous_user_and_get_token(self):
        other_user_data = {'username': 'other_user', 'email': 'other_user@email.com', 'password': 'password'}
        request = self.factory.post('/register-as-guest', other_user_data)
        response = AnonymousUserCreate.as_view()(request)
        self.assertEqual(response.status_code, 201)  # 201 status created
        self.assertEqual(response.data['success'], True)

        request = self.factory.post('/token', other_user_data)
        response = ObtainAuthToken.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        token = response.data["token"]
        self.assertIsInstance(token, str)

    def test_login(self):
        request = self.factory.post('/token', user_data)
        response = ObtainAuthToken.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        token = response.data["token"]
        self.assertIsInstance(token, str)

    def test_login_wrong_password(self):
        request = self.factory.post('/token', {'username': 'main', 'password': 'wrong_password'})
        response = ObtainAuthToken.as_view()(request)
        self.assertEquals(str(response.data['non_field_errors'][0]), 'Unable to log in with provided credentials.')
        self.assertEquals(response.data['non_field_errors'][0].code, 'authorization')
        self.assertEqual(response.status_code, 400)

