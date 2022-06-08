from django.contrib.auth.models import User
from django.db import models

class Token(models.Model):

    key = models.CharField(max_length=32, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class BearerToken(Token):
    pass

class ActivationToken(Token):
    pass
