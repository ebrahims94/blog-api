from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from posts.models import Comment, Post

class CommentViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.access_token = AccessToken.for_user(self.user)
        self.post = Post.objects.create(title='Title 1', body='Content 1')
        self.comment1 = Comment.objects.create(post_id=self.post, name='comment 1', email='test1@gmail.com', body='test body 1')
        self.comment2 = Comment.objects.create(post_id=self.post, name='comment 2', email='test2@gmail.com', body='test body 2')

    def test_list_comments(self):
        url = reverse('comments-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_comment(self):
        url = reverse('comments-detail', kwargs={'pk': self.comment1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'comment 1')
    
    def test_update_comment(self):
        data = {'name': 'Updated name', 'body': 'Updated Content', 'post_id': self.post.pk}
        url = reverse('comments-detail', kwargs={'pk': self.comment1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['body'], data['body'])
        self.assertEqual(response.data['email'], 'test1@gmail.com')
    
    def test_delete_comment(self):
        url = reverse('comments-detail', kwargs={'pk': self.comment1.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
    
    def test_create_comment(self):
        data = {'name': 'New comment', 'body': 'New Content', 'email': 'new@gmail.com', 'post_id': self.post.pk}
        url = reverse('comments-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['body'], data['body'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['post_id'], self.post.pk)