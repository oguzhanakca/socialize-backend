from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')
        
    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logged_in_user_can_create_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_not_logged_in_user_can_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        gonzalo = User.objects.create_user(username='gonzalo', password='pass')
        mura = User.objects.create_user(username='mura', password='pass')
        Post.objects.create(
            owner=gonzalo, title='a title', content='gonzalos post'
        )
        Post.objects.create(
            owner=mura, title='another title', content='muras post'
        )
        
    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_cant_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/18')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_user_can_update_own_post(self):
        self.client.login(username='gonzalo', password='pass')
        response = self.client.put('/posts/1', {'title':'a brand new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a brand new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_cant_update_own_post(self):
        self.client.login(username='gonzalo', password='pass')
        response = self.client.put('/posts/2', {'title':'a brand new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        