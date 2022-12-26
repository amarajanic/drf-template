import datetime
from django.db import models
from django.contrib.auth.models import User


class Roles(models.Model):
    ADMINISTRATOR = 'admin'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMINISTRATOR, 'administrator'),
        (USER, 'user'),
    ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )
    created_at = models.DateTimeField(datetime.datetime.now())
    modified_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = "roles"


class Gender(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )
    created_at = models.DateTimeField(datetime.datetime.now())
    modified_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'genders'


class AdditionalUserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_url = models.ImageField(
        null=True, blank=True, upload_to='images/profile-pictures/')
    role_id = models.ForeignKey(
        Roles, on_delete=models.DO_NOTHING, blank=False)
    birth_year = models.IntegerField(null=False, blank=False, default=2000)
    gender = models.ForeignKey(
        Gender, blank=False, on_delete=models.DO_NOTHING)
    date_registred = models.DateTimeField(datetime.datetime.now())
    created_at = models.DateTimeField(datetime.datetime.now())
    modified_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f'user: {self.user}\npicture_url: {self.profile_picture_url}\nrole: {self.role_id}'

    class Meta:
        db_table = "additional_user_data"
