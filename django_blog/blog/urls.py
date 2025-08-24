from django.urls import path
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # create
    path('', PostListView.as_view(), name='post-list'),  # list of posts
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # create
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # detail
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # update
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # delete
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),



]
