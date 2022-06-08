import random

from string import ascii_letters, digits
from typing import Type

from django.contrib.auth.models import User
from django.db import transaction

from users.models import BearerToken, ActivationToken, Token

TOKEN_ALPHABET = ''.join([
    ascii_letters,
    digits,
    '-._~+/',
])

class TokenGenerator(object):

    def generate_bearer_token(self, user: User) -> BearerToken:
        return self._generate_token(BearerToken, user)

    def generate_activation_token(self, user: User) -> ActivationToken:
        return self._generate_token(ActivationToken, user)

    @transaction.atomic
    def _generate_token(self, token_cls: Type[Token], user: User) -> Token:

        token_key = self._generate_token_key()

        while token_cls.objects.filter(key=token_key).exists():
            token_key = self._generate_token_key()

        return token_cls.objects.create(key=token_key, user=user)

    def _generate_token_key(self, length=32) -> str:
        return ''.join(random.choice(TOKEN_ALPHABET) for _ in range(length))
