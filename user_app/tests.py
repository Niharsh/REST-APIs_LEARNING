from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class ResgisterUserTestCase(APITestCase):
    
    def test_register_user(self):
        data={
            "username": "testuser",
            'email': "testuser@example.com",
            "password": "testpassword123",
            "password2": "testpassword123"
        }#we create the data to be sent to the register api
        response = self.client.post(reverse('register'), data)#send a post request to the register api
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)#check if the response status code is 201 CREATED

class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',password='testpassword123')
        # if we need to do some intial setup to test our functions we can do that here

    def test_login_user(self):
        data={
            "username": "testuser",
            "password": "testpassword123"
        }#we create the data to be sent to the login api
        response = self.client.post(reverse('login'), data)#send a post request to the login api
        self.assertEqual(response.status_code, status.HTTP_200_OK)#check if the response status code is 200 OK
    
    def test_logout_user(self):
        #now we need to login first to get the token for user and store it and then we can use that token to logout the user
        # First, log in to get the token
        self.token=Token.objects.get(user__username='testuser')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Now, log out using the token
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)