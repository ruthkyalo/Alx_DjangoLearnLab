from django.shortcuts import render
from .models import Book, Author, Library
from django.views.generic import DetailView

# Function-Based View to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

# Class-Based View for library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
