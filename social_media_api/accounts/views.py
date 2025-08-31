from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer
from .models import CustomUser

# Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_serializer().instance
        token, created = Token.objects.get_or_create(user=user)
        response.data['token'] = token.key
        return response

# Follow User
class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        user_to_follow = self.get_queryset().get(pk=pk)
        request.user.following.add(user_to_follow)
        return Response({'status': f'You are now following {user_to_follow.username}'}, status=status.HTTP_200_OK)

# Unfollow User
class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        user_to_unfollow = self.get_queryset().get(pk=pk)
        request.user.following.remove(user_to_unfollow)
        return Response({'status': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)
