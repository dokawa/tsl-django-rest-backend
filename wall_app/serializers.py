from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    # user = serializers.ModelSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}, "email": {'required': True}, "username": {'required':True} }

    # def create(self, data):
    #     user = User(**data)
    #     user.set_password(data['password'])
    #     user.save()
    #     return user

