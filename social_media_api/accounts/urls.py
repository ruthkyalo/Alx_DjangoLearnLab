from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserViewSet
from django.urls import path
from .views import RegisterView, FollowUserView, UnfollowUserView
from rest_framework.authtoken.views import obtain_auth_token

# DRF router for follow/unfollow
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),  # DRF token login
    path('', include(router.urls)),  # include the user follow/unfollow routes
    path('users/<int:pk>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('users/<int:pk>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
]
