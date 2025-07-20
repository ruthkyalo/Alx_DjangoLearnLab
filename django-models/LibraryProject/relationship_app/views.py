from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .models import Library, Book, UserProfile
from .forms import BookForm  # <-- Make sure to create this form!

# Function-Based View to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-Based View for Library Detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Adjust this redirect if needed
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Role checker factory
def check_role(role):
    def inner(user):
        try:
            return user.userprofile.role == role
        except UserProfile.DoesNotExist:
            return False
    return inner

# Role-based dashboard views
@login_required
@user_passes_test(check_role('Admin'))
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(check_role('Librarian'))
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(check_role('Member'))
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# Combined decorator for class-based views with role and permission
def class_login_role_and_permission_required(role, permission):
    return method_decorator([
        login_required,
        user_passes_test(check_role(role)),
        permission_required(permission, raise_exception=True)
    ], name='dispatch')

# Librarian-only book management views with permission checks
@class_login_role_and_permission_required('Librarian', 'relationship_app.add_book')
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book_form.html'
    success_url = reverse_lazy('list_books')

@class_login_role_and_permission_required('Librarian', 'relationship_app.change_book')
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book_form.html'
    success_url = reverse_lazy('list_books')

@class_login_role_and_permission_required('Librarian', 'relationship_app.delete_book')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'relationship_app/book_confirm_delete.html'
    success_url = reverse_lazy('list_books')
