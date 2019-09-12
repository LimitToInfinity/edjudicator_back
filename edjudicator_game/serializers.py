from rest_framework import serializers
from .models import HighScore
from django.contrib.auth.models import User

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class HighScoreSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
    # username = serializers.CharField(source="user.username")
    # email = serializers.CharField(source="user.email")

    def update(self, instance, validated_data):
        user_data = validated_data.get("user", instance.user)
        user_serializer = UserSerializer(instance=instance.user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
        instance.value = validated_data.get("value", instance.value)
        instance.save()
        return instance

    class Meta:
        model = HighScore
        fields = ("user", "value")
