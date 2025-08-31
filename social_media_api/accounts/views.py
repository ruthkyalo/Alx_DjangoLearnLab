from rest_framework import generics
from .serializers import UserRegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_serializer().instance
        token, created = Token.objects.get_or_create(user=user)
        response.data['token'] = token.key
        return response
