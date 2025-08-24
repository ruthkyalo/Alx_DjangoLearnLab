from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    """
    AuthorViewSet
    -------------
    Handles CRUD for Author objects.
    - list:   GET /authors/        -> returns all authors
    - create: POST /authors/       -> create a new author
    - retrieve: GET /authors/{id}/ -> fetch a single author
    - update: PUT/PATCH /authors/{id}/ -> update an author
    - destroy: DELETE /authors/{id}/   -> delete an author

    Nested Relationship:
    --------------------
    Each author includes their related books (via AuthorSerializer).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    BookViewSet
    -----------
    Handles CRUD for Book objects.
    - list:   GET /books/        -> returns all books
    - create: POST /books/       -> create a new book
    - retrieve: GET /books/{id}/ -> fetch a single book
    - update: PUT/PATCH /books/{id}/ -> update a book
    - destroy: DELETE /books/{id}/   -> delete a book

    Custom Behavior:
    ----------------
    - Includes validation to ensure 'publication_year' is not in the future,
      handled in the BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
