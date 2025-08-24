from rest_framework import generics, parsers, exceptions, permissions
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    ListView: GET /api/books/
    - Publicly accessible (read-only).
    - Supports optional filters:
        ?author=<id>   → filter by author id
        ?year=<YYYY>   → filter by publication_year
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view

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
    """
    DetailView: GET /api/books/<pk>/
    - Publicly accessible (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    CreateView: POST /api/books/create/
    - Restricted to authenticated users only.
    - Accepts JSON, form, or multipart data.
    - Custom behavior: Title is normalized and must not be empty.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title", "").strip()
        if not title:
            raise exceptions.ValidationError({"title": "Title cannot be empty."})
        serializer.save(title=title)


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView: PUT/PATCH /api/books/<pk>/update/
    - Restricted to authenticated users only.
    - Accepts JSON, form, or multipart data.
    - Custom behavior: Normalize title if provided.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        title = serializer.validated_data.get("title", None)
        if title is not None:
            title = title.strip()
            if not title:
                raise exceptions.ValidationError({"title": "Title cannot be empty."})
            serializer.save(title=title)
        else:
            serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView: DELETE /api/books/<pk>/delete/
    - Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
