from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active']

class NoAuthUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'is_active']
