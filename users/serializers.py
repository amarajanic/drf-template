from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import IntegrityError


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)
    confirm_password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        exclude = ('id', 'is_superuser', 'username', 'is_staff', 'is_active',
                   'groups', 'user_permissions', 'last_login', 'date_joined',)


class RegistrationSerializer(serializers.Serializer):
    user = UserSerializer()

    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        res = dict()
        user_data = validated_data.pop('user')
        if user_data['confirm_password'] == user_data['password']:
            try:
                del user_data['confirm_password']
            except KeyError:
                pass
        else:
            res['error'] = 1
            res['user'] = dict(confirm_password=list(
                ['Passwords do not match.']))
            return res

        try:
            User.objects.create_user(**user_data,
                                     username=user_data['email'].lower(),
                                     is_superuser=False, is_staff=False, is_active=True)
        except IntegrityError:
            res['error'] = 1
            res['status'] = 400
            res['details'] = 'That user already exists.'
            return res

        res = {
            'error': 0,
            'status': 201,
            'details': 'User successfully registered.'
        }
        return res
