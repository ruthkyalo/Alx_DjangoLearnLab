from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# <Book: 1984 by George Orwell (1949)>

# Admin Interface for Book Model

1. Registered Book model in `bookshelf/admin.py` using `@admin.register`.
2. Displayed `title`, `author`, `publication_year` in list view.
3. Added search fields for `title`, `author`.
4. Added list filter for `publication_year`.
5. Verified through Django admin interface.
