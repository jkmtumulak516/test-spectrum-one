from urllib.parse import quote

from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from spectrum import settings
from users import serializers
from users.tokens import TokenGenerator, TokenValidator

# Create your views here.
class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = []

    @action(detail=False, methods=['post'], name='Register User')
    def register(self, request: Request):

        serializer = serializers.UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email: str = serializer.validated_data['email']
        if User.objects.filter(email=email).exists():
            return Response(f'{email} exists', status=400)

        serializer.save()
        user: User = serializer.instance

        token_generator = TokenGenerator()
        token = token_generator.generate_activation_token(user)

        activation_url = f'{reverse("activate-user", request=request)}?at={quote(token.key, safe="")}'
        email_contents = f'Please click on the link to activate your new account:\n\n{activation_url}'

        send_mail(
            'Account Activation',
            email_contents,
            settings.EMAIL_HOST_USERA,
            [user.email],
            fail_silently=True,
        )

        return Response(serializer.data, status=201)

    @action(detail=False, methods=['put'], name='Activate User')
    def activate(self, request: Request):

        token_string = request.query_params.get('at', None)
        if token_string is None:
            return Response('activation token missing', status=400)

        token_validator = TokenValidator()
        user = token_validator.validate_activation_token(token_string)

        if user is None:
            return Response('invalid activation token', status=400)

        if user.is_active:
            return Response('user is already active', status=400)

        user.is_active = True
        user.save()

        serializer = serializers.UserSerializer(instance=user)

        return Response(serializer.data, status=200)
