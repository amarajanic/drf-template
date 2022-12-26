"""Tests for authentication endpoints"""

from django.test import TestCase

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

LOGIN_URL = reverse('token_obtain_pair')
REFRESH_URL = reverse('token_refresh')


def create_user(**params):
    """Create and return a new user"""
    return User.objects.create_user(**params)


class AuthAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        create_user(username='test123@gmail.com', password='PassWord1234!')

    def test_user_login_successfull(self):
        username = 'test123@gmail.com'
        password = 'PassWord1234!'

        res = self.client.post(
            LOGIN_URL, {'username': username, 'password': password})
        self.assertTrue('refresh' in res.data)
        self.assertTrue('access' in res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_login_wrong_username(self):
        username = 'test234@gmail.com'
        password = 'PassWord1234!'

        res = self.client.post(
            LOGIN_URL, {'username': username, 'password': password})
        self.assertTrue('refresh' not in res.data)
        self.assertTrue('access' not in res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_wrong_password(self):
        username = 'test123@gmail.com'
        password = 'PassWord123!'

        res = self.client.post(
            LOGIN_URL, {'username': username, 'password': password})
        self.assertTrue('refresh' not in res.data)
        self.assertTrue('access' not in res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_route(self):
        username = 'test123@gmail.com'
        password = 'PassWord1234!'

        res1 = self.client.post(
            LOGIN_URL, {'username': username, 'password': password})

        res2 = self.client.post(REFRESH_URL, {'refresh': res1.data['refresh']})

        self.assertTrue('refresh' in res2.data)
        self.assertTrue('access' in res2.data)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
