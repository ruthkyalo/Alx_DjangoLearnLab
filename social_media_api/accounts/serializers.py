from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class UserRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField() 

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'bio', 'profile_picture', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Use get_user_model().objects.create_user directly
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        token = Token.objects.create(user=user)
        user.token = token.key
        return user
