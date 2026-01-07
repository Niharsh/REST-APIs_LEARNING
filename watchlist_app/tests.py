from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app import models
from watchlist_app.api import serializers

class StreamPlatformTestCase(APITestCase):

    def setUp(self):#`setUp` method is called before each test case is executed
        self.user = User.objects.create_user(username='testuser',password='testpassword123')
        self.token=Token.objects.get(user__username='testuser')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)#set the token in the header for authentication
        self.stream_platform = models.StreamPlatform.objects.create(name="Netflix",about="#1 Platform",website="https://www.netflix.com")

    # Test cases for StreamPlatform API endpoints for admin users
    def test_stream_platform_create(self):
        data={
            "name": "Hulu",
            "about": "Popular Platform",
            "website": "https://www.hulu.com"
        }
        response = self.client.post(reverse('streamplatform'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 

    # Test cases for StreamPlatform API endpoints for normal users
    def test_stream_platform_list(self):
        response = self.client.get(reverse('streamplatform'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    # Test cases for StreamPlatform API endpoints for normal users
    def test_stream_platform_detail(self):
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream_platform.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test cases for StreamPlatform API endpoints for admin users
    def test_stream_platform_update(self):
        data={
            "name": "Netflix Updated",
            "about": "#1 Platform Updated",
            "website": "https://www.netflix.com/updated"
        }
        response = self.client.put(reverse('streamplatform-detail', args=(self.stream_platform.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #Test case for deleting a stream platform for admin users
    def test_stream_platform_delete(self):
        response = self.client.delete(reverse('streamplatform-detail', args=(self.stream_platform.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class WatchlistTestCase(APITestCase):

    # Set up initial data for the tests
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',password='testpassword123')
        self.token=Token.objects.get(user__username='testuser')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream_platform = models.StreamPlatform.objects.create(name="Netflix",about="#1 Platform",website="https://www.netflix.com")
        self.watchlist = models.WatchList.objects.create(title="Example Movie", description="An example movie storyline.", platform=self.stream_platform, active=True)
    #Test cases for Watchlist API endpoints for admin user
    def test_watchlist_create(self):
        data={
            "title": "New Movie",
            "description": "A new movie storyline.",
            "platform": self.stream_platform.id,
            "active": True
        }
        response = self.client.post(reverse('watch-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #Test cases for Watchlist API endpoints for normal users
    def test_watchlist_list(self):
        response = self.client.get(reverse('watch-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    #Test cases for Watchlist API endpoints for normal users
    def test_watchlist_detail(self):
        response = self.client.get(reverse('watchlist-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get(id=self.watchlist.id).title, "Example Movie")

    #Test cases for Watchlist API endpoints for admin users
    def test_watchlist_update(self):
        data={
            "title": "Updated Movie",
            "description": "An updated movie storyline.",
            "platform": self.stream_platform.id,
            "active": False
        }
        response = self.client.put(reverse('watchlist-detail', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #Test case for deleting a watchlist for admin users
    def test_watchlist_delete(self):
        response = self.client.delete(reverse('watchlist-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
 