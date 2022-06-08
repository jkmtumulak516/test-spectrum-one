from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, Serializer, EmailField, CharField


class UserSerializer(ModelSerializer):

    email = EmailField()
    password = CharField(
        write_only=True,
        style={'input_type': 'password'},
    )
    first_name = CharField(required=False)
    last_name = CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'password')
        read_only_fields = ('id', 'is_active')

    def __init__(self, instance=None, data=..., **kwargs):
        request: Request = kwargs['context']['request']
        user: User = request.user

        if user.is_anonymous:
            del self.fields['email']
            del self.fields['last_name']

        super().__init__(instance, data, **kwargs)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data['username'] = validated_data['email']
        validated_data['is_active'] = False
        return super(UserSerializer, self).create(validated_data)

class NoAuthUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'is_active']

class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField(style={'input_type': 'password'})

class ChangePasswordSerializer(Serializer):
    password = CharField(style={'input_type': 'password'})
