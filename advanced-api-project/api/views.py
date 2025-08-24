# api/views.py
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework as filters_django
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


# Define the filter class for Book
class BookFilter(filters_django.FilterSet):
    title = filters_django.CharFilter(field_name="title", lookup_expr="icontains")
    author = filters_django.CharFilter(field_name="author", lookup_expr="icontains")
    publication_year = filters_django.NumberFilter(field_name="publication_year")

    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]


# API view for listing and creating books
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Add filtering + ordering + search
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BookFilter
    ordering_fields = ["title", "author", "publication_year"]
    ordering = ["title"]  # default ordering

    # Fields that can be searched using ?search=
    search_fields = ["title", "author"]


# API view for retrieving, updating, and deleting a book
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
