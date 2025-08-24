from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """ListView: GET /api/books/ → all books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveAPIView):
    """DetailView: GET /api/books/<pk>/ → single book by id"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(generics.CreateAPIView):
    """CreateView: POST /api/books/create/ → create a new book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookUpdateView(generics.UpdateAPIView):
    """UpdateView: PUT/PATCH /api/books/<pk>/update/ → update a book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDeleteView(generics.DestroyAPIView):
    """DeleteView: DELETE /api/books/<pk>/delete/ → delete a book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
