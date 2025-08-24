from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        # Create a sample book
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            publication_year=2023
        )

        # Define endpoints
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book.id])

    def test_list_books_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])  #  Using response.data

    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="testpass123")  #  Uses login

        data = {
            "title": "New Book",
            "author": "Jane Doe",
            "publication_year": 2024,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")

    def test_create_book_unauthenticated(self):
        data = {
            "title": "Unauthorized Book",
            "author": "Hacker",
            "publication_year": 2025,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="testpass123")

        data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "publication_year": 2026,
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")

    def test_delete_book_authenticated(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_book_unauthenticated(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
