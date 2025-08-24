from django.contrib.auth import get_user_model
from django.urls import reverse, NoReverseMatch
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Tests for Book API endpoints covering:
    - List & Detail (read-only)
    - Filtering, Searching, Ordering
    - Permissions (unauth vs auth)
    - CRUD (create/update/delete)
    """

    @classmethod
    def setUpTestData(cls):
        # Users
        User = get_user_model()
        cls.user = User.objects.create_user(username="tester", email="t@example.com", password="pass1234")

        # Authors
        cls.a1 = Author.objects.create(name="Alice Munro")
        cls.a2 = Author.objects.create(name="Bob Martin")

        # Books
        cls.b1 = Book.objects.create(title="Alpha Patterns", publication_year=2001, author=cls.a1)
        cls.b2 = Book.objects.create(title="Beta Clean Code", publication_year=2008, author=cls.a2)
        cls.b3 = Book.objects.create(title="Another Alpha", publication_year=2003, author=cls.a1)

    # --------- URL helpers (try named routes, then fall back to common paths) ---------
    def url_list(self):
        for name in ["book-list", "books-list", "BookListView", "BookListCreateView"]:
            try:
                return reverse(name)
            except NoReverseMatch:
                continue
        # fallback
        return "/api/books/"

    def url_detail(self, pk):
        for name in ["book-detail", "books-detail", "BookDetailView", "BookRetrieveUpdateDestroyView"]:
            try:
                return reverse(name, kwargs={"pk": pk})
            except NoReverseMatch:
                continue
        # fallback
        return f"/api/books/{pk}/"

    def url_create(self):
        # Either POST to list endpoint (ListCreate) or a dedicated /create/ endpoint
        for name in ["book-list", "books-list", "BookListCreateView", "book-create", "BookCreateView"]:
            try:
                return reverse(name)
            except NoReverseMatch:
                continue
        # fallbacks (try list first, then explicit create)
        return "/api/books/"

    def url_update(self, pk):
        # Prefer RUD on detail, else explicit update url
        for name in ["book-detail", "books-detail", "BookRetrieveUpdateDestroyView", "book-update", "BookUpdateView"]:
            try:
                return reverse(name, kwargs={"pk": pk})
            except NoReverseMatch:
                continue
        # fallbacks (detail first, then explicit update route)
        return f"/api/books/{pk}/"

    def url_delete(self, pk):
        # Prefer RUD on detail, else explicit delete url
        for name in ["book-detail", "books-detail", "BookRetrieveUpdateDestroyView", "book-delete", "BookDeleteView"]:
            try:
                return reverse(name, kwargs={"pk": pk})
            except NoReverseMatch:
                continue
        return f"/api/books/{pk}/"

    # Small helper to (re)auth
    def auth(self, user=None):
        self.client = APIClient()
        self.client.force_authenticate(user=user)
