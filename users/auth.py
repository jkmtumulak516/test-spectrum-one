import re

from typing import Tuple

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.request import Request

from users.models import BearerToken, User

BEARER_PATTERN = re.compile(r'^Bearer (.+)$')

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Tuple[User, str] | None:

        bearer_string = request.META.get('HTTP_AUTHORIZATION')
        if not bearer_string:
            return None

        match = BEARER_PATTERN.match(bearer_string)
        if match is None:
            raise exceptions.AuthenticationFailed('invalid bearer token')

        token_string = match.group(1)

        try:
            token: BearerToken = BearerToken.objects\
                .select_related('user') \
                .get(key=token_string)
        except BearerToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('invalid bearer token')

        return (token.user, token.key)