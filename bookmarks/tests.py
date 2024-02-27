from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Bookmark
from posts.models import Post

class BookmarkTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(title="Test Post", content="This is a test post")

    def test_create_bookmark(self):
        url = '/bookmarks/'
        data = {'post': self.post.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bookmark.objects.count(), 1)
        self.assertEqual(Bookmark.objects.get().owner, self.user)
        self.assertEqual(Bookmark.objects.get().post, self.post)

    def test_duplicate_bookmark(self):
        Bookmark.objects.create(owner=self.user, post=self.post)
        url = '/bookmarks/'
        data = {'post': self.post.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_bookmark(self):
        bookmark = Bookmark.objects.create(owner=self.user, post=self.post)
        url = f'/bookmarks/{bookmark.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], self.user.username)
        self.assertEqual(response.data['post'], self.post.id)

    def test_delete_bookmark(self):
        bookmark = Bookmark.objects.create(owner=self.user, post=self.post)
        url = f'/bookmarks/{bookmark.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)