from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status, response
from django.contrib.auth.models import User


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        res = dict()

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(username=request.data['username'])
        except ObjectDoesNotExist:
            res['detail'] = 'Could not get the user data.'
            return response.Response(res, status=400)

        return response.Response({
            'refresh': data['refresh'],
            'access': data['access'],
        }, status=200)
