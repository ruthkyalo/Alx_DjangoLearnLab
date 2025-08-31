from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification

# Custom permission
class IsAuthorOrReadOnly(permissions.BasePermission):
    """Only authors can edit/delete their content"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

# Post CRUD with Like/Unlike
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    filter_backends = [filters.SearchFilter]  
    search_fields = ['title', 'content'] 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Like a post
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        # Create notification if liking someone else's post
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.id
            )
        return Response({'status': 'Post liked'})

    # Unlike a post
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            return Response({'status': 'Post unliked'})
        except Like.DoesNotExist:
            return Response({'detail': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

# Comment CRUD remains the same
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
