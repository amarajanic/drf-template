from rest_framework import generics, status, response
from django.contrib.auth.models import User
from users.serializers import UserSerializer, RegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        res = dict()

        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return response.Response(message)
