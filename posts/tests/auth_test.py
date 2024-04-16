from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

class AuthAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('posts-list')
        self.auth_token_url = reverse('token-obtain-pair')
        self.auth_refresh_token_url = reverse('token-refresh')
        self.user = User.objects.create_user(username='testuser', email='test@gmail.com', password='test123')
        self.access_token = AccessToken.for_user(self.user)

    def test_authenticated_request(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_obtain_pair_view(self):
        data = {'username': self.user.get_username(), 'password': 'test123'}
        response = self.client.post(self.auth_token_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_token_obtain_pair_view_invalid_data(self):
        data = {'username': self.user.get_username()}
        response = self.client.post(self.auth_token_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_token_obtain_pair_view(self):
        auth_token_data = {'username': self.user.get_username(), 'password': 'test123'}
        token_response = self.client.post(self.auth_token_url, data=auth_token_data)
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        auth_refresh_data = {'refresh': token_response.data['refresh']}
        refresh_token_response = self.client.post(self.auth_refresh_token_url, data=auth_refresh_data)
        self.assertEqual(refresh_token_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_token_response.data)
    
    def test_token_obtain_pair_view_invalid_token(self):
        auth_token_data = {'username': self.user.get_username(), 'password': 'test123'}
        token_response = self.client.post(self.auth_token_url, data=auth_token_data)
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        auth_refresh_data = {'refresh': token_response.data['refresh'] + 'wdfefew'}
        refresh_token_response = self.client.post(self.auth_refresh_token_url, data=auth_refresh_data)
        self.assertEqual(refresh_token_response.status_code, status.HTTP_401_UNAUTHORIZED)
