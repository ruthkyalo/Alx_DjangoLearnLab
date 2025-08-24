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

    # -------------------- Read-only tests --------------------
    def test_list_books_ok(self):
        url = self.url_list()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.json()), 3)

    def test_detail_book_ok(self):
        url = self.url_detail(self.b1.pk)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json().get("title"), "Alpha Patterns")

    # -------------------- Filtering --------------------
    def test_filter_by_author(self):
        url = self.url_list()
        resp = self.client.get(f"{url}?author={self.a1.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertTrue("Alpha Patterns" in titles and "Another Alpha" in titles)
        self.assertNotIn("Beta Clean Code", titles)

    def test_filter_by_publication_year(self):
        url = self.url_list()
        resp = self.client.get(f"{url}?publication_year=2008")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertEqual(titles, ["Beta Clean Code"])

    # -------------------- Searching --------------------
    def test_search_by_title_or_author(self):
        url = self.url_list()
        # should match "Alpha Patterns" and "Another Alpha"
        resp = self.client.get(f"{url}?search=Alpha")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = sorted([b["title"] for b in resp.json()])
        self.assertEqual(titles, ["Alpha Patterns", "Another Alpha"])

        # should match author "Bob Martin" via author__name if configured
        resp2 = self.client.get(f"{url}?search=Martin")
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        titles2 = [b["title"] for b in resp2.json()]
        self.assertIn("Beta Clean Code", titles2)

    # -------------------- Ordering --------------------
    def test_ordering_by_title_desc(self):
        url = self.url_list()
        resp = self.client.get(f"{url}?ordering=-title")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_ordering_by_year_asc(self):
        url = self.url_list()
        resp = self.client.get(f"{url}?ordering=publication_year")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp.json()]
        self.assertEqual(years, sorted(years))
