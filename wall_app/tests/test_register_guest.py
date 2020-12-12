from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.authtoken.models import Token

from rest_framework.test import APIRequestFactory

from wall_app.views import AnonymousUserCreate

user_data = {'username': 'user', 'email': 'main_user@email.com', 'password': 'password'}


class APITest(TestCase):

    def setUp(self):
        super().setUpClass()
        self.factory = APIRequestFactory()
        self.user = User(**user_data)
        self.user.set_password(user_data['password'])
        self.user.save()
        self.user.auth_token = Token.objects.create(user=self.user)

    def test_register_already_created_user(self):
        request = self.factory.post('/register', user_data)
        response = AnonymousUserCreate.as_view()(request)
        self.assertEqual(response.data['username'][0], 'A user with that username already exists.')
        self.assertEqual(response.data['username'][0].code, 'unique')
        self.assertEqual(response.status_code, 400)  # 400 bad request

    def test_register_new_user(self):
        other_user_data = {'username': 'other_user', 'email': 'other_user@email.com', 'password': 'password'}
        request = self.factory.post('/register', other_user_data)
        response = AnonymousUserCreate.as_view()(request)
        self.assertEqual(response.status_code, 201)  # 201 status created

    def test_register_with_missing_username(self):
        other_user_data = {'email': 'other_user@email.com', 'password': 'password'}
        request = self.factory.post('/register', other_user_data)
        response = AnonymousUserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)  # 400 status bad request
        self.assertEqual(str(response.data['username'][0]), 'This field is required.')
        self.assertEqual(response.data['username'][0].code, 'required')

    def test_register_with_missing_email(self):
        other_user = {'username': 'other_user', 'password': 'password'}
        request = self.factory.post('/register', other_user)
        response = AnonymousUserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)  # 400 status bad request
        self.assertEqual(str(response.data['email'][0]), 'This field is required.')
        self.assertEqual(response.data['email'][0].code, 'required')

    def test_register_with_missing_password(self):
        other_user = {'username': 'other_user', 'first_name': 'other', 'last_name': 'user',
                      'email': 'other_user@email.com'}
        request = self.factory.post('/register', other_user)
        response = AnonymousUserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)  # 400 status bad request
        self.assertEqual(str(response.data['password'][0]), 'This field is required.')
        self.assertEqual(response.data['password'][0].code, 'required')
