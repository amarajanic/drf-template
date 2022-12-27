from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import IntegrityError
from drf_extra_fields.fields import Base64ImageField
from users.models import AdditionalUserData, Gender, Roles
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        exclude = ('created_at', 'modified_at',)


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        exclude = ('created_at', 'modified_at',)


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


class UserAdditionalRegistrationSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField(required=False)
    birth_year = serializers.IntegerField(
        required=True, validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    gender = GenderSerializer()

    class Meta:
        model = AdditionalUserData
        exclude = ('id', 'user', 'role_id', 'profile_picture_url',
                   'created_at', 'modified_at', 'date_registred',)


class RegistrationSerializer(serializers.Serializer):
    user = UserSerializer()
    additional_data = UserAdditionalRegistrationSerializer()

    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        res = dict()
        user_data = validated_data.pop('user')

        additional_data = validated_data.pop('additional_data')

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
            user_model = User.objects.create_user(**user_data,
                                                  username=user_data['email'].lower(
                                                  ),
                                                  is_superuser=False, is_staff=False, is_active=True)
        except IntegrityError:
            res['error'] = 1
            res['status'] = 400
            res['details'] = 'That user already exists.'
            return res
        user_gender = additional_data.pop('gender')
       # try:
        role = Roles.objects.get(name__icontains='user')
        AdditionalUserData.objects.create(
            **additional_data, user=user_model, role_id=role, gender_id=Gender.objects.filter(
                name__icontains=user_gender['name']).first().id, date_registred=datetime.now(), created_at=datetime.now())
        """except:
            res['error'] = 1
            res['status'] = 400
            res['details'] = 'There was a problem with a roles.'
            return res"""

        res = {
            'error': 0,
            'status': 201,
            'details': 'User successfully registered.'
        }
        return res
