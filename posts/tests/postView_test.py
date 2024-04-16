from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from posts.models import Post, Comment

class PostViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.access_token = AccessToken.for_user(self.user)
        self.post1 = Post.objects.create(title='Title 1', body='Content 1')
        self.post2 = Post.objects.create(title='Title 2', body='Content 2')
        self.comment1 = Comment.objects.create(post_id=self.post1, name='comment 1', email='test1@gmail.com', body='test body 1')

    def test_list_posts(self):
        url = reverse('posts-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming there are 2 posts

    def test_retrieve_post(self):
        url = reverse('posts-detail', kwargs={'pk': self.post1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Title 1')
        self.assertEqual(response.data['user_id'], 99999942)
        self.assertEqual(response.data['comments'][0]['id'], self.comment1.pk)
        self.assertEqual(response.data['comments'][0]['email'], self.comment1.email)

    def test_update_post(self):
        data = {'title': 'Updated Title', 'body': 'Updated Content'}
        url = reverse('posts-detail', kwargs={'pk': self.post1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['body'], data['body'])
        self.assertEqual(response.data['user_id'], 99999942)
    
    def test_delete_post(self):
        url = reverse('posts-detail', kwargs={'pk': self.post1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
    
    def test_create_post(self):
        data = {'title': 'New Post', 'body': 'New Content'}
        url = reverse('posts-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['body'], data['body'])