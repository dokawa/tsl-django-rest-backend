from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from wall_app.views import UserCreate

user_data = {'username': 'user1', 'email': 'user1@email.com', 'password': 'password'}


class RegisterTest(TestCase):

    def setUp(self):
        super().setUpClass()
        self.factory = APIRequestFactory()
        self.user = User(**user_data)

    def test_register_user(self):
        request = self.factory.post('/register', user_data)
        response = UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)
