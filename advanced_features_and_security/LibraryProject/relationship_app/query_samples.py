import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

# Import models AFTER setting up Django
from relationship_app.models import Author, Book, Library, Librarian

# Create data if not exists
author, created = Author.objects.get_or_create(name="Jane Austen")
book1, _ = Book.objects.get_or_create(title="Pride and Prejudice", author=author)
book2, _ = Book.objects.get_or_create(title="Sense and Sensibility", author=author)
library, _ = Library.objects.get_or_create(name="Central Library")
library.books.set([book1, book2])
librarian, _ = Librarian.objects.get_or_create(name="Mr. John", library=library)

# 1. Query all books by a specific author
author_name = "Jane Austen"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

# 2. List all books in a library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print(f"Books in {library_name}: {[book.title for book in books_in_library]}")

# 3. Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print(f"Librarian for {library_name}: {librarian.name}")
