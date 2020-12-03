from django.contrib.auth.models import User
from rest_framework import serializers

from wall_app.models import WallPost


class WallPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WallPost
        # owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['id', 'text']
        ordering = ['created']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}, "email": {'required': True}, "username": {'required': True}}
