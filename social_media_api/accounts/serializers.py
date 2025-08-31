from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True) 

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # use get_user_model().objects.create_user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        token = Token.objects.create(user=user)
        user.token = token.key  # include token in serializer output
        return user
