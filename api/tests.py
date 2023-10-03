from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Post
from .serializers import UserSerializer, PostSerializer, UserLoginSerializer, PostDetailSerializer

class UserRegistrationViewTestCase(APITestCase):

    def test_user_registration(self):
        url = reverse('user-registration')
        data = {
            "email": "Python@gmail.com",
            "username":"user",
            "password":"123",
            "first_name":"test",
            "last_name":"user"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'user')

class UserLoginViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='Python@gmail.com', password='123')
        self.login_data = {
            'email': 'Python@gmail.com',
            'password': '123'
        }

    def test_user_login(self):
        url = reverse('user-authentication')
        response = self.client.post(url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PostListViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='Python@gmail.com', password='123')
        self.client.force_authenticate(user=self.user)
        self.post_data = {
            'title': 'Test Post',
            'content': 'This is a test post.'
        }

    def test_create_post_authenticated(self):
        url = reverse('post-create')
        response = self.client.post(url, self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Test Post')

    def test_list_all_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PostDetailViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='Python@gmail.com', password='123')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)
        self.updated_data = {
            'title': 'Updated Post',
            'content': 'This is the updated content.'
        }

    def test_retrieve_post(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.put(url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_partial_update_post(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.patch(url, {'title': 'Updated Title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_delete_post(self):
        url = reverse('post-detail', args=[self.post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
