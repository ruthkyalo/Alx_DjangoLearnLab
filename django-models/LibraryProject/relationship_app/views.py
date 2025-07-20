from django.shortcuts import render
from .models import Library
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile

# Function-Based View to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-Based View for library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # <-- FIXED
    context_object_name = 'library'

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('home')  # or wherever you want to redirect
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def check_role(role):
    def inner(user):
        try:
            return user.userprofile.role == role
        except UserProfile.DoesNotExist:
            return False
    return inner

@login_required
@user_passes_test(check_role('Admin'))
def admin_view(request):
    return render(request, 'admin_view.html')

@login_required
@user_passes_test(check_role('Librarian'))
def librarian_view(request):
    return render(request, 'librarian_view.html')

@login_required
@user_passes_test(check_role('Member'))
def member_view(request):
    return render(request, 'member_view.html')