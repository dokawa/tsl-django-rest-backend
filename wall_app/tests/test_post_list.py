from collections import OrderedDict

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate

from wall_app.views import WallPostViewSet

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

    def test_post_message(self):
        request = self.factory.post('/message', {'message': 'Hello World'})
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = WallPostViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)

    def test_get_messages(self):
        message = 'Hello World'

        request = self.factory.post('/message', {'message': message})
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = WallPostViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)

        request = self.factory.get('/')
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = WallPostViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.data['results'][0]['id'], 1)
        self.assertEqual(response.data['results'][0]['owner'], 'main user')
        self.assertEqual(response.data['results'][0]['message'], message)
        self.assertIsInstance(response.data['results'][0], OrderedDict)
        self.assertEqual(response.status_code, 200)