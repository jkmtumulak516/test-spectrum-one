from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets

from users.serializers import UserSerializer

# Create your views here.
class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = []
