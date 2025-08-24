from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters import rest_framework as django_filters
from .models import Book
from .serializers import BookSerializer


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],
            'author': ['icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
        }


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = BookFilter
    ordering_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
