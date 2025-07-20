from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('admin-dashboard/', views.admin_view, name='admin_view'),
    path('librarian-dashboard/', views.librarian_view, name='librarian_view'),
    path('member-dashboard/', views.member_view, name='member_view'),
    path('', BookListView.as_view(), name='book-list'),
    path('add/', add_book, name='add-book'),
    path('edit/<int:pk>/', edit_book, name='edit-book'),
    path('delete/<int:pk>/', delete_book, name='delete-book'),
]
