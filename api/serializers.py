from rest_framework import serializers
from .models import User, Post
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name','password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    email = serializers.EmailField()
    name = serializers.EmailField(required=False)
    password = serializers.CharField()
    tokens = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError('Email is required')

        if not password:
            raise serializers.ValidationError('Password is required')
        user_active = User.objects.filter(email = email).first()
        if user_active:
            if not user_active.is_active:
                raise serializers.ValidationError('Your Profile is LOCK. Please connect to the support')

        try:
            user = authenticate(username=email, password=password)
        except Exception:
            raise serializers.ValidationError(
                'Error occurred while logging in')

        if not user:
            raise serializers.ValidationError('Incorrect email or password')

        if not user.is_active:
            raise serializers.ValidationError('Your Profile is LOCK. Please connect to the support')

        data['user'] = user
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "tokens": user.tokens().get("access"),
            "refresh_token": user.tokens().get("refresh"),
            "password": user.password,
        }

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at')

class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at')
