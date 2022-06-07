from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users import serializers

# Create your views here.
class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = []

    @action(detail=False, methods=['post'], name='Register User')
    def register(self, request):

        serializer = serializers.UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data['email']
        if User.objects.filter(email=email).exists():
            return Response(f'{email} exists', status=400)

        # TODO generate activation key
        # TODO send email

        serializer.save()

        return Response(serializer.data, status=201)
