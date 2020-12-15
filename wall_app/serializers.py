from gettext import ngettext

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from wall_app.models import WallPost


class DisplayNameField(serializers.RelatedField):
    def to_representation(self, value):
        if value.first_name == "" or value.first_name is None:
            return value.username
        else:
            return '{} {}'.format(value.first_name, value.last_name)


class WallPostSerializer(serializers.ModelSerializer):
    owner = DisplayNameField(read_only=True)

    class Meta:
        model = WallPost
        fields = ['id', 'owner', 'message']
        ordering = ['created']


class UserSerializer(serializers.ModelSerializer):
    wall_post = serializers.PrimaryKeyRelatedField(many=True, queryset=WallPost.objects.all())
    display_name = serializers.SerializerMethodField()

    def get_display_name(self, obj):
        if obj.first_name == "" or obj.first_name is None:
            return obj.username
        else:
            return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'display_name', 'wall_post']
        extra_kwargs = {'password': {'write_only': True}, "email": {'required': True}, "username": {'required': True},
                        'wall_post': {'required': False}
                        }


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'required': True, 'allow_blank': False, 'allow_null': False},
                        'last_name': {'required': True, 'allow_blank': False, 'allow_null': False},
                        "email": {'required': True, 'allow_blank': False, 'allow_null': False},
                        "username": {'required': True}
                        }

    def validate_password(self, password):
        min_length = 8
        if len(password) < min_length:
            raise ValidationError(
                ngettext(
                     "This password is too short. It must contain at least 1 character.",
                     "This password is too short. It must contain at least {} characters.".format(min_length),
                     min_length
                ),
                code='password_too_short',
            )
        return password

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'], email=validated_data['email'],
                                   password=make_password(validated_data['password']))
        return user


class AnonymousUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}, "email": {'required': True, 'allow_blank': False,
                        'allow_null': False}, 'username': {'required': True}
                        }

    def validate_password(self, password):
        min_length = 8
        if len(password) < min_length:
            raise ValidationError(
                ngettext(
                     "This password is too short. It must contain at least 1 character.",
                     "This password is too short. It must contain at least {} characters.".format(min_length),
                     min_length
                ),
                code='password_too_short',
            )
        return password

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'],
                                   password=make_password(validated_data['password']))
        return user
