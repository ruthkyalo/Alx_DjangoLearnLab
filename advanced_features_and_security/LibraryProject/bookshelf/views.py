from django.shortcuts import render

# advanced_features_and_security/views.py

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Book

@permission_required('advanced_features_and_security.can_view', raise_exception=True)
def view_books(request):
    books = Book.objects.all()
    return render(request, 'books/list.html', {'books': books})

@permission_required('advanced_features_and_security.can_create', raise_exception=True)
def create_book(request):
    # logic to create book
    pass

@permission_required('advanced_features_and_security.can_edit', raise_exception=True)
def edit_book(request, pk):
    # logic to edit book
    pass

@permission_required('advanced_features_and_security.can_delete', raise_exception=True)
def delete_book(request, pk):
    # logic to delete book
    pass
