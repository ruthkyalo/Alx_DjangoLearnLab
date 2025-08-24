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

    # --------- URL helpers ---------
    def url_list(self):
        for name in ["book-list", "books-list", "BookListView", "BookListCreateView"]:
            try:
                return reverse(name)
            except NoReverseMatch:
                continue
        return "/api/books/"

    def url_detail(self, pk):
        for name in ["book-detail", "books-detail", "BookDetailView", "BookRetrieveUpdateDestroyView"]:
            try:
                return reverse(name, kwargs={"pk": pk})
            except NoReverseMatch:
                continue
        return f"/api/books/{pk}/"

    def url_create(self):
        for name in ["book-list", "books-list", "BookListCreateView", "book-create", "BookCreateView"]:
            try:
                return reverse(name)
            except NoReverseMatch:
                continue
        return "/api/books/"

    def url_update(self, pk):
        for name in ["book-detail", "books-detail", "BookRetrieveUpdateDestroyView", "book-update", "BookUpdateView"]:
            try:
                return reverse(name, kwargs={"pk": pk})
            except NoReverseMatch:
                continue
        return f"/api/books/{pk}/"

    def url_delete(self, pk):
        for name in ["book-detail", "books-detail", "BookRetrieveUpdateDestroyView", "book-delete", "BookDeleteView"]:
            try:
                return reverse(name, kwargs={"pk": pk})
            except NoReverseMatch:
                continue
        return f"/api/books/{pk}/"

    def auth(self, user=None):
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    # -------------------- Read-only tests --------------------
    def test_list_books_ok(self):
        url = self.url_list()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # use response.data
        self.assertGreaterEqual(len(resp.data), 3)

    def test_detail_book_ok(self):
        url = self.url_detail(self.b1.pk)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("title"), "Alpha Patterns")

    # -------------------- Filtering --------------------
    def test_filter_by_author(self):
        url = self.url_list()
        resp = self.client.get(f"{url}?author={self.a1.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.data]   # ✅ response.data
        self.assertTrue("Alpha Patterns" in titles and "Another Alpha" in titles)
        self.assertNotIn("Beta Clean Code", titles)

    def test_filter_by_publication_year(self):
        url = self.url_list()
        resp = self.client.get(f"{url}?publication_year=2008")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.data]
        self.assertEqual(titles, ["Beta Clean Code"])

    # -------------------- Searching --------------------
    def test_search_by_title_or_author(self):
        url = self.url_list()
        resp = self.client.get(f"{url}?search=Alpha")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = sorted([b["title"] for b in resp.data])
        self.assertEqual(titles, ["Alpha Patterns", "Another Alpha"])

        resp2 = self.client.get(f"{url}?search=Martin")
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        titles2 = [b["title"] for b in resp2.data]
        self.assertIn("Beta Clean Code", titles2)

    # -------------------- Ordering --------------------
    def test_ordering_by_title_desc(self):
        url = self.url_list()
        resp = self.client.get(f"{url}?ordering=-title")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.data]
        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_ordering_by_year_asc(self):
        url = self.url_list()
        resp = self.client.get(f"{url}?ordering=publication_year")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp.data]
        self.assertEqual(years, sorted(years))

    # -------------------- Permissions --------------------
    def test_create_requires_auth(self):
        self.auth(user=None)
        data = {"title": "Gamma", "publication_year": 2010, "author": self.a1.id}
        url = self.url_create()
        resp = self.client.post(url, data, format="json")
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_update_requires_auth(self):
        self.auth(user=None)
        url = self.url_update(self.b1.id)
        resp = self.client.patch(url, {"title": "Alpha Revised"}, format="json")
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_delete_requires_auth(self):
        self.auth(user=None)
        url = self.url_delete(self.b2.id)
        resp = self.client.delete(url)
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    # -------------------- CRUD (authenticated) --------------------
    def test_create_book_authenticated(self):
        self.auth(user=self.user)
        data = {"title": "Gamma Practices", "publication_year": 2010, "author": self.a1.id}
        url = self.url_create()
        resp = self.client.post(url, data, format="json")
        if resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            url = "/api/books/create/"
            resp = self.client.post(url, data, format="json")

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        #  Check response.data
        self.assertEqual(resp.data["title"], "Gamma Practices")
        self.assertEqual(Book.objects.filter(title="Gamma Practices").count(), 1)

    def test_update_book_authenticated(self):
        self.auth(user=self.user)
        url = self.url_update(self.b1.id)
        resp = self.client.patch(url, {"title": "Alpha Patterns (2nd Ed.)"}, format="json")
        if resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            url = f"/api/books/{self.b1.id}/update/"
            resp = self.client.patch(url, {"title": "Alpha Patterns (2nd Ed.)"}, format="json")

        self.assertIn(resp.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED])
        # Check response.data
        self.assertEqual(resp.data["title"], "Alpha Patterns (2nd Ed.)")
        self.b1.refresh_from_db()
        self.assertEqual(self.b1.title, "Alpha Patterns (2nd Ed.)")

    def test_delete_book_authenticated(self):
        self.auth(user=self.user)
        url = self.url_delete(self.b3.id)
        resp = self.client.delete(url)
        if resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            url = f"/api/books/{self.b3.id}/delete/"
            resp = self.client.delete(url)

        self.assertIn(resp.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])
        if resp.status_code == status.HTTP_200_OK:
            self.assertIn("message", resp.data)
        self.assertFalse(Book.objects.filter(id=self.b3.id).exists())
