from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from wall_app.models import WallPost


class WallPostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = WallPost
        fields = ['id', 'owner', 'message']
        ordering = ['created']


class UserSerializer(serializers.ModelSerializer):
    wall_post = serializers.PrimaryKeyRelatedField(many=True, queryset=WallPost.objects.all())

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'wall_post']
        extra_kwargs = {'password': {'write_only': True}, "email": {'required': True}, "username": {'required': True}}

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'], username=validated_data['username'],
                                   password=make_password(validated_data['password']))
        return user
