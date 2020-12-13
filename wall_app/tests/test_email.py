from unittest import TestCase
from unittest.mock import Mock
from django.core import mail

from rest_framework.test import APIRequestFactory

from wall_app.views import UserCreate, AnonymousUserCreate


class APITest(TestCase):

    def setUp(self):
        super().setUpClass()
        self.mock_mail = mail
        self.mock_mail.send_mail = Mock()
        self.factory = APIRequestFactory()

    def test_send_mail_on_user_create(self):
        user_data = {'username': 'user', 'first_name': 'main', 'last_name': 'user', 'email': 'main_user@email.com',
                     'password': 'password'}
        request = self.factory.post('/register', user_data)

        UserCreate.as_view()(request)
        self.mock_mail.send_mail.assert_called_once()

    def test_send_mail_on_user_create(self):
        other_user_data = {'username': 'other_user', 'email': 'other_user@email.com', 'password': 'password'}
        request = self.factory.post('/register', other_user_data)

        AnonymousUserCreate.as_view()(request)
        self.mock_mail.send_mail.assert_called_once()
