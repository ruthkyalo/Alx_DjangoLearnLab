from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import Library, Book, UserProfile
from .forms import BookForm

# View to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Library detail view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# User registration view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Adjust redirect target as needed
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

# Role-based dashboards
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

# Class-based decorators
def class_login_and_role_required(role):
    return method_decorator([login_required, user_passes_test(check_role(role))], name='dispatch')

def class_permission_required(perm):
    return method_decorator(permission_required(perm, raise_exception=True), name='dispatch')

# Book creation view (requires Librarian role and add permission)
@class_login_and_role_required('Librarian')
@class_permission_required('relationship_app.can_add_book')
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book_form.html'
    success_url = reverse_lazy('list_books')

# Book update view (requires Librarian role and change permission)
@class_login_and_role_required('Librarian')
@class_permission_required('relationship_app.can_change_book')
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'relationship_app/book_form.html'
    success_url = reverse_lazy('list_books')

# Book delete view (requires Librarian role and delete permission)
@class_login_and_role_required('Librarian')
@class_permission_required('relationship_app.can_delete_book')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'relationship_app/book_confirm_delete.html'
    success_url = reverse_lazy('list_books')
