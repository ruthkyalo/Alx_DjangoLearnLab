# api/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as filters

from .models import Book
from .serializers import BookSerializer


# Define the filter class for Book
class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    author = filters.CharFilter(field_name="author", lookup_expr="icontains")
    publication_year = filters.NumberFilter(field_name="publication_year")

    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]


# API view for listing and creating books
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter


# API view for retrieving, updating, and deleting a book
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
