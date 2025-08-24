from rest_framework import generics, parsers, exceptions
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    """
    ListView: GET /api/books/
    Optional filters:
      - ?author=<id>  → filter by author id
      - ?year=<YYYY>  → filter by publication_year
    """
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = Book.objects.all()
        author_id = self.request.query_params.get("author")
        year = self.request.query_params.get("year")
        if author_id:
            qs = qs.filter(author_id=author_id)
        if year:
            qs = qs.filter(publication_year=year)
        return qs


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Accept JSON, form, and multipart
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def perform_create(self, serializer):
        # Example customization: normalize the title and enforce non-empty
        title = serializer.validated_data.get("title", "")
        title = title.strip()
        if not title:
            raise exceptions.ValidationError({"title": "Title cannot be empty."})
        serializer.save(title=title)


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def perform_update(self, serializer):
        # Normalize title if provided
        title = serializer.validated_data.get("title", None)
        if title is not None:
            title = title.strip()
            if not title:
                raise exceptions.ValidationError({"title": "Title cannot be empty."})
            serializer.save(title=title)
        else:
            serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
