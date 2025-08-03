
from .forms import BookSearchForm
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/list.html', {'books': books})

def book_list(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()
    if form.is_valid():
        title = form.cleaned_data.get('title')
        if title:
            books = books.filter(title__icontains=title)
    return render(request, 'bookshelf/book_list.html', {'form': form, 'books': books})

